import asyncio, os, sys, itertools, aiohttp, time
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELLO = "qwen3:8b" 
USA_SKILL = True  # 🔄 Interruttore per le regole compatte

def formatta_tools(tools_mcp):
    return [{"type": "function", "function": {"name": t.name, "description": t.description, "parameters": {"type": "object", "properties": t.input_schema.get("properties", {}), "required": t.input_schema.get("required", [])}}} for t in tools_mcp]

async def mostra_caricamento(evento_stop):
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not evento_stop.is_set():
        sys.stdout.write(f"\r⏳ Elaborazione IA {next(spinner)}")
        sys.stdout.flush()
        try:
            await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
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
            
            # SYSTEM PROMPT AGGIORNATO: L'IA diventa un Docente Teorico
            #SYSTEM PROMPT AGGIORNATO: Direttive contro l'allucinazione dei comandi e JSON strutturato
            contenuto_sistema = (
                "Sei un ingegnere di reti. Puoi usare gli strumenti per avviare, spegnere e inviare comandi a laboratori Kathará esistenti. "
                "REGOLA CRITICA 0 (COMPORTAMENTO REATTIVO): Non eseguire MAI strumenti (tool) di tua iniziativa. Usa un tool SOLO se l'utente ti ha esplicitamente richiesto un'azione pratica (es. 'avvia il lab', 'analizza il compito', 'controlla il router'). Se l'utente fa una domanda generica o teorica, rispondi testualmente senza attivare alcuno strumento. "
                "Quando l'utente ti chiede di risolvere un compito, usa lo strumento analizza_compito per leggere il file. "
                "Per ogni domanda trovata, esamina prima le configurazioni statiche (es. lab.conf, .startup) e poi verifica obbligatoriamente "
                "il comportamento reale sul campo usando esegui_comando_filtrato (es. tcpdump, ping, ip route) per ricavare la risposta definitiva. "
                "REGOLA CRITICA 1: Quando esegui unesci ping, devi SEMPRE usare il parametro -c (es. ping -c 2 ). "
                "REGOLA CRITICA 2 (VERITÀ SUI COMANDI): È assolutamente proibito inventare comandi o falsificare i risultati. Se per rispondere a una domanda non hai utilizzato uno strumento, devi scriverlo esplicitamente. Le giustificazioni devono riflettere i log reali. "
                "REGOLA CRITICA 3 (FORMATO DI USCITA RIGIDO): Quando fornisci l'analisi finale, devi restituire ESCLUSIVAMENTE un array JSON in cui ogni elemento corrisponde a una singola domanda del compito, rispettando rigorosamente la numerazione originale. "
                "NON aggiungere testo discorsivo prima o dopo l'array JSON. NON raggruppare le domande. Usa questa esatta struttura:\n"
                "[\n"
                "  {\n"
                "    \"id_domanda\": \"[DOMANDA X]\",\n"
                "    \"risposta_breve\": \"(solo il valore esatto)\",\n"
                "    \"comandi_eseguiti\": \"(elenca ESATTAMENTE i comandi digitati realmente. Se non hai usato comandi, scrivi 'Nessun comando eseguito - deduzione logica')\",\n"
                "    \"giustificazione\": \"(Fornisci un'analisi oggettiva: descrivi passo dopo passo il ragionamento logico che hai fatto, i file che hai realmente letto e come i risultati degli strumenti confermano la tua tesi)\"\n"
                "  }\n"
                "]"
            )

            
            # Iniezione del manuale compatto (che ora contiene anche le regole difensive)
            if USA_SKILL:
                testo_skills = ""
                percorso_regole = os.path.join(project_dir, "REGOLE-RETE.md")
                
                try:
                    if os.path.exists(percorso_regole):
                        with open(percorso_regole, "r", encoding="utf-8") as f:
                            testo_skills += "\n\n=== REGOLE E COMANDI KATHARA ===\n" + f.read()
                            
                    if testo_skills:
                        contenuto_sistema += f"\n\nDi seguito trovi la tua documentazione tecnica ufficiale da studiare e applicare rigorosamente:{testo_skills}"
                        print("📚 Modulo SKILL attivato: File REGOLE-RETE.md caricato nel contesto.")
                except Exception as e:
                    print(f"⚠️ Impossibile caricare il file REGOLE-RETE.md: {e}")
            else:
                print("⚡ Modulo SKILL disattivato: Esecuzione in modalità leggera.")

            storico_messaggi = [{"role": "system", "content": contenuto_sistema}]
            storico_report = [] 
            numero_prompt = 0
            
            while True:
                try:
                    prompt = input("👤 Tu: ")
                except KeyboardInterrupt:
                    print("\nUsa 'esci' per chiudere il programma.")
                    continue
                    
                if prompt.lower() in ["esci", "exit", "quit"]:
                    break
                
                if prompt.lower() in ["reset", "pulisci", "clear"]:
                    storico_messaggi = [storico_messaggi[0]]
                    storico_report.clear()
                    numero_prompt = 0
                    print("🧹 Memoria azzerata. Contesto e report puliti.\n")
                    continue
                    
                if prompt.lower() == "report":
                    nome_file = f"Report_Telemetria.md"
                    with open(nome_file, "w", encoding="utf-8") as f:
                        f.write("# 📊 Report Telemetria IA\n\n")
                        f.write("| Prompt # | Tempo (s) | Token Prompt | Token Generati | Velocità (tk/s) |\n")
                        f.write("|----------|-----------|--------------|----------------|-----------------|\n")
                        for r in storico_report:
                            f.write(f"| {r['id']} | {r['tempo']:.2f} | {r['prompt']} | {r['gen']} | {r['vel']:.1f} |\n")
                    print(f"📁 Report generato con successo: {nome_file}\n")
                    continue
                    
                storico_messaggi.append({"role": "user", "content": prompt})
                
                try:
                    contatore_tool = 0 
                    
                    while True:
                        if len(storico_messaggi) > 7:
                            storico_messaggi = [storico_messaggi[0]] + storico_messaggi[-6:]

                        payload = {
                            "model": MODELLO, 
                            "messages": storico_messaggi, 
                            "stream": False, 
                            "tools": formatta_tools(tools.tools),
                            "options": {
                                "num_ctx": 8192 
                            }
                        }
                        
                        inizio_timer = time.perf_counter()
                        evento_stop = asyncio.Event()
                        task_caricamento = asyncio.create_task(mostra_caricamento(evento_stop))
                        
                        try:
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
                            evento_stop.set()
                            await task_caricamento  
                        
                        tempo_totale = time.perf_counter() - inizio_timer
                        token_prompt = risposta_grezza.get("prompt_eval_count", 0)
                        token_risposta = risposta_grezza.get("eval_count", 0)
                        durata_generazione_ns = risposta_grezza.get("eval_duration", 0)
                        velocita = (token_risposta / (durata_generazione_ns / 1e9)) if durata_generazione_ns > 0 else 0
                        
                        print(f"📊 [REPORT IA] ⏱️ Rete+Elaborazione: {tempo_totale:.2f}s | 📥 Prompt: {token_prompt} tk | 📤 Gen: {token_risposta} tk | ⚡ Velocità: {velocita:.1f} tk/s\n")
                        
                        numero_prompt += 1
                        storico_report.append({
                            "id": numero_prompt,
                            "tempo": tempo_totale,
                            "prompt": token_prompt,
                            "gen": token_risposta,
                            "vel": velocita
                        })
                            
                        if "error" in risposta_grezza:
                            print(f"\n❌ ERRORE INTERNO OLLAMA: {risposta_grezza['error']}")
                            break
                            
                        risposta = risposta_grezza.get("message", {})
                        if not risposta:
                            break
                            
                        storico_messaggi.append(risposta)
                        
                        if "tool_calls" in risposta and risposta["tool_calls"]:
                            contatore_tool += 1 
                            
                            if contatore_tool > 50:
                                print(f"\n🛑 [ANTI-LOOP] Rilevati {contatore_tool} comandi consecutivi. Forzo l'interruzione di sicurezza...\n")
                                for chiamata in risposta["tool_calls"]:
                                    storico_messaggi.append({
                                        "role": "tool",
                                        "content": "SISTEMA: Limite di sicurezza anti-loop superato. Comando annullato. Genera ora l'array JSON strutturato con quello che hai scoperto finora.",
                                        "name": chiamata["function"]["name"]
                                    })
                                continue 
                                
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
                            # Stampa formattata aggiornata per il nuovo JSON del Docente
                            testo_risposta = risposta.get('content', '').strip()
                            try:
                                if testo_risposta.startswith("```json"):
                                    testo_risposta = testo_risposta.replace("```json\n", "").replace("```", "")
                                
                                dati_json = json.loads(testo_risposta)
                                print("\n🧠 RISPOSTA IA (Guida Teorica Strutturata):")
                                for elemento in dati_json:
                                    print(f"\n{elemento.get('id_domanda', '[ID MANCANTE]')}")
                                    print(f"  ├─ Valore Esatto: {elemento.get('risposta_breve', 'N/D')}")
                                    print(f"  ├─ Comando Suggerito: {elemento.get('comando_di_verifica', 'N/D')}")
                                    print(f"  └─ Spiegazione Teorica: {elemento.get('giustificazione_teorica', 'N/D')}")
                                print("\n")
                            except json.JSONDecodeError:
                                print(f"🧠 IA (Formato non JSON):\n{testo_risposta}\n")
                            break
                            
                except KeyboardInterrupt:
                    print("\n\n🛑 Ragionamento interrotto manualmente!")
                    storico_messaggi = storico_messaggi[:-1]
                    print("Ritorno al prompt principale...\n")

if __name__ == "__main__":
    try:                        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Programma interrotto dall'utente.")