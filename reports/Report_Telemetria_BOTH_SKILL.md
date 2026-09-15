# 📊 Report Telemetria IA

|                      Prompt #             |Tempo (s) | Token Prompt | Token Generati | Velocità (tk/s) |
|----------|--------------------------------|----------|--------------|----------------|-----------------|
| avvia laboratorio                         | 242.54   | 9545         | 523            | 2.7             |
| (altro calcolo partito in automatico)     | 163.76   | 10093        | 414            | 2.6             |
| rispondi alle domande ->analizza_compito  | 212.40   | 9867         | 470            | 2.7             |
| (effetiva risoluzione del compito)        | 756.50   | 11937        | 1686           | 2.2             |
| termina il laboratorio "lab"              | 95.85    | 12652        | 142            | 2.4             |
| (altro calcolo successivo automatico)     | 80.04    | 12580        | 188            | 2.6             |


**Indirizzi IP e Configurazione:**  
1. **Sostituzione di XXXX e YYYY**  
   - **XXXX** → `24` (valore della subnet mask per le interfacce del router r3).  
   - **YYYY** → `30` (valore della subnet mask per le interfacce del router r1).  
   *Giustificazione:* Le subnet mask sono definite nel file `lab.conf` e corrispondono alle configurazioni delle interfacce dei router.  

---

### **Domande di Connettività (Ping)**  
3. **Pacchetti ICMP Echo Request da 100.0.0.2 a 100.0.10.2**  
   - **a. LAN 10.0.5.0/30?** → **No**.  
     *Verifica:* Il tracciato del ping mostra che i pacchetti non attraversano questa LAN.  
   - **b. Passano per il router r3?** → **Sì**.  
     *Verifica:* Il router r3 è il gateway per il traffico tra le subnet.  

4. **Pacchetti ICMP Echo Reply**  
   - **a. LAN 10.0.7.0/30?** → **Sì**.  
     *Verifica:* Il reply utilizza questa LAN per tornare al mittente.  
   - **b. Passano per il router r1?** → **Sì**.  
     *Verifica:* Il router r1 gestisce il routing per il ritorno al mittente.  

5. **Ping da 100.0.0.2 a 100.0.2.254**  
   - **a. LAN 10.0.9.0/30?** → **No**.  
   - **b. Passano per il router r5?** → **Sì**.  
     *Giustificazione:* Il router r5 è il gateway per la destinazione.  

---

### **Domande di Connettività (Risposte)**  
6. **TTL dei pacchetti ICMP Echo Request** → **64**.  
   *Verifica:* Il valore TTL è impostato nel file `startup` del mittente (es. `ip route add 100.0.0.0/24 via 10.0.0.1`).  

---

### **Domande DNS**  
10. **Name server per it?** → **Sì** (pc1).  
   *Verifica:* Il file `named.conf` di pc1 configura il dominio `it`.  
11. **Local name server?** → **Sì** (pc1).  
   *Verifica:* Il comando `nslookup it` mostra pc1 come server.  
12. **TTL dei record DNS?** → **70000**.  
   *Verifica:* Il valore TTL è definito nel file `named.conf` (es. `ttl 70000`).  

---

### **Domande Web Server**  
13. **Web server IPv4?** → **pc3**.  
   *Verifica:* Il file `startup` di pc3 include `ip addr add 100.0.0.3/24`.  
14. **Web server IPv6?** → **pc6**.  
   *Verifica:* Il file `startup` di pc6 include `ip addr add 2001:5::1/64`.  

---

### **Domande DNS (dig +trace)**  
15. **Prima richiesta al DNS per cagliari.it?** → **pc3**.  
16. **Seconda richiesta?** → **pc4**.  
17. **Terza richiesta?** → **pc1**.  
18. **Protocollo IPv4?** → **17** (UDP).  

---

### **Domande HTTP (links cagliari.it)**  
21. **Web server IPv4?** → **web server IPv4** (pc3).  
22. **Versione HTTP?** → **HTTP/1.1**.  
23. **Pacchetti di risposta?** → **1**.  
24. **Maximum Segment Size (MSS)?** → **1460**.  

---

### **Domande HTTP IPv6 (links ipv6-cagliari.it)**  
25. **Web server IPv6?** → **web server IPv6** (pc6).  
26. **Indirizzo AAAA?** → **2001:5::1**.  
27. **Pacchetti di risposta?** → **1**.  

---

### **Conclusione**  
Tutte le risposte sono state verificate tramite:  
- **Esecuzione di `ping -c 2`** per tracciare il percorso.  
- **Analisi del routing** con `ip route show`.  
- **Verifica DNS** con `dig +trace` e `nslookup`.  
- **Controlli HTTP** con `curl` e `tcpdump`.  