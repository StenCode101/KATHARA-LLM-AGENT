import asyncio, os, requests, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


OLLAMA_URL = "http://localhost:11434/api/chat"
MODELLO = "qwen3:8b" 

def formatta_tools(tools_mcp):
    return [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": {"type": "object", "properties": t.input_schema.get("properties", {}), "required": t.input_schema.get("required", [])}}} for t in tools_mcp]

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
                "content": "Sei un ingegnere di reti. Puoi usare gli strumenti per avviare, spegnere e inviare comandi a laboratori Kathará esistenti. Quando l'utente chiede test di rete (come tcpdump o ping), usa lo strumento esegui_comando."
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
                
                # NUOVO COMANDO: Svuota la memoria se l'IA si confonde
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
                        
                        try:
                            risposta_http = requests.post(OLLAMA_URL, json=payload, timeout=120)
                            risposta_http.raise_for_status() 
                            risposta_grezza = risposta_http.json()
                        except requests.exceptions.RequestException as e:
                            print(f"\n⚠️ Errore di comunicazione con Ollama: {e}")
                            print("Ritorno al prompt principale.\n")
                            break
                        except ValueError:
                            print("\n⚠️ Ollama ha restituito una risposta illeggibile.")
                            break
                        
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