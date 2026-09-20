import os
import shlex
import subprocess
import platform
import shutil
import sys
import re
from mcp.server.mcpserver import MCPServer
from Kathara.manager.Kathara import Kathara
from Kathara.parser.netkit.LabParser import LabParser
from Kathara.setting.Setting import Setting

# Inizializziamo il Server FastMCP
mcp = MCPServer("ServerGestioneKathara")

@mcp.tool()
def analizza_compito(percorso_file: str) -> str:
    """
    Legge un file, pulisce la numerazione a paragrafi e restituisce il testo affiancato dalle soluzioni.
    """
    try:
        if not os.path.isfile(percorso_file):
            return f"❌ Errore: Il file '{percorso_file}' non esiste."
            
        with open(percorso_file, 'r', encoding='utf-8') as f:
            testo = f.read()
            
        soluzioni = {}
        contatore = 1
        
        def rimpiazza_blocco(match):
            nonlocal contatore
            blocco = match.group(1)
            corrette = re.findall(r"~=([^#]+)#OK", blocco)
            id_domanda = f"[DOMANDA {contatore}]"
            if corrette:
                soluzioni[id_domanda] = " OPPURE ".join(corrette)
            else:
                soluzioni[id_domanda] = "Nessuna soluzione specificata"
            contatore += 1
            return id_domanda

        testo_pulito = re.sub(r"\{([^}]+)\}", rimpiazza_blocco, testo)
        
        # Rimuove i numeri di paragrafo per non confondere l'IA
        testo_pulito = re.sub(r"^\s*(\d+|[a-z])\.\s*", "", testo_pulito, flags=re.MULTILINE)
        
        risultato_finale = "📄 TESTO DEL COMPITO:\n"
        risultato_finale += testo_pulito.strip() + "\n\n"
        
        risultato_finale += "✅ CHIAVE DI LETTURA (SOLUZIONI CORRETTE):\n"
        for id_dom, sol in soluzioni.items():
            risultato_finale += f"{id_dom}: {sol}\n"
            
        return risultato_finale
        
    except Exception as e:
        return f"❌ Errore durante l'analisi: {str(e)}"
    
@mcp.tool()
def leggi_file_laboratorio(percorso_lab: str, file_relativo: str) -> str:
    """
    Legge il contenuto di un file di configurazione del laboratorio (es. lab.conf, pc1.startup, pc2/etc/resolv.conf).
    Da usare SEMPRE per l'analisi statica prima di eseguire comandi nei terminali.
    """
    # Costruisce il percorso assoluto unendo la cartella del lab e il nome del file
    percorso_completo = os.path.join(percorso_lab, file_relativo)
    
    if not os.path.exists(percorso_completo):
        return f"❌ Errore: Il file '{file_relativo}' non esiste in '{percorso_lab}'."
    
    if not os.path.isfile(percorso_completo):
        return f"❌ Errore: '{file_relativo}' è una cartella, non un file."
        
    try:
        with open(percorso_completo, 'r', encoding='utf-8') as f:
            contenuto = f.read()
        return f"📄 Contenuto di {file_relativo}:\n\n{contenuto}"
    except Exception as e:
        return f"❌ Errore durante la lettura del file: {str(e)}"    
    
@mcp.tool()
def avvia_laboratorio(percorso_lab: str) -> str:
    """Legge la configurazione, avvia il lab e apre i terminali usando Docker exec in modo multipiattaforma."""
    try:
        if not os.path.isdir(percorso_lab):
            return f"❌ Errore: La cartella '{percorso_lab}' non esiste."
            
        # 1. Analizza la cartella
        lab = LabParser.parse(percorso_lab)
        
        # 2. ASSEGNAZIONE AUTOMATICA DEL NOME (se mancante)
        if not lab.name:
            # Estrae il nome dell'ultima cartella dal percorso
            lab.name = os.path.basename(os.path.normpath(percorso_lab))
            
        # 3. Avvia il lab con le API native
        Kathara.get_instance().deploy_lab(lab)
        
        # 4. Interroga Docker per i container
        risultato_docker = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"], 
            capture_output=True, text=True, check=True
        )
        lista_container = risultato_docker.stdout.strip().split('\n')
        
        # Rileva il sistema operativo una sola volta fuori dal ciclo per efficienza
        sistema_operativo = platform.system()
        
        # 5. Apre i terminali
        macchine_avviate = list(lab.machines.keys())
        for nome_macchina in macchine_avviate:
            nome_container = None
            for linea in lista_container:
                if f"_{nome_macchina}_" in linea:
                    nome_container = linea.strip()
                    break
            
            if nome_container:
                comando_connessione = f"docker exec -it {nome_container} /bin/bash"
                
                if sistema_operativo == "Windows":
                    # NOTA: Usiamo /c affinché le finestre si chiudano da sole quando il lab viene spento
                    subprocess.Popen(f'start cmd.exe /c {comando_connessione}', shell=True)
                    
                elif sistema_operativo == "Linux":
                    # Cerca dinamicamente il terminale installato sulla distro Linux
                    if shutil.which("gnome-terminal"):
                        subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{comando_connessione}; exec bash"])
                    elif shutil.which("konsole"):
                        subprocess.Popen(["konsole", "-e", "bash", "-c", f"{comando_connessione}; exec bash"])
                    elif shutil.which("xfce4-terminal"):
                        subprocess.Popen(["xfce4-terminal", "-e", f"bash -c '{comando_connessione}; exec bash'"])
                    elif shutil.which("xterm"):
                        subprocess.Popen(["xterm", "-e", f"bash -c '{comando_connessione}; exec bash'"])
                    else:
                        print(f"⚠️ Nessun emulatore di terminale riconosciuto trovato per {nome_macchina}.")
                        
                elif sistema_operativo == "Darwin":
                    # Supporto per macOS
                    subprocess.Popen(["osascript", "-e", f'tell app "Terminal" to do script "{comando_connessione}"'])
            else:
                print(f"⚠️ Impossibile aprire il terminale per {nome_macchina}: container non trovato.")
                
        return f"✅ Laboratorio '{lab.name}' avviato. Terminali aperti."
        
    except Exception as e:
        return f"❌ Errore durante l'avvio del laboratorio: {str(e)}"

@mcp.tool()
def spegni_laboratorio(nome_lab: str) -> str:
    """Spegne ed elimina un laboratorio in esecuzione utilizzando il suo nome."""
    try:
        # undeploy_lab accetta direttamente il nome del lab per spegnerlo
        Kathara.get_instance().undeploy_lab(lab_name=nome_lab)
        
        return f"✅ Laboratorio '{nome_lab}' spento e rimosso. Le finestre dei terminali si chiuderanno automaticamente."
    except Exception as e:
        return f"❌ Errore durante lo spegnimento del laboratorio: {str(e)}"
    

@mcp.tool()
def esegui_comando_filtrato(nome_macchina: str, nome_lab: str, comando: str) -> str:
    """
    Esegue un comando di terminale su un nodo del laboratorio Kathará.
    ATTENZIONE: L'output è limitato a un massimo di 30 righe per prevenire overflow.
    Se l'output è troppo lungo, usa 'grep' o 'head' nel comando per filtrare i risultati.
    """
    try:
        # 1. Esecuzione nativa tramite l'istanza di Kathará
        stdout, stderr, exit_code = Kathara.get_instance().exec(
            machine_name=nome_macchina,
            lab_name=nome_lab,
            command=shlex.split(comando),
            wait=True,
            stream=False
        )
        
        risultato_grezzo = ""
        if stdout: 
            risultato_grezzo += f"STDOUT:\n{stdout.decode('utf-8')}\n"
        if stderr: 
            risultato_grezzo += f"STDERR:\n{stderr.decode('utf-8')}\n"
            
        # 2. Logica di filtraggio e troncamento
        if not risultato_grezzo.strip():
            return f"Codice di uscita: {exit_code} (Nessun output testuale)"
            
        righe = risultato_grezzo.splitlines()
        max_righe = 30
        
        if len(righe) > max_righe:
            righe_filtrate = righe[:max_righe]
            messaggio_alert = (
                f"\n\n[⚠️ ALLERTA SISTEMA: OUTPUT TRONCATO]\n"
                f"Il comando ha generato {len(righe)} righe, superando il limite di sicurezza.\n"
                f"Sono state mostrate solo le prime {max_righe} righe. Riformula il comando usando 'grep' per cercare la stringa esatta."
            )
            return "\n".join(righe_filtrate) + messaggio_alert
            
        return risultato_grezzo

    except Exception as e:
        return f"❌ Errore durante l'esecuzione del comando su {nome_macchina}: {str(e)}"

if __name__ == "__main__":
    manager = Kathara.get_instance()
    mcp.run()