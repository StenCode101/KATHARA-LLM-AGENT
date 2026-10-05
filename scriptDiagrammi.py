import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.0
})

def draw_box(ax, x, y, w, h, text, bg='#ffffff', edge='black', lw=1.4, fontsize=9.0, bold=True, color='black', ls='-'):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.5",
                                 facecolor=bg, edgecolor=edge, linewidth=lw, linestyle=ls, zorder=3)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize,
            fontweight=weight, color=color, zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, text="", color='black', lw=1.6, style="->", text_offset=(0, 1.2), fontsize=8.4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw), zorder=2)
    if text:
        mx, my = (x1 + x2) / 2 + text_offset[0], (y1 + y2) / 2 + text_offset[1]
        ax.text(mx, my, text, ha='center', va='center', fontsize=fontsize, fontweight='bold',
                color=color, bbox=dict(boxstyle='round,pad=0.12', facecolor='white', edgecolor='none', alpha=0.9), zorder=5)

# ==============================================================================
# 1. FIGURA 1.1: Confronto Paradigma Manuale vs Agente AI (Cap. 1, Sez. 1.1)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 3.8))
ax.axis('off')
ax.set_xlim(0, 108)
ax.set_ylim(0, 38)

bg_left = patches.FancyBboxPatch((1, 2), 49, 34, boxstyle="round,pad=0.05,rounding_size=0.8",
                                 facecolor='#fcf2f2', edgecolor='#b85450', linewidth=1.5, linestyle='--')
ax.add_patch(bg_left)
ax.text(25.5, 33.5, "Approccio Tradizionale (Ispezione Manuale / Script Rigidi)",
        ha='center', va='center', fontsize=9.5, fontweight='bold', color='#900000')

draw_box(ax, 4, 13, 16, 12, "Operatore\nUmano /\nDocente", bg='#f8cecc', edge='#b85450')
draw_box(ax, 31, 23, 16, 7, "Container pc1\n( Terminale )", bg='#ffffff', edge='black', bold=False)
draw_box(ax, 31, 14, 16, 7, "Container r1\n( ip route )", bg='#ffffff', edge='black', bold=False)
draw_box(ax, 31, 5, 16, 7, "Container pcN\n( lab.conf )", bg='#ffffff', edge='black', bold=False)

draw_arrow(ax, 20.5, 21, 30.5, 26.5, "CLI 1", color='#900000', text_offset=(-1, 1.5), fontsize=8)
draw_arrow(ax, 20.5, 19, 30.5, 17.5, "CLI 2", color='#900000', text_offset=(0, 1.5), fontsize=8)
draw_arrow(ax, 20.5, 17, 30.5, 8.5, "CLI N", color='#900000', text_offset=(-1, -1.8), fontsize=8)

bg_right = patches.FancyBboxPatch((54, 2), 53, 34, boxstyle="round,pad=0.05,rounding_size=0.8",
                                  facecolor='#f3f9f1', edgecolor='#274e13', linewidth=1.5)
ax.add_patch(bg_right)
ax.text(80.5, 33.5, "Architettura Proposta (Orchestrazione Autonoma AI + MCP)",
        ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e4620')

draw_box(ax, 56, 13, 13, 12, "Utente\n(Query in\nLinguaggio\nNaturale)", bg='#dae8fc', edge='#1f4e79', fontsize=8.4)
draw_box(ax, 73, 13, 15, 12, "Agente AI\n(Ollama 8B\n+ Client MCP)", bg='#d5e8d4', edge='#274e13', fontsize=8.4)
draw_box(ax, 92, 13, 13, 12, "Server MCP\n&\nNamespace\nDocker", bg='#ffe599', edge='black', fontsize=8.4)

draw_arrow(ax, 69.3, 19, 72.7, 19, style="<->", color='#1f4e79')
draw_arrow(ax, 88.3, 19, 91.7, 19, style="<->", color='#274e13')
ax.text(80.5, 6.5, "Ispezione automatica, Grounding deterministico e Zero Data-Leak",
        ha='center', va='center', fontsize=8.6, style='italic', fontweight='bold', color='#1e4620')

plt.tight_layout()
plt.savefig('fig_1_1_confronto_paradigma.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 2. FIGURA 1.2: Metodologia di Ricerca in 4 Fasi (Cap. 1, Sez. 1.3)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 3.2))
ax.axis('off')
ax.set_xlim(0, 108)
ax.set_ylim(0, 32)

fasi = [
    (2, 13, 22, 15, '#dae8fc', "Fase 1: Setup\nTopologie Kathará\ne Container Docker\n(Ambiente Test)"),
    (29, 13, 22, 15, '#fff2cc', "Fase 2: Backend\nSviluppo Server MCP\ne 4 Primitive Tool\n(Sanitizzazione)"),
    (56, 13, 22, 15, '#d5e8d4', "Fase 3: Cognizione\nPrompt Engineering,\nChain-of-Thought\ne REGOLE-RETE.md"),
    (83, 13, 23, 15, '#e1d5e7', "Fase 4: Tuning\nGeneratori yield,\nCalibrazione Sampling\ne Telemetria")
]

for (bx, by, bw, bh, col, txt) in fasi:
    draw_box(ax, bx, by, bw, bh, txt, bg=col, fontsize=8.5)

for x1, x2 in [(24.4, 28.6), (51.4, 55.6), (78.4, 82.6)]:
    draw_arrow(ax, x1, 20.5, x2, 20.5)

ax.plot([94.5, 94.5, 40.0], [12.6, 5.0, 5.0], color='#900000', linewidth=1.8, linestyle='--')
draw_arrow(ax, 40.0, 5.0, 40.0, 12.6, color='#900000', lw=1.8)
ax.text(67.2, 2.2, "Ciclo continuo di Feedback Empirico, Trial-and-Error e Raffinamento",
        ha='center', va='center', fontsize=9.0, style='italic', fontweight='bold', color='#900000')

plt.tight_layout()
plt.savefig('fig_1_2_metodologia_fasi.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 3. FIGURA 2.1: Architettura API REST Stateless Ollama (Zero sconfinamenti!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.6, 3.5))
ax.axis('off')
ax.set_xlim(0, 106)
ax.set_ylim(0, 35)

# Box laterali larghi 27 unità -> corridoio centrale largo ben 46 unità (da x=30 a x=76)!
draw_box(ax, 2, 6, 27, 23, "Client AI (Python Host)\n\n• Gestione storico_messaggi\n• Iniezione REGOLE-RETE.md\n• Schemi JSON Tool MCP\n• Parametri options (T, top_p)",
         bg='#dae8fc', edge='#1f4e79', fontsize=8.4)

draw_box(ax, 77, 6, 27, 23, "Server Ollama Locale\n(127.0.0.1 : 11434)\n\n• Endpoint /api/chat (Stateless)\n• Pesi qwen3:8b (Q4) in VRAM\n• Prefill / Decode + KV Cache",
         bg='#d5e8d4', edge='#274e13', fontsize=8.4)

draw_arrow(ax, 30.0, 23.0, 76.0, 23.0, "HTTP POST /api/chat\n(Payload JSON Auto-Contenuto)", color='#1f4e79', text_offset=(0, 3.2), fontsize=8.4)
ax.text(53, 17.0, "Interfaccia di Loopback\n(localhost — Zero Traffico Esterno)", ha='center', va='center', fontsize=8.3, style='italic', color='#444444')
draw_arrow(ax, 76.0, 11.5, 30.0, 11.5, "HTTP 200 OK (JSON Response:\nmessage / tool_calls + Telemetria)", color='#274e13', text_offset=(0, -3.5), fontsize=8.4)

plt.tight_layout()
plt.savefig('fig_2_1_ollama_rest.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 4. FIGURA 2.3: Ciclo ReAct (Layout ortogonale senza alcuna intersezione!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 4.2))
ax.axis('off')
ax.set_xlim(0, 108)
ax.set_ylim(0, 42)

# Flusso principale in alto: 1. Input -> 2. Thought -> 5. Grounding
draw_box(ax, 2,  24, 19, 13, "1. Input Utente\nQuesito sulla\nRete Emulata", bg='#ededed', fontsize=8.6)
draw_box(ax, 29, 24, 24, 13, "2. Thought (Reasoning)\nAnalisi del problema e\npianificazione ispezione", bg='#fff2cc', edge='#b45f06', fontsize=8.5)
draw_box(ax, 84, 24, 22, 13, "5. Grounding Finale\nDiagnosi Verificata\nsu Dati Reali", bg='#d5e8d4', edge='#274e13', fontsize=8.6)

# Ciclo Tool in basso: 3. Action (a destra) e 4. Observation (a sinistra)
draw_box(ax, 58, 3,  23, 12, "3. Action (Tool Call)\nDirettiva JSON-RPC\nverso Server MCP", bg='#dae8fc', edge='#1f4e79', fontsize=8.4)
draw_box(ax, 29, 3,  24, 12, "4. Observation\nExec nel Container e\ncattura STDOUT", bg='#ffe599', edge='black', fontsize=8.4)

# 1 -> 2
draw_arrow(ax, 21.4, 30.5, 28.6, 30.5, color='black')

# 2 -> 5 (Convergenza dritta in alto senza toccare nulla!)
draw_arrow(ax, 53.4, 30.5, 83.6, 30.5, "Convergenza (Evidenze Sufficienti)", color='#274e13', text_offset=(0, 2.2), fontsize=8.3)

# 2 -> 3 (Scende da Thought a Action tramite gomito pulito)
ax.plot([69.5, 69.5], [27.0, 15.4], color='#1f4e79', linewidth=1.6)
ax.plot([53.4, 69.5], [27.0, 27.0], color='#1f4e79', linewidth=1.6)
draw_arrow(ax, 69.5, 17.0, 69.5, 15.3, color='#1f4e79')
ax.text(69.5, 21.5, "Tool Call\n(JSON-RPC)", ha='center', va='center', fontsize=8.0, fontweight='bold', color='#1f4e79',
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none'))

# 3 -> 4 (Da Action a Observation in basso)
draw_arrow(ax, 57.6, 9.0, 53.4, 9.0, color='black')

# 4 -> 2 (Da Observation risale dritto a Thought!)
draw_arrow(ax, 41.0, 15.4, 41.0, 23.6, "Feedback STDOUT", color='#b45f06', text_offset=(0, 0), fontsize=8.2)

plt.tight_layout()
plt.savefig('fig_2_3_ciclo_react.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 5. FIGURA 2.4: Astrazione Kathará e Docker Engine (Box Bridge allargato!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.5, 4.2))
ax.axis('off')
ax.set_xlim(0, 105)
ax.set_ylim(0, 42)

host_box = patches.FancyBboxPatch((2, 2), 101, 38, boxstyle="round,pad=0.05,rounding_size=0.8",
                                  facecolor='#f9f9f9', edgecolor='gray', linewidth=1.5)
ax.add_patch(host_box)
ax.text(52.5, 37.5, "Sistema Operativo Host (Kernel Linux Condiviso & Docker Engine)",
        ha='center', va='center', fontsize=10, fontweight='bold')

draw_box(ax, 6, 19, 29, 15, "Container Nodo: pc1\n[Network Namespace Isolato]\n\nInterfaccia eth0: 100.0.5.2/24\nTabella ARP & Routing Propria",
         bg='#dae8fc', edge='#1f4e79', fontsize=8.4)
draw_box(ax, 70, 19, 29, 15, "Container Nodo: r1\n[Network Namespace Isolato]\n\nInterfaccia eth0: 100.0.5.1/24\nDemone FRRouting (OSPF/BGP)",
         bg='#dae8fc', edge='#1f4e79', fontsize=8.4)

# Box Bridge allargato a 57 unità (da x=24 a x=81) così il testo non tocca mai i bordi!
draw_box(ax, 24, 4, 57, 9, "Bridge Virtuale Docker (Dominio di Collisione Kathará 'A1')\nEmulazione Livello 2 ISO/OSI",
         bg='#ffe599', edge='#b45f06', fontsize=8.6)

draw_arrow(ax, 20.5, 18.6, 36, 13.4, "veth pair", style="<->", color='#b45f06', text_offset=(-5.5, -0.5))
draw_arrow(ax, 84.5, 18.6, 69, 13.4, "veth pair", style="<->", color='#b45f06', text_offset=(5.5, -0.5))

draw_box(ax, 40, 22, 25, 9.5, "API Docker Engine\n(Iniezione Comandi\ndocker exec senza SSH)",
         bg='#d5e8d4', edge='#274e13', fontsize=8.3)
draw_arrow(ax, 39.6, 26.7, 35.4, 26.7, color='#274e13')
draw_arrow(ax, 65.4, 26.7, 69.6, 26.7, color='#274e13')

plt.tight_layout()
plt.savefig('fig_2_4_kathara_docker_net.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 6. FIGURA 2.5: Architettura Model Context Protocol (Corridoio stdio allargato!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 3.6))
ax.axis('off')
ax.set_xlim(0, 108)
ax.set_ylim(0, 36)

host_outer = patches.FancyBboxPatch((2, 4), 41, 28, boxstyle="round,pad=0.05,rounding_size=0.8",
                                    facecolor='#dae8fc', edgecolor='#1f4e79', linewidth=1.8)
ax.add_patch(host_outer)
ax.text(22.5, 29, "1. MCP Host (Orchestratore Python)", ha='center', va='center', fontsize=9.2, fontweight='bold', color='#1f4e79')
ax.text(13, 16.5, "• Ciclo REPL e Storico\n• System Prompt\n• Chiamate HTTP\n  verso Ollama (8B)", ha='center', va='center', fontsize=8.2)

draw_box(ax, 24.5, 6.5, 16.5, 18.5, "2. MCP Client\n\nTraduttore\nProtocollo\nJSON-RPC 2.0", bg='#ffffff', edge='#1f4e79', fontsize=8.3)

# Corridoio centrale da x=43 a x=64 (21 unità libere!)
draw_box(ax, 64, 4, 24, 28, "3. MCP Server\n(ServerGestioneKathara)\n\n• Esposizione Tools\n• Validazione Input\n• Troncamento 30 righe\n• Isolamento Sicurezza",
         bg='#d5e8d4', edge='#274e13', fontsize=8.3)

draw_box(ax, 92, 19, 14, 13, "File System\nStatico\n(lab.conf,\n.startup)", bg='#fff2cc', fontsize=8.2)
draw_box(ax, 92, 4, 14, 13, "Docker API\nDinamica\n(Container\nAttivi)", bg='#ffe599', fontsize=8.2)

ax.text(53.5, 26.5, "Canale Locale stdio\n(JSON-RPC 2.0)", ha='center', va='center', fontsize=8.2, style='italic', fontweight='bold')
draw_arrow(ax, 43.5, 19.0, 63.5, 19.0, "STDIN (Request)", color='#1f4e79', text_offset=(0, 2.0), fontsize=8.0)
draw_arrow(ax, 63.5, 12.5, 43.5, 12.5, "STDOUT (Response)", color='#274e13', text_offset=(0, -2.2), fontsize=8.0)

draw_arrow(ax, 88.4, 25.5, 91.6, 25.5, style="<->")
draw_arrow(ax, 88.4, 10.5, 91.6, 10.5, style="<->")

plt.tight_layout()
plt.savefig('fig_2_5_mcp_architettura.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 7. FIGURA 3.1: Diagramma di Sequenza UML delle 5 Fasi (Testi compatti!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(11.4, 5.4))
ax.axis('off')
ax.set_xlim(0, 116)
ax.set_ylim(0, 56)

lifelines = [
    (9,   "Operatore\nUtente", '#ededed'),
    (35,  "MCP Host / Client\n(Orchestratore)", '#dae8fc'),
    (62,  "Motore Ollama\n(qwen3:8b)", '#fff2cc'),
    (86,  "Server MCP\n(Kathará)", '#d5e8d4'),
    (107, "Container /\nFile System", '#ffe599')
]

for lx, title, col in lifelines:
    draw_box(ax, lx - 8.2, 47.5, 16.4, 6.8, title, bg=col, fontsize=8.3)
    ax.plot([lx, lx], [2, 47.5], color='gray', linestyle='--', linewidth=1.2, zorder=1)

seq = [
    (43.5, 9,   35,  "1. Query Diagnostica", '#000000', "->"),
    (38.5, 35,  62,  "2a. POST /api/chat (Prompt+Tools)", '#1f4e79', "->"),
    (33.5, 62,  35,  "2b. JSON tool_calls (funzione+args)", '#b45f06', "->"),
    (28.0, 35,  86,  "3. Chiamata JSON-RPC 2.0 via canale stdio", '#1f4e79', "->"),
    (22.5, 86,  107, "4a. lab.conf / exec()", '#274e13', "->"),
    (17.0, 107, 86,  "4b. STDOUT (≤30 righe)", '#274e13', "->"),
    (11.5, 86,  35,  "5a. Risposta JSON-RPC con evidenza empirica", '#274e13', "->"),
    (6.5,  35,  62,  "5b. POST output 'tool' e Sintesi", '#1f4e79', "<->"),
    (2.5,  35,  9,   "5c. Diagnosi Finale (Grounding)", '#000000', "->")
]

for (y, x1, x2, label, col, st) in seq:
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle=st, color=col, lw=1.6), zorder=3)
    mx = (x1 + x2) / 2
    ax.text(mx, y + 1.35, label, ha='center', va='center', fontsize=8.0, fontweight='bold', color=col,
            bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='none', alpha=0.92), zorder=4)

plt.tight_layout()
plt.savefig('fig_3_1_sequence_mcp.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 8. FIGURA 3.2: Architettura del Tooling del Server MCP (Albero ortogonale!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 4.0))
ax.axis('off')
ax.set_xlim(0, 108)
ax.set_ylim(0, 40)

# Box superiore allargato a 62 unità (da x=23 a x=85) così il testo ci sta comodamente!
draw_box(ax, 23, 29, 62, 9, "Processo ServerGestioneKathara (FastMCP)\nIntrospezione Decoratori @mcp.tool() e Generazione JSON Schema",
         bg='#d5e8d4', edge='#274e13', fontsize=8.8)

tools_boxes = [
    (2,  3, 23, 18, '#dae8fc', "1. avvia_laboratorio\n\n• LabParser.parse()\n• deploy_lab() nativo\n• Apertura terminali\n  multipiattaforma"),
    (29, 3, 23, 18, '#dae8fc', "2. spegni_laboratorio\n\n• undeploy_lab()\n• Rimozione container\n• Chiusura automatica\n  finestre terminale"),
    (56, 3, 23, 18, '#fff2cc', "3. leggi_file_lab\n\n• Lettura statica UTF-8\n• Fallback cartella lab/\n• Sanitizzazione path\n  os.path.isfile()"),
    (83, 3, 23, 18, '#ffe599', "4. esegui_comando\n\n• Kathara.exec() bash\n• Cattura STDOUT/ERR\n• Troncamento 30 righe\n  + Allerta grep/head")
]

# Bus ortogonale ad albero pulito (senza doppie punte!)
ax.plot([54, 54], [29.0, 25.0], color='black', linewidth=1.6)
ax.plot([13.5, 94.5], [25.0, 25.0], color='black', linewidth=1.6)

for (bx, by, bw, bh, col, txt) in tools_boxes:
    draw_box(ax, bx, by, bw, bh, txt, bg=col, fontsize=8.2)
    cx = bx + bw / 2
    draw_arrow(ax, cx, 25.0, cx, 21.3, color='black', lw=1.6)

plt.tight_layout()
plt.savefig('fig_3_2_tooling_server.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 9. FIGURA 3.3: Macchina a Stati della Bimodalità Operativa (Box largo + albero!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 4.2))
ax.axis('off')
ax.set_xlim(0, 108)
ax.set_ylim(0, 42)

# Box superiore allargato a 62 unità (da x=23 a x=85) così il testo non sborda mai!
draw_box(ax, 23, 32, 62, 8, "Input dell'Utente a Console o Comando 'analizza'\n(Classificazione Semantica dell'Intento nel System Prompt)",
         bg='#ededed', fontsize=8.8)

branches = [
    (3,  16, 30, 10, '#d5e8d4', "MODALITÀ 1:\nIngegnere Esecutivo\n(Troubleshooting & Lab)"),
    (39, 16, 30, 10, '#fff2cc', "SOTTO-PROFILO:\nRevisore di Sintassi\n(Verifica Comandi Errati)"),
    (75, 16, 30, 10, '#dae8fc', "MODALITÀ 2:\nTutor di Teoria\n(Domande Concettuali / Batch)")
]

actions = [
    (3,  2, 30, 10, '#ffffff', "• Autonomia Tool-Use obbligatoria\n• Divieto di delega all'utente\n• Verifica ibrida Statica + Dinamica"),
    (39, 2, 30, 10, '#ffffff', "• Inibizione esecuzione container\n• Analisi lessicale statica\n• Correzione flag Linux/Kathará"),
    (75, 2, 30, 10, '#ffffff', "• Barriera logica: Zero Tool Call\n• Omissione schemi JSON MCP\n• Spiegazione accademica rigorosa")
]

# Bus ortogonale ad albero tra il box superiore e i 3 rami
ax.plot([54, 54], [32.0, 29.0], color='black', linewidth=1.6)
ax.plot([18, 90], [29.0, 29.0], color='black', linewidth=1.6)

for (bx, by, bw, bh, col, txt) in branches:
    draw_box(ax, bx, by, bw, bh, txt, bg=col, fontsize=8.5)
    cx = bx + bw / 2
    draw_arrow(ax, cx, 29.0, cx, 26.3, color='black', lw=1.6)

for (bx, by, bw, bh, col, txt) in actions:
    draw_box(ax, bx, by, bw, bh, txt, bg=col, fontsize=8.2, bold=False)
    cx = bx + bw / 2
    draw_arrow(ax, cx, 15.8, cx, 12.3, color='black', lw=1.6)

plt.tight_layout()
plt.savefig('fig_3_3_bimodalita.pdf', bbox_inches='tight')
plt.close()

print("Tutti i 9 diagrammi architetturali sono stati rigenerati e corretti!")