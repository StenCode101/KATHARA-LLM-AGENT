import os
import shlex
from mcp.server.mcpserver import MCPServer
from Kathara.manager.Kathara import Kathara
from Kathara.parser.netkit.LabParser import LabParser

import subprocess
import sys
from Kathara.setting.Setting import Setting

# Inizializziamo il Server FastMCP
mcp = MCPServer("ServerGestioneKathara")

@mcp.tool()
def avvia_laboratorio(percorso_lab: str) -> str:
    """Legge la configurazione, avvia il lab e apre i terminali usando le API native di Kathará."""
    try:
        if not os.path.isdir(percorso_lab):
            return f"❌ Errore: La cartella '{percorso_lab}' non esiste."
            
        # 1. Analizza la cartella tramite il parser ufficiale
        lab = LabParser.parse(percorso_lab)
        
        # 2. Esegue il deploy dell'infrastruttura
        Kathara.get_instance().deploy_lab(lab)
        
        # 3. Ottiene la shell predefinita configurata in Kathará (es. /bin/bash)
        shell_dispositivo = Setting.get_instance().device_shell
        
        # 4. Apre un terminale per ogni macchina avviata
        macchine_avviate = list(lab.machines.keys())
        for nome_macchina in macchine_avviate:
            # Crea il comando Python nativo documentato nelle API
            comando_api = (
                f"from Kathara.manager.Kathara import Kathara; "
                f"Kathara.get_instance().connect_tty('{nome_macchina}', lab_name='{lab.name}', shell='{shell_dispositivo}', logs=True)"
            )
            
            # Esegue il comando in una nuova finestra di Windows (CREATE_NEW_CONSOLE)
            subprocess.Popen(
                [sys.executable, "-c", comando_api],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            
        return f"✅ Laboratorio '{lab.name}' avviato. Terminali nativi aperti per: {', '.join(macchine_avviate)}."
        
    except Exception as e:
        return f"❌ Errore durante l'avvio del laboratorio: {str(e)}"

@mcp.tool()
def spegni_laboratorio(nome_lab: str) -> str:
    """Spegne ed elimina un laboratorio in esecuzione utilizzando il suo nome."""
    try:
        Kathara.get_instance().undeploy_lab(lab_name=nome_lab)
        return f"✅ Laboratorio '{nome_lab}' spento e rimosso con successo."
    except Exception as e:
        return f"❌ Errore durante lo spegnimento del laboratorio: {str(e)}"
    
    
    
@mcp.tool()
def stato_macchine(nome_lab: str) -> str:
    """Restituisce la lista delle macchine del laboratorio con i loro nomi brevi originali."""
    try:
        # Recupera l'oggetto Lab ad alto livello invece dei container grezzi
        lab = Kathara.get_instance().get_lab_from_api(lab_name=nome_lab)
        
        if not lab or not lab.machines:
            return f"Nessuna macchina trovata per il lab '{nome_lab}'."
            
        risultato = f"Dispositivi attivi nel lab '{nome_lab}':\n"
        
        # lab.machines è un dizionario che usa i nomi brevi (es. 'r3', 'pc1') come chiavi
        for nome_macchina in lab.machines.keys():
            risultato += f"- {nome_macchina}\n"
            
        return risultato
    except Exception as e:
        return f"❌ Errore durante la lettura dello stato: {str(e)}"
    

@mcp.tool()
def apri_terminale(nome_macchina: str) -> str:
    """Apre una finestra di terminale fisica per interagire con una macchina specifica usando Docker."""
    try:
        # 1. Interroga Docker per ottenere i nomi di tutti i container in esecuzione
        risultato_docker = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"], 
            capture_output=True, text=True, check=True
        )
        
        # 2. Cerca il container esatto che contiene il nome del nodo (es. "_pc1_")
        nome_container = None
        for linea in risultato_docker.stdout.strip().split('\n'):
            if f"_{nome_macchina}_" in linea:
                nome_container = linea.strip()
                break
        
        if not nome_container:
            return f"❌ Dispositivo '{nome_macchina}' non trovato su Docker. Sicuro sia avviato?"
        
        # 3. Lancia il terminale di sistema entrando direttamente nel container tramite Docker
        comando_windows = f"start cmd.exe /k docker exec -it {nome_container} /bin/bash"
        
        subprocess.Popen(comando_windows, shell=True)
        
        return f"✅ Finestra del terminale richiesta per {nome_macchina}."
    except Exception as e:
        return f"❌ Errore nell'apertura del terminale: {str(e)}"

@mcp.tool()
def esegui_comando(nome_macchina: str, nome_lab: str, comando: str) -> str:
    """Esegue un comando non interattivo all'interno di una macchina virtuale."""
    try:
        stdout, stderr, exit_code = Kathara.get_instance().exec(
            machine_name=nome_macchina,
            lab_name=nome_lab,
            command=shlex.split(comando),
            wait=True,
            stream=False
        )
        
        risultato = ""
        if stdout: risultato += f"STDOUT:\n{stdout.decode('utf-8')}\n"
        if stderr: risultato += f"STDERR:\n{stderr.decode('utf-8')}\n"
            
        return risultato if risultato else f"Codice di uscita: {exit_code} (Nessun output testuale)"
    except Exception as e:
        return f"❌ Errore di esecuzione su {nome_macchina}: {str(e)}"

if __name__ == "__main__":
    manager = Kathara.get_instance()
    mcp.run()