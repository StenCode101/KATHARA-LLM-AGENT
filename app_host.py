import asyncio, os, sys, itertools, aiohttp
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELLO = "qwen3:8b" 

def formatta_tools(tools_mcp):
    return [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": {"type": "object", "properties": t.input_schema.get("properties", {}), "required": t.input_schema.get("required", [])}}} for t in tools_mcp]

async def mostra_caricamento(evento_stop):
    """Mostra un'animazione di caricamento nel terminale finché l'evento non viene impostato."""
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    
    while not evento_stop.is_set():
        sys.stdout.write(f"\r⏳ Elaborazione IA {next(spinner)}")
        sys.stdout.flush()
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
            
    # Pulisce la riga quando ha finito
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

async def main():
    print("🔄 Connessione al Server MCP Kathara API...")
    
    project_dir = os.path.dirname(os.path.abspath(__file__))
    project_python = os.path.join(project_dir, "env", "Scripts", "python.exe")
    server_python = project_python if os.path.exists(project_python) else sys.executable
    server_script = os.path.join(project_dir, "server_kathara.py")
    server_params = StdioServerParameters(command=server_python, args=[server_script])
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            
            print("\n✅ Server Operativo! Puoi gestire i lab Kathará.")
            print("-" * 50)
            
            storico_messaggi = [{
                "role": "system", 
                "content": (
                    "Sei un ingegnere di reti. Puoi usare gli strumenti per avviare, spegnere e inviare comandi a laboratori Kathará esistenti. "
                    "Quando l'utente ti chiede di risolvere un compito, usa lo strumento analizza_compito per leggere il file. "
                    "Per ogni domanda trovata, NON limitarti a leggere la soluzione: indaga attivamente sul laboratorio usando esegui_comando "
                    "(es. tcpdump, ping, ip route) per ricavare tu stesso la risposta. "
                    "Infine, scrivi la tua analisi dettagliata e confronta il risultato ottenuto sul campo con la soluzione corretta fornita dal file, "
                    "spiegando il perché del risultato. "
                    "REGOLA CRITICA: Quando esegui un ping, devi SEMPRE usare il parametro -c (es. ping -c 2 <ip>)."
                )
            }]
            
            while True:
                # Gestione sicura dell'input per evitare crash se premi Ctrl+C al prompt
                try:
                    prompt = input("👤 Tu: ")
                except KeyboardInterrupt:
                    print("\nUsa 'esci' per chiudere il programma.")
                    continue
                    
                if prompt.lower() in ["esci", "exit", "quit"]:
                    break
                
                # Svuota la memoria se l'IA si confonde
                if prompt.lower() in ["reset", "pulisci", "clear"]:
                    storico_messaggi = [storico_messaggi[0]]
                    print("🧹 Memoria azzerata. Contesto pulito.\n")
                    continue
                    
                storico_messaggi.append({"role": "user", "content": prompt})
                
                # BLOCCO TRY-EXCEPT PER INTERROMPERE IL RAGIONAMENTO (CTRL+C)
                try:
                    while True:
                        # Troncamento automatico della memoria
                        if len(storico_messaggi) > 7:
                            storico_messaggi = [storico_messaggi[0]] + storico_messaggi[-6:]

                        payload = {
                            "model": MODELLO, 
                            "messages": storico_messaggi, 
                            "stream": False, 
                            "tools": formatta_tools(tools.tools)
                        }
                        
                        # Inizializzazione del caricatore animato
                        evento_stop = asyncio.Event()
                        task_caricamento = asyncio.create_task(mostra_caricamento(evento_stop))
                        
                        try:
                            # aiohttp è asincrono nativo: taglia la connessione all'istante su Ctrl+C
                            # Imposta total=None per disabilitare il limite di tempo e aspettare Ollama all'infinito
                            timeout_infinito = aiohttp.ClientTimeout(total=None)
                            async with aiohttp.ClientSession(timeout=timeout_infinito) as session_http:
                                async with session_http.post(OLLAMA_URL, json=payload) as risposta_http:
                                    risposta_http.raise_for_status() 
                                    risposta_grezza = await risposta_http.json()
                                    
                        except aiohttp.ClientError as e:
                            print(f"\n⚠️ Errore di comunicazione con Ollama: {e}")
                            print("Ritorno al prompt principale.\n")
                            break
                        except Exception as e:
                            import traceback
                            print(f"\n⚠️ Errore imprevisto durante l'elaborazione: {e}")
                            print("🔍 DETTAGLIO ERRORE:")
                            traceback.print_exc()
                            break
                        finally:
                            # Ferma sempre l'animazione, sia in caso di successo che di interruzione
                            evento_stop.set()
                            await task_caricamento
                        
                        if "error" in risposta_grezza:
                            print(f"\n❌ ERRORE INTERNO OLLAMA: {risposta_grezza['error']}")
                            break
                            
                        risposta = risposta_grezza.get("message", {})
                        if not risposta:
                            break
                            
                        storico_messaggi.append(risposta)
                        
                        if "tool_calls" in risposta and risposta["tool_calls"]:
                            for chiamata in risposta["tool_calls"]:
                                nome_tool = chiamata["function"]["name"]
                                argomenti = chiamata["function"]["arguments"]
                                
                                print(f"🛠️  Esecuzione [{nome_tool}]...")
                                try:
                                    risultato = await session.call_tool(nome_tool, argomenti)
                                    testo_risultato = risultato.content[0].text
                                    print(f"✅ Esito:\n{testo_risultato}\n")
                                except Exception as e:
                                    testo_risultato = f"Errore interno: {str(e)}"
                                    print(f"❌ {testo_risultato}\n")
                                
                                storico_messaggi.append({
                                    "role": "tool",
                                    "content": testo_risultato,
                                    "name": nome_tool
                                })
                        else:
                            print(f"🧠 IA: {risposta.get('content', '')}\n")
                            break
                            
                # CATTURA L'INTERRUZIONE MANUALE
                except KeyboardInterrupt:
                    print("\n\n🛑 Ragionamento interrotto manualmente!")
                    # Rimuoviamo le ultime interazioni incomplete per non sporcare il contesto
                    storico_messaggi = storico_messaggi[:-1]
                    print("Ritorno al prompt principale...\n")

if __name__ == "__main__":
    try:                        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Programma interrotto dall'utente.")