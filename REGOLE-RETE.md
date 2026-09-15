# MANUALE OPERATIVO KATHARÁ: REGOLE E COMANDI ESSENZIALI

Questo documento definisce i vincoli operativi e gli strumenti a disposizione per l'analisi dei laboratori di rete Kathará. Devi attenerti strettamente a queste regole per ogni risposta.

- Il file 'lab.conf' definisce SOLO i domini di collisione fisici (es. pc1[0]=A) e le subnet mask associate. NON contiene configurazioni di Web Server, DNS Server, IP statici o protocolli.
- I demoni e i servizi (Web Server, DNS) si attivano nei file '.startup' o si verificano interrogando direttamente le macchine (es. con curl, dig).
- Numeri dei Protocolli di Rete (fondamentale per tcpdump): ICMP = 1, TCP = 6, UDP = 17, IPv6-ICMP = 58. (Non confondere mai UDP 17 con TCP).
- Il TTL (Time To Live) dei pacchetti di rete si verifica leggendo l'header IP tramite 'ping' o 'tcpdump'. Il TTL dei record DNS si legge dai file di zona (es. /etc/bind/named.conf) o con 'dig'.
- Il comando 'links' è un browser interattivo, non si usa per fare dump dei pacchetti. Per analizzare le richieste HTTP (Request Version, MSS) si usa SEMPRE 'tcpdump' catturando il three-way-handshake TCP (porta 80).
- Le tabelle di routing si verificano rigorosamente usando 'ip route get ' oppure 'traceroute -n'.

## 1. Analisi Statica: Topologia e Servizi
* **Domini di Collisione:** Nel file `lab.conf`, la sintassi `macchina[N]=DOMINIO` definisce la topologia. Esempio: `pc1[0]=A` significa che l'interfaccia `eth0` (indice 0) di `pc1` è fisicamente connessa al dominio di collisione `A`. Usa questa regola per mappare la rete a priori senza eseguire comandi.
* **Percorsi Standard:** Non esplorare il file system alla cieca. Ricorda che:
  * I file di configurazione DNS e le zone di risoluzione si trovano sempre sotto `/etc/bind/`.
  * Le directory radice dei siti Web si trovano tipicamente in `/var/www/html/`.

## 2. Regole di Base del Laboratorio
* **Stato delle Interfacce:** In Kathará, tutte le interfacce di rete assegnate a un dispositivo sono automaticamente attive (`UP`) all'avvio. Non è necessario eseguire comandi come `ip link set dev eth0 up`.
* **Immagini Docker:** I dispositivi si basano su immagini specifiche:
  * `kathara/base`: Contiene strumenti di rete base (`iproute2`, `tcpdump`, `ping`, `curl`, `dig`).
  * `kathara/frr`: Utilizzata per i router, include i demoni di routing dinamico (OSPF, BGP, RIP).
  * `kathara/bind`: Utilizzata per i server DNS.
* **Approccio Ibrido:** Per ogni problema, verifica prima le configurazioni statiche (`lab.conf`, file `.startup`, o `/etc/resolv.conf`), poi conferma obbligatoriamente il comportamento reale eseguendo comandi diagnostici sui terminali.

## 3. Direttive di Comportamento per l'IA
* **Rispetto della Struttura:** Rispondi a una singola domanda alla volta, rispettando rigorosamente la numerazione fornita nel prompt. Non raggruppare mai le risposte.
* **Giustificazione Empirica:** Ogni affermazione teorica deve essere supportata dall'output di un comando reale eseguito sul nodo.
* **Sicurezza dei Comandi:** I laboratori non hanno accesso a Internet. Non tentare di scaricare pacchetti tramite `apt` o `apk`.

## 4. Strumenti di Rete e Sintassi Obbligatoria

### Controllo Indirizzamento e Routing
Usa esclusivamente la suite `iproute2` (abbandona `ifconfig` e `route`).
* Ispezione IPv4/IPv6: `ip addr show`
* Visualizzazione tabelle di routing IPv4: `ip route show`
* Visualizzazione tabelle di routing IPv6: `ip -6 route show`
* Verifica dell'instradamento di un IP specifico: `ip route get <indirizzo_ip>`

### Test di Connettività
* **Ping (REGOLA CRITICA):** Devi sempre limitare il numero di pacchetti ICMP per evitare loop infiniti. Usa la sintassi: `ping -c 2 <indirizzo_ip>` (oppure `ping6 -c 2` per IPv6).
* Tracciamento percorso IPv4: `traceroute -n <indirizzo_ip>`
* Tracciamento percorso IPv6: `traceroute6 -n <indirizzo_ip>`

### Ispezione del Traffico (Packet Sniffing)
* Cattura traffico di base: `tcpdump -i <interfaccia> -n -c 10`
* Filtro per ICMP: `tcpdump -i <interfaccia> icmp -c 5`
* Filtro per DNS (porta 53): `tcpdump -i <interfaccia> udp port 53 -c 5`

### Analisi DNS
* Risoluzione standard: `dig <dominio>`
* Tracciamento completo (root e TLD): `dig +trace <dominio>`
* Ispezione del resolver locale: `cat /etc/resolv.conf`
* Controllo configurazioni server (se immagine bind): `cat /etc/bind/named.conf`

### Verifica Servizi Web
* Test server HTTP IPv4: `curl -I http://<indirizzo_ipv4>`
* Test server HTTP IPv6: `curl -I "http://[<indirizzo_ipv6>]"` (nota le parentesi quadre obbligatorie).