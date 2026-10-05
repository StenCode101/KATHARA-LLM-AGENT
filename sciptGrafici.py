import matplotlib.pyplot as plt
import numpy as np

# Configurazione stile accademico compatibile con LaTeX
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "legend.fontsize": 9.2,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--"
})

# ==============================================================================
# GRAFICO 1: Confronto num_ctx (2048 vs 8192 vs 16384) - TPS e Latenza
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

steps = ['Step 1\n(pc1.startup)', 'Step 2\n(lab.conf)', 'Step 3\n(Risposta A1)']
x = np.arange(len(steps))
width = 0.26

tps_2048 = [8.5, 0, 0]
tps_8192 = [4.5, 4.4, 4.0]
tps_16384 = [3.8, 3.6, 3.4]

rects0 = ax1.bar(x[0] - width, tps_2048[0], width, label='num_ctx = 2048 (Troncato/Loop)', color='#d62728', edgecolor='black')
rects1 = ax1.bar(x, tps_8192, width, label='num_ctx = 8192 (Sweet Spot)', color='#1f77b4', edgecolor='black')
rects2 = ax1.bar(x + width, tps_16384, width, label='num_ctx = 16384 (VRAM Offload)', color='#ff7f0e', edgecolor='black')

ax1.set_ylabel('Velocità di Scrittura - TPS (tk/s)')
ax1.set_title('Confronto TPS al variare di num_ctx', pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(steps)
ax1.set_ylim(0, 10.5)
ax1.legend(loc='upper right', framealpha=0.95)

for rect in list(rects0) + list(rects1) + list(rects2):
    h = rect.get_height()
    if h > 0:
        ax1.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

time_2048 = [45.23, 0, 0]
time_8192 = [61.60, 80.83, 104.93]
time_16384 = [109.22, 103.68, 69.86]

rects3 = ax2.bar(x[0] - width, time_2048[0], width, label='num_ctx = 2048 (Abortito: 45.2s)', color='#d62728', edgecolor='black')
rects4 = ax2.bar(x, time_8192, width, label='num_ctx = 8192 (Tot: 247.4s)', color='#1f77b4', edgecolor='black')
rects5 = ax2.bar(x + width, time_16384, width, label='num_ctx = 16384 (Tot: 282.8s)', color='#ff7f0e', edgecolor='black')

ax2.set_ylabel('Latenza Totale di Step (s)')
ax2.set_title('Latenza per Step del Ciclo ReAct', pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(steps)
# Alzato a 152 così la legenda in alto non copre mai 109.2s e 103.7s
ax2.set_ylim(0, 152)
ax2.legend(loc='upper right', framealpha=0.95)

for rect in list(rects3) + list(rects4) + list(rects5):
    h = rect.get_height()
    if h > 0:
        ax2.annotate(f'{h:.1f}s', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5)

plt.tight_layout()
plt.savefig('grafico_1_num_ctx.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# GRAFICO 2: Correlazione KV Cache (Token Prompt) vs TPS (No_Skill_A vs SKILL_C)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

turni_noskill = np.arange(1, 14)
prompt_noskill = [973, 1156, 1183, 1622, 2418, 2174, 2678, 3059, 2885, 3703, 4128, 4067, 4571]
tps_noskill = [9.1, 8.5, 7.4, 7.4, 6.6, 6.9, 6.6, 5.7, 6.3, 5.4, 5.0, 5.2, 5.0]

turni_skillc = np.arange(1, 13)
prompt_skillc = [5913, 6161, 6183, 7666, 7654, 8188, 8077, 7533, 7551, 8141, 8145, 8181]
tps_skillc = [4.8, 4.5, 4.5, 4.1, 3.9, 4.3, 4.2, 4.2, 4.1, 4.3, 4.3, 4.3]

ax1.plot(turni_noskill, prompt_noskill, marker='o', linewidth=2, label='No_Skill_A (Acc: 40%)', color='#d62728')
ax1.plot(turni_skillc, prompt_skillc, marker='s', linewidth=2, label='SKILL_C (Acc: 100%)', color='#2ca02c')
ax1.axhline(8192, color='black', linestyle=':', linewidth=1.2, label='Soglia num_ctx (8192 tk)')
ax1.set_xlabel('Turno di Interazione (Chiamata HTTP)')
ax1.set_ylabel('Dimensione Contesto in Ingresso (Token)')
ax1.set_title('Occupazione della Context Window per Turno', pad=10)
ax1.set_ylim(0, 9200)
# Posizionata nella zona libera tra le due curve a sinistra (turni 1-5, 3200-5600 tk)
ax1.legend(loc='center left', bbox_to_anchor=(0.02, 0.48), framealpha=0.95)

ax2.plot(turni_noskill, tps_noskill, marker='o', linewidth=2, label='No_Skill_A (Media: 6.55 tk/s)', color='#d62728')
ax2.plot(turni_skillc, tps_skillc, marker='s', linewidth=2, label='SKILL_C (Media: 4.29 tk/s)', color='#2ca02c')
ax2.set_xlabel('Turno di Interazione (Chiamata HTTP)')
ax2.set_ylabel('Velocità di Generazione - TPS (tk/s)')
ax2.set_title('Impatto dell\'Ampiezza KV Cache sui TPS', pad=10)
ax2.set_ylim(2, 10.2)
ax2.legend(loc='upper right', framealpha=0.95)

plt.tight_layout()
plt.savefig('grafico_2_ablation_kvcache.pdf', bbox_inches='tight')
plt.close()

# ==============================================================================
# GRAFICO 3: Scalabilità Batch Analizza (9 Blocchi Reali B1-B9)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

blocchi = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9']
prompt_stateless = [2050] * 9
gen_tokens = [1925, 1740, 1323, 1872, 1383, 1616, 1705, 1632, 1386]
prompt_cumulativo = [2050 + sum(gen_tokens[:i]) for i in range(9)]

ax1.plot(blocchi, prompt_cumulativo, marker='x', linestyle='--', linewidth=2, color='#d62728', label='Senza Generatore (Cumulativo)')
ax1.plot(blocchi, prompt_stateless, marker='o', linewidth=2.5, color='#1f77b4', label='Con Generatore yield (2050 tk fissi)')
ax1.axhline(8192, color='black', linestyle=':', linewidth=1.2, label='Limite num_ctx (8192 tk)')
ax1.fill_between(blocchi, 8192, 17500, color='#d62728', alpha=0.1, label='Zona di Context Overflow')
ax1.set_xlabel('Blocco Quesiti d\'Esame (compito.txt)')
ax1.set_ylabel('Token nel Contesto (Prompt)')
ax1.set_title('Prevenzione del Context Overflow con yield', pad=10)
ax1.set_ylim(0, 17500)
ax1.legend(loc='upper left', fontsize=8.5, framealpha=0.95)

ttft_batch = [16.87, 2.78, 2.89, 2.74, 3.38, 3.38, 3.33, 3.38, 0.67]
load_batch = [13.91, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

ax2.plot(blocchi, ttft_batch, marker='s', linewidth=2, color='#9467bd', label='TTFT Totale (s)')
ax2.bar(blocchi, load_batch, width=0.4, alpha=0.5, color='#8c564b', label='Di cui Load in VRAM (Cold Start)')
ax2.set_xlabel('Blocco Quesiti d\'Esame (compito.txt)')
ax2.set_ylabel('Tempo di Latenza (s)')
ax2.set_title('Abbattimento del TTFT dopo il Cold Start (B1)', pad=10)
ax2.set_ylim(0, 19)
ax2.legend(loc='upper right', framealpha=0.95)

plt.tight_layout()
plt.savefig('grafico_3_batch_analizza.pdf', bbox_inches='tight')
plt.close()

print("Grafici aggiornati senza sovrapposizioni!")