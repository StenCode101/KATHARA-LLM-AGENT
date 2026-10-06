import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Configurazione stile accademico compatibile con LaTeX
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.5,
    "axes.labelsize": 11,
    "axes.titlesize": 11,
    "legend.fontsize": 9.0,
    "xtick.labelsize": 9.8,
    "ytick.labelsize": 9.8,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"
})

# ==============================================================================
# 1. FIGURA 2.2: Allocazione VRAM (4 GB) vs RAM (Senza titolo, c'è la caption)
# ==============================================================================
fig, ax = plt.subplots(figsize=(9.0, 4.2))

categorie = [
    'Modello 4B Puro\n(Stima Teorica Q4)',
    'gemma4:e4b (Q4)\n(4.5B Attivi + PLE)',
    'qwen3:8b (Q4)\n(8.2B Densi Attivi)'
]
vram_pesi = np.array([2.4, 3.8, 3.8])
ram_offload = np.array([0.0, 1.4, 1.0])
overhead_extra = np.array([0.0, 4.3, 0.4])

x = np.arange(len(categorie))
width = 0.42

ax.bar(x, vram_pesi, width, label='Pesi allocati in VRAM Dedicata (Max 4 GB)', color='#1f77b4', edgecolor='black')
ax.bar(x, ram_offload, width, bottom=vram_pesi, label='Layer Offloading su RAM di Sistema (16 GB)', color='#ff7f0e', edgecolor='black')
ax.bar(x, overhead_extra, width, bottom=vram_pesi + ram_offload,
       label='Overhead PLE / Proiettori Multimodali / Cache', color='#d62728', alpha=0.75, edgecolor='black', hatch='//')

ax.axhline(4.0, color='black', linestyle='--', linewidth=1.6, label='Limite Fisico VRAM RTX 3050 Ti (4.0 GB)')
ax.set_ylabel('Occupazione di Memoria (GB)')
ax.set_xticks(x)
ax.set_xticklabels(categorie)
ax.set_ylim(0, 14.2)
ax.legend(loc='upper left', framealpha=0.95)

tot_mem = vram_pesi + ram_offload + overhead_extra
note_mem = ['2.4 GB\n(Zero Offload)', '5.0 - 9.5 GB\n(Solo 4.5B attivi)', '4.8 - 5.2 GB\n(8.2B 100% attivi)']
for i, tot in enumerate(tot_mem):
    ax.annotate(note_mem[i], xy=(x[i], tot), xytext=(0, 5),
                textcoords="offset points", ha='center', va='bottom', fontsize=9.2, fontweight='bold')

plt.tight_layout()
plt.savefig('fig_2_2_vram_alloc.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 2. FIGURA 3.4: Meccanismo di Prefix Caching sulla KV Cache (Zero sovrapposizioni)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.5, 3.6))
ax.axis('off')
ax.set_xlim(0, 105)
ax.set_ylim(0, 40)

# Turno 1 (y da 26 a 36)
ax.text(1, 31, "Turno 1\n(Cold Prefill):", fontsize=10, fontweight='bold', va='center', ha='left')
r1_sys = patches.FancyBboxPatch((16, 26), 54, 10, boxstyle="round,pad=0.05,rounding_size=0.6",
                                facecolor='#ffd966', edgecolor='black', linewidth=1.4)
r1_usr = patches.FancyBboxPatch((71.5, 26), 16.5, 10, boxstyle="round,pad=0.05,rounding_size=0.6",
                                facecolor='#f4b183', edgecolor='black', linewidth=1.4)
ax.add_patch(r1_sys)
ax.add_patch(r1_usr)
ax.text(43, 31, "storico_messaggi[0]\nSystem Prompt + REGOLE-RETE.md (~5900 tk)\n[Calcolo Tensori KV in VRAM: ~695 tk/s]",
        ha='center', va='center', fontsize=8.8)
ax.text(79.75, 31, "Prompt 1\n(Nuovo Input)", ha='center', va='center', fontsize=8.8)
ax.text(96.5, 31, "TTFT:\n20.10 s", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#c00000')

# Freccia pulita al centro (tra y=25.2 e y=14.8) con testo a fianco non sovrapposto
ax.annotate('', xy=(43, 14.8), xytext=(43, 25.2),
            arrowprops=dict(arrowstyle="->", color='#1e4620', lw=2.2))
ax.text(45, 20.0, "Riutilizzo Tensori in VRAM (0 Ricalcoli)",
        ha='left', va='center', fontsize=9.0, fontweight='bold', color='#1e4620')

# Turno 2..N (y da 4 a 14)
ax.text(1, 9, "Turno 2..N\n(Cache Hit):", fontsize=10, fontweight='bold', va='center', ha='left')
r2_sys = patches.FancyBboxPatch((16, 4), 43, 10, boxstyle="round,pad=0.05,rounding_size=0.6",
                                facecolor='#a9d18e', edgecolor='#1e4620', linewidth=1.8)
r2_hist = patches.FancyBboxPatch((60.5, 4), 13, 10, boxstyle="round,pad=0.05,rounding_size=0.6",
                                 facecolor='#a9d18e', edgecolor='#1e4620', linewidth=1.4)
r2_usr = patches.FancyBboxPatch((75, 4), 13, 10, boxstyle="round,pad=0.05,rounding_size=0.6",
                                facecolor='#f4b183', edgecolor='black', linewidth=1.4)
ax.add_patch(r2_sys)
ax.add_patch(r2_hist)
ax.add_patch(r2_usr)
ax.text(37.5, 9, "storico_messaggi[0] INVARIANTE\n[PREFISSO GIÀ IN KV CACHE]\n[Lettura Istantanea: PPS > 7200 tk/s]",
        ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1e4620')
ax.text(67, 9, "Turno 1..N-1\n(Cached)", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#1e4620')
ax.text(81.5, 9, "Nuovo\nInput", ha='center', va='center', fontsize=8.5)
ax.text(96.5, 9, "TTFT:\n0.84 s", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1e4620')

plt.tight_layout()
plt.savefig('fig_3_4_prefix_caching.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 3. FIGURA 3.5: Sliding Window con Context Pinning (Spaziatura perfetta)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.5, 3.2))
ax.axis('off')
ax.set_xlim(0, 104)
ax.set_ylim(0, 32)

b_pin = patches.FancyBboxPatch((2, 12), 23, 15, boxstyle="round,pad=0.05,rounding_size=0.7",
                               facecolor='#b4c7e7', edgecolor='#1f4e79', linewidth=1.8)
ax.add_patch(b_pin)
ax.text(13.5, 19.5, "storico_messaggi[0]\n[PINNED IN CIMA]\nSystem Prompt +\nREGOLE-RETE.md",
        ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1f4e79')

# Segno + ben distanziato (tra x=25 e x=34)
ax.text(29.5, 19.5, "+", ha='center', va='center', fontsize=18, fontweight='bold')

b_del = patches.FancyBboxPatch((34, 12), 22, 15, boxstyle="round,pad=0.05,rounding_size=0.7",
                               facecolor='#f8cecc', edgecolor='#b85450', linewidth=1.5, linestyle='--')
ax.add_patch(b_del)
ax.text(45, 19.5, "Messaggi [1 .. k]\n(Cronologia Remota)\n[SCARTATI (FIFO)]\nPreviene Overflow",
        ha='center', va='center', fontsize=8.5, color='#900000')

# Freccia ben distanziata (tra x=56 e x=66)
ax.annotate('', xy=(64.5, 19.5), xytext=(57.5, 19.5),
            arrowprops=dict(arrowstyle="->", color='black', lw=2.0))

b_keep = patches.FancyBboxPatch((66, 12), 36, 15, boxstyle="round,pad=0.05,rounding_size=0.7",
                                facecolor='#d5e8d4', edgecolor='#274e13', linewidth=1.8)
ax.add_patch(b_keep)
ax.text(84, 19.5, "storico_messaggi[-24:]\n[FINESTRA SCORREVOLE ATTIVA]\nUltimi 24 messaggi recenti\n(User Prompt, Tool Calls, STDOUT)",
        ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1e4620')

ax.text(52, 4.5, "Formula di Pruning:  storico_messaggi = [storico_messaggi[0]] + storico_messaggi[-24:]",
        ha='center', va='center', fontsize=9.5, family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#f2f2f2', edgecolor='gray'))

plt.tight_layout()
plt.savefig('fig_3_5_sliding_window.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 4. FIGURA 4.3: Pipeline del Generatore Python (yield) per Analisi Batch
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.8, 3.4))
ax.axis('off')
ax.set_xlim(0, 106)
ax.set_ylim(0, 34)

boxes = [
    (2, 14, 17, 15, '#ededed', '1. Input File\ncompito.txt\n(Formato GIFT\n27 Quesiti)'),
    (23, 14, 19, 15, '#dae8fc', '2. Regex Parser\nre.split() blocchi\nEstrae {=sol#OK}\nPulisce indici'),
    (46, 14, 18, 15, '#fff2cc', '3. Generatore\nyield (Lazy)\nSospende stato\nO(1) in RAM'),
    (68, 14, 19, 15, '#d5e8d4', '4. Call Stateless\nmessaggi_temp\n(2050 tk fissi)\nTool Disabilitati'),
    (91, 14, 13, 15, '#f8cecc', '5. Reset\ndel / GC\nDistrugge\ncontesto')
]

for (bx, by, bw, bh, col, txt) in boxes:
    patch = patches.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.05,rounding_size=0.6",
                                   facecolor=col, edgecolor='black', linewidth=1.4)
    ax.add_patch(patch)
    ax.text(bx + bw/2, by + bh/2, txt, ha='center', va='center', fontsize=8.6, fontweight='bold')

arrows = [(19.4, 22.6), (42.4, 45.6), (64.4, 67.6), (87.4, 90.6)]
for (x1, x2) in arrows:
    ax.annotate('', xy=(x2, 21.5), xytext=(x1, 21.5), arrowprops=dict(arrowstyle="->", color='black', lw=1.8))

# Linea ortogonale inferiore pulita
ax.plot([97.5, 97.5, 55.0], [13.6, 6.0, 6.0], color='#1f4e79', linewidth=1.8)
ax.annotate('', xy=(55.0, 13.6), xytext=(55.0, 6.0),
            arrowprops=dict(arrowstyle="->", color='#1f4e79', lw=1.8))
ax.text(76.2, 2.5, "Iterazione sul quesito successivo (i + 1) con memoria conversazionale azzerata",
        ha='center', va='center', fontsize=9, style='italic', fontweight='bold', color='#1f4e79')

plt.tight_layout()
plt.savefig('fig_4_3_pipeline_yield.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 5. FIGURA 5.1: Timeline Fisica di una Transazione di Inferenza Ollama
# ==============================================================================
fig, ax = plt.subplots(figsize=(10.2, 3.3))
ax.axis('off')
ax.set_xlim(0, 100)
ax.set_ylim(0, 36)

s1 = patches.Rectangle((5, 16), 18, 9, facecolor='#d9b38c', edgecolor='black', linewidth=1.4)
s2 = patches.Rectangle((23, 16), 26, 9, facecolor='#9dc3e6', edgecolor='black', linewidth=1.4)
s3 = patches.Rectangle((49, 16), 46, 9, facecolor='#a9d18e', edgecolor='black', linewidth=1.4)
ax.add_patch(s1)
ax.add_patch(s2)
ax.add_patch(s3)

ax.text(14, 20.5, "1. load_duration\n(VRAM Cold Start)", ha='center', va='center', fontsize=8.8, fontweight='bold')
ax.text(36, 20.5, "2. prompt_eval_duration\nFase di Prefill (PPS - Parallela)", ha='center', va='center', fontsize=8.8, fontweight='bold')
ax.text(72, 20.5, "3. eval_duration\nFase di Decode Autoregressiva (TPS - Seriale)", ha='center', va='center', fontsize=8.8, fontweight='bold')

ax.annotate('Emissione 1° Token\n(Istante TTFT)', xy=(49, 25.2), xytext=(49, 32.5),
            ha='center', va='center', fontsize=9, fontweight='bold', color='#c00000',
            arrowprops=dict(arrowstyle="->", color='#c00000', lw=2))

ax.annotate('', xy=(5, 12.0), xytext=(49, 12.0), arrowprops=dict(arrowstyle="<->", color='#c00000', lw=1.8))
ax.text(27, 8.8, "TTFT = load_duration + prompt_eval_duration", ha='center', va='center', fontsize=9, fontweight='bold', color='#c00000')

ax.annotate('', xy=(5, 4.2), xytext=(95, 4.2), arrowprops=dict(arrowstyle="<->", color='black', lw=1.6))
ax.text(50, 1.2, "total_duration (Latenza complessiva End-to-End della chiamata HTTP)", ha='center', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('fig_5_1_timeline_metriche.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 6. FIGURA 5.2: Effetto di Temperature e Top-p sulla distribuzione Softmax
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.0))

tokens_cand = ['ip addr', 'ip route', 'cat', 'ifconfig', 'netstat', 'switch0', 'vlan1']
logits = np.array([4.2, 3.8, 3.1, 2.4, 2.0, 1.5, 1.1])
x = np.arange(len(tokens_cand))

p_a = np.exp(logits / 0.8) / np.sum(np.exp(logits / 0.8))
colors_a = ['#d62728' if i < 5 else '#cccccc' for i in range(len(tokens_cand))]
ax1.bar(x, p_a * 100, color=colors_a, edgecolor='black', width=0.55)
ax1.set_xticks(x)
ax1.set_xticklabels(tokens_cand, rotation=20)
ax1.set_ylabel('Probabilità del Token P(w) [%]')
#ax1.set_title('Profilo A (T = 0.8, Top-p = 0.9) — Alta Entropia', pad=8, fontweight='bold')
ax1.set_ylim(0, 62)
for i, v in enumerate(p_a * 100):
    ax1.text(i, v + 1.5, f"{v:.1f}%", ha='center', fontsize=8.5, fontweight='bold')

p_c = np.exp(logits / 0.1) / np.sum(np.exp(logits / 0.1))
colors_c = ['#2ca02c' if i == 0 else '#cccccc' for i in range(len(tokens_cand))]
ax2.bar(x, p_c * 100, color=colors_c, edgecolor='black', width=0.55)
ax2.set_xticks(x)
ax2.set_xticklabels(tokens_cand, rotation=20)
ax2.set_ylabel('Probabilità del Token P(w) [%]')
#ax2.set_title('Profilo C (T = 0.1, Top-p = 0.5) — Quasi-Greedy', pad=8, fontweight='bold')
ax2.set_ylim(0, 114)
for i, v in enumerate(p_c * 100):
    ax2.text(i, v + 2.2, f"{v:.1f}%", ha='center', fontsize=8.5, fontweight='bold')

plt.tight_layout()
plt.savefig('fig_5_2_softmax_sampling.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 7. FIGURA 5.4: Topologia del Laboratorio Kathará di Benchmark (Senza titolo)
# ==============================================================================
fig, ax = plt.subplots(figsize=(11, 6.2))
ax.axis('off')
ax.set_xlim(0, 104)
ax.set_ylim(0, 66)

pos = {
    'r1': (28, 47), 'r2': (76, 47),
    'r3': (22, 23), 'r4': (52, 33), 'r5': (82, 23),
    'pc1': (9, 58),  'pc2': (95, 58),
    'pc3': (7, 9),   'pc4': (52, 9),
    'pc5': (75, 6),  'pc6': (95, 9),
    'ws':  (52, 59)
}

links = [
    ('r1', 'pc1', 'A1 (100.0.5.0/24)', (17.5, 53.5)),
    ('r2', 'pc2', 'A2 (200.0.8.0/24)', (86.5, 53.5)),
    ('r3', 'pc3', 'A3', (14.5, 16.0)),
    ('r4', 'pc4', 'A4', (52.0, 21.0)),
    ('r5', 'pc5', 'A5 (LAN IPv6)', (83.0, 14.0)),
    ('r5', 'pc6', '', (0, 0)),
    ('r1', 'r2', 'B5 (10.0.7.0/30)', (52.0, 47.0)),
    ('r1', 'r3', 'B1 (10.0.8.0/30)', (24.8, 35.0)),
    ('r1', 'r4', 'B2 (10.0.1.0/30)', (39.5, 40.2)),
    ('r2', 'r4', 'B4', (64.5, 40.2)),
    ('r2', 'r5', 'B3', (79.2, 35.0)),
    ('r3', 'r4', 'B6', (37.0, 28.0)),
    ('r4', 'r5', 'B7 (10.0.3.0/30)', (67.0, 28.0))
]

for (n1, n2, dom, lpos) in links:
    x1, y1 = pos[n1]
    x2, y2 = pos[n2]
    is_lan = n2.startswith('pc')
    col = '#1f77b4' if is_lan else '#d62728'
    ls = '-' if is_lan else '--'
    ax.plot([x1, x2], [y1, y2], color=col, linestyle=ls, linewidth=2.0, zorder=1)
    if dom:
        ax.text(lpos[0], lpos[1], dom, ha='center', va='center', fontsize=8.0, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.22', facecolor='white', edgecolor=col, lw=1.1), zorder=3)

for node, (nx, ny) in pos.items():
    if node.startswith('r'):
        circ = patches.Circle((nx, ny), radius=3.8, facecolor='#ffe599', edgecolor='black', linewidth=1.8, zorder=4)
        ax.add_patch(circ)
        ax.text(nx, ny, node.upper(), ha='center', va='center', fontsize=10, fontweight='bold', zorder=5)
    elif node == 'ws':
        rect = patches.FancyBboxPatch((nx-6.5, ny-2.8), 13.0, 5.6, boxstyle="round,pad=0.05,rounding_size=0.4",
                                      facecolor='#e2efda', edgecolor='#274e13', linewidth=1.5, linestyle='--', zorder=4)
        ax.add_patch(rect)
        ax.text(nx, ny, "wireshark\n(Nodo Sniffing)", ha='center', va='center', fontsize=8.0, fontweight='bold', color='#1e4620', zorder=5)
    else:
        rect = patches.FancyBboxPatch((nx-4.6, ny-2.8), 9.2, 5.6, boxstyle="round,pad=0.05,rounding_size=0.4",
                                      facecolor='#b4c7e7', edgecolor='black', linewidth=1.5, zorder=4)
        ax.add_patch(rect)
        sub = "\n(BIND9)" if node in ['pc1', 'pc3', 'pc4'] else ("\n(Apache2)" if node == 'pc2' else "\n(Host IPv6)")
        ax.text(nx, ny, f"{node}{sub}", ha='center', va='center', fontsize=8.0, fontweight='bold', zorder=5)

ax.plot([], [], color='#1f77b4', linestyle='-', linewidth=2, label='Domini di Collisione LAN Host (A1 - A5)')
ax.plot([], [], color='#d62728', linestyle='--', linewidth=2, label='Dorsali Point-to-Point /30 tra Router (B1 - B7)')
ax.legend(loc='lower left', frameon=True, framealpha=0.95, fontsize=8.8)

plt.tight_layout()
plt.savefig('fig_5_4_topologia_lab.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# 8. FIGURA 5.5: Dinamica Bifase del Prefix Caching (Zero sovrapposizioni!)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.2))

turni_c = np.arange(1, 13)
pps_c = [695.0, 7258.9, 7452.6, 2880.7, 686.4, 2019.5, 660.3, 675.5, 690.6, 674.8, 684.0, 677.5]
ttft_c = [20.10, 0.87, 0.84, 2.67, 11.16, 4.06, 12.24, 11.16, 10.95, 12.08, 11.92, 12.08]

ax1.plot(turni_c, pps_c, marker='o', linewidth=2.2, color='#1f77b4', label='PPS - Velocità Lettura Prompt (tk/s)')
ax1.axvspan(1.8, 4.2, color='#2ca02c', alpha=0.15, label='Fase 1: Cache Hit Pieno (>7200 tk/s)')
ax1.axvspan(4.8, 12.2, color='#ff7f0e', alpha=0.12, label='Fase 2: Saturazione 8192 tk (Ricalcolo)')
ax1.set_xlabel('Turno di Interazione (SKILL_C)')
ax1.set_ylabel('Prompt Processing Speed - PPS (tk/s)')
#ax1.set_title('Efficienza del Prefix Caching sulla PPS', pad=8, fontweight='bold')
ax1.set_xticks(turni_c)
# Alzato a 10800 così la legenda in alto a destra non tocca né i punti né le bande
ax1.set_ylim(0, 10800)
ax1.legend(loc='upper right', fontsize=8.4, framealpha=0.95)

ax2.plot(turni_c, ttft_c, marker='s', linewidth=2.2, color='#d62728', label='TTFT - Time To First Token (s)')
ax2.annotate('Cold Start\n(20.10 s)', xy=(1, 20.10), xytext=(2.3, 19.2),
             arrowprops=dict(arrowstyle="->", color='black', lw=1.5),
             ha='left', va='center', fontsize=8.8, fontweight='bold')
# Posizionato in alto al centro (x=3.5, y=15.0) nello spazio completamente bianco: la freccia scende dritta su (3, 0.84) senza toccare nessuna linea!
ax2.annotate('Cache Hit\n(0.84 s)', xy=(3, 1.1), xytext=(3.0, 15.0),
             arrowprops=dict(arrowstyle="->", color='#1e4620', lw=1.8),
             ha='center', va='center', fontsize=8.8, fontweight='bold', color='#1e4620',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#e2efda', edgecolor='#1e4620', lw=1.0))
ax2.set_xlabel('Turno di Interazione (SKILL_C)')
ax2.set_ylabel('Latenza di Innesco - TTFT (s)')
#ax2.set_title('Andamento del TTFT lungo i 12 Turni', pad=8, fontweight='bold')
ax2.set_xticks(turni_c)
ax2.set_ylim(0, 24.5)
ax2.legend(loc='upper right', fontsize=8.6, framealpha=0.95)

plt.tight_layout()
plt.savefig('fig_5_5_pps_cache_hit.pdf', bbox_inches='tight')
plt.close()

print("Tutte le 8 figure sono state rigenerate senza titoli ridondanti e senza sovrapposizioni!")