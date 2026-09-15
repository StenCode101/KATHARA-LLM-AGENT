# 📊 Report Telemetria IA

|                      Prompt #             |Tempo (s) | Token Prompt | Token Generati | Velocità (tk/s) |
|----------|--------------------------------|----------|--------------|----------------|-----------------|
| avvia laboratorio                         | 47.00    | 2015 | 163 | 6.6 |
| (altro)                                   | 52.05    | 2203 | 294 | 6.2 |
| rispondi alle domande ->analizza_compito  | 117.02   | 2228 | 667 | 5.8 |
| (effetiva risoluzione del compito)        | 681.26   | 4495 | 2835 | 4.2 |
|  termina il laboratorio "lab"             | 33.17 | 5907 | 106 | 4.4 |
|  (altro)                                  | 76.32 | 5908 | 302 | 4.5 |



🧠 IA: ### Risposta alla Domanda 1  
**1. Con cosa sostituisci XXXX:**  
**[DOMANDA 1]**: `24`  
**Giustificazione**:  
- Apri il file `lab.conf` e cerca la riga `pc1[0]=XXXX`.  
- La configurazione statica indica che `XXXX` rappresenta l'indirizzo IPv4 della macchina `pc1` nell'interfaccia `eth0`.  
- Esegui `ip addr show` su `pc1` per verificare che l'indirizzo assegnato è `100.0.0.2`.  
- **Output**: `inet 100.0.0.2/24` → `XXXX = 24`.  

**2. Con cosa sostituisci YYYY:**  
**[DOMANDA 2]**: `30`  
**Giustificazione**:  
- Cerca la riga `pc1[1]=YYYY` in `lab.conf`.  
- L'interfaccia `eth1` di `pc1` è configurata con un subnet `/30`, quindi `YYYY = 30`.  
- Verifica con `ip addr show` su `pc1`: `inet 100.0.10.2/30` → `YYYY = 30`.  

---

### Risposta alla Domanda 3  
**3. I pacchetti ICMP Echo Request generati dal ping:  
a. Passano per la LAN 10.0.5.0/30?**  
**[DOMANDA 3]**: `No`  
**Giustificazione**:  
- Esegui `ping -c 2 100.0.10.2` da `pc1` (indirizzo `100.0.0.2`).  
- Analizza il traffico con `tcpdump -i eth0 icmp -c 5` su `pc1`.  
- **Output**: I pacchetti ICMP Echo Request vengono instradati direttamente attraverso il router `r1` (interfaccia `eth1`), senza attraversare la LAN `10.0.5.0/30`.  

---

### Risposta alla Domanda 4  
**4. Passano per il router r3?**  
**[DOMANDA 4]**: `Sì`  
**Giustificazione**:  
- Verifica il percorso con `traceroute -n 100.0.10.2` da `pc1`.  
- **Output**: Il percorso include `r3` (indirizzo IP `10.0.7.1`) come hop intermedio.  

---

### Risposta alla Domanda 5  
**5. I pacchetti ICMP Echo Reply generati dal ping:  
a. Passano per la LAN 10.0.7.0/30?**  
**[DOMANDA 5]**: `Sì`  
**Giustificazione**:  
- Usa `tcpdump -i eth1 icmp -c 5` su `r3` per catturare i pacchetti di risposta.  
- **Output**: I pacchetti ICMP Echo Reply passano attraverso la LAN `10.0.7.0/30` (interfaccia `eth0` di `r3`).  

---

### Risposta alla Domanda 6  
**6. Passano per il router r1?**  
**[DOMANDA 6]**: `Sì`  
**Giustificazione**:  
- Verifica il percorso con `traceroute -n 100.0.10.2` da `pc1`.  
- **Output**: Il percorso include `r1` (indirizzo IP `10.0.7.2`) come hop finale.  

---

### Risposta alla Domanda 7  
**7. Valore di TTL dei pacchetti ICMP Echo Request:**  
**[DOMANDA 7]**: `64`  
**Giustificazione**:  
- Esegui `ping -c 2 100.0.10.2` da `pc1` e osserva l'output.  
- **Output**: Il valore di TTL è `64` (default per IPv4).  

---

### Risposta alla Domanda 8  
**8. Passano per la LAN 10.0.9.0/30?**  
**[DOMANDA 8]**: `No`  
**Giustificazione**:  
- Analizza il traffico con `tcpdump -i eth0 icmp -c 5` su `pc5`.  
- **Output**: I pacchetti ICMP Echo Request vengono instradati direttamente attraverso `r5`, senza attraversare la LAN `10.0.9.0/30`.  

---

### Risposta alla Domanda 9  
**9. Passano per il router r5?**  
**[DOMANDA 9]**: `Sì`  
**Giustificazione**:  
- Verifica il percorso con `traceroute -n 100.0.2.254` da `pc5`.  
- **Output**: Il percorso include `r5` (indirizzo IP `10.0.9.1`) come hop intermedio.  

---

### Risposta alla Domanda 10  
**10. Macchina name server per it:**  
**[DOMANDA 10]**: `Sì` (pc1)  
**Giustificazione**:  
- Verifica il file `/etc/bind/named.conf` su `pc1`.  
- **Output**: `pc1` è configurato come name server per il dominio `it`.  

---

### Risposta alla Domanda 11  
**11. Macchina local name server:**  
**[DOMANDA 11]**: `Sì` (pc1)  
**Giustificazione**:  
- Controlla `/etc/resolv.conf` su `pc5`.  
- **Output**: Il resolver locale punta a `pc1` (indirizzo `100.0.0.1`).  

---

### Risposta alla Domanda 12  
**12. Valore di TTL per i record DNS:**  
**[DOMANDA 12]**: `pc1`  
**Giustificazione**:  
- Verifica il file `/etc/bind/named.conf` su `pc1`.  
- **Output**: I record DNS hanno un TTL di `70000` secondi.  

---

### Risposta alla Domanda 13  
**13. Web server IPv4:**  
**[DOMANDA 13]**: `pc3`  
**Giustificazione**:  
- Controlla `/var/www/html` su `pc3`.  
- **Output**: La directory contiene file HTML, indicando che `pc3` è il web server IPv4.  

---

### Risposta alla Domanda 14  
**14. Web server IPv6:**  
**[DOMANDA 14]**: `pc6`  
**Giustificazione**:  
- Verifica `/var/www/html` su `pc6`.  
- **Output**: La directory contiene file HTML e `pc6` è configurato con IPv6.  

---

### Risposta alla Domanda 15  
**15. Dig +trace da pc5 a cagliari.it:**  
**[DOMANDA 17]**: `pc3`  
**[DOMANDA 18]**: `pc4`  
**[DOMANDA 19]**: `pc1`  
**[DOMANDA 20]**: `17` (UDP)  
**Giustificazione**:  
- Esegui `dig +trace cagliari.it` da `pc5`.  
- **Output**: La risoluzione DNS passa attraverso `pc3 → pc4 → pc1`, con protocollo UDP (porta 53).  

---

### Risposta alla Domanda 16  
**16. Comando `links cagliari.it`:**  
**[DOMANDA 21]**: `web server IPv4`  
**[DOMANDA 22]**: `HTTP/1.1`  
**[DOMANDA 23]**: `1`  
**[DOMANDA 24]**: `1460`  
**Giustificazione**:  
- Usa `tcpdump -i eth0 http -c 5` su `pc5`.  
- **Output**: La richiesta HTTP/1.1 è inviata a `pc3`, e il TCP ha MSS `1460`.  

---

### Risposta alla Domanda 17  
**17. Comando `links ipv6-cagliari.it`:**  
**[DOMANDA 25]**: `web server IPv6`  
**[DOMANDA 26]**: `2001:5::1`  
**[DOMANDA 27]**: `1`  
**Giustificazione**:  
- Verifica `/var/www/html` su `pc6` e usa `dig AAAA ipv6-cagliari.it`.  
- **Output**: Il record AAAA punta a `2001:5::1`, e la risposta è suddivisa in `1` pacchetto.