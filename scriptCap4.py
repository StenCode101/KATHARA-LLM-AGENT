import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10.0,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.0,
    "legend.fontsize": 8.8,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5
})

# ==============================================================================
# 4. FIGURA 4.4: Curva ad "U" Lost in the Middle vs Isolamento Stateless (Corretta!)
# ==============================================================================
fig, ax = plt.subplots(figsize=(9.5, 4.3))
ax.grid(True, linestyle='--', alpha=0.3)

q = np.arange(1, 28)
# Curva a U tipica del fenomeno Lost in the Middle nel Bulk Prompting
acc_bulk = 32 + 63 * ((q - 14.0) / 13.0) ** 2
acc_bulk = np.clip(acc_bulk, 30, 95)
# Stabilità dell'approccio Iterative Prompting via yield
acc_yield = np.full_like(q, 98.5, dtype=float)

ax.plot(q, acc_yield, marker='o', markersize=4.8, linewidth=2.3, color='#1f77b4',
        label='Iterative Prompting Stateless con yield (Attenzione Costante ~100%)')
ax.plot(q, acc_bulk, marker='x', markersize=5.2, linestyle='--', linewidth=2.1, color='#d62728',
        label='Bulk Prompting Monolitico (Curva a "U" — Fenomeno Lost in the Middle)')

ax.axvspan(7, 21, color='#d62728', alpha=0.09,
           label='Fascia Centrale di Degrado Cognitivo e Omissione Regole (Quesiti 7–21)')

ax.set_xlabel('Indice Progressivo del Quesito nel Compito d\'Esame (27 Domande Totali)')
ax.set_ylabel('Capacità di Attenzione / Accuratezza [%]')
ax.set_xticks(np.arange(1, 28, 2))

# Tetto alzato a 138 per ospitare la legenda sopra quota 100% senza mai toccare le linee!
ax.set_ylim(15, 138)
ax.set_yticks([20, 40, 60, 80, 100])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0.99), frameon=True, framealpha=0.96, fontsize=8.6)

# Box annotazione ben centrato nella conca della U senza toccare i punti rossi
ax.annotate('Minimo di Attenzione\n(Troncamenti e Allucinazioni)', xy=(14, 33.5), xytext=(14, 62),
            ha='center', va='center', fontsize=8.6, fontweight='bold', color='#900000',
            arrowprops=dict(arrowstyle="->", color='#900000', lw=1.8),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fcf2f2', edgecolor='#900000', lw=1.2))

plt.tight_layout()
plt.savefig('fig_4_4_lost_in_the_middle.pdf', bbox_inches='tight')
plt.close()

print("Figura 4.4 rigenerata senza alcuna sovrapposizione!")