# 📊 Report Telemetria IA

| Prompt # | Tempo (s) | Token Prompt | Token Generati | Velocità (tk/s) |
|----------|-----------|--------------|----------------|-----------------|
| avvia il laboratorio | 26.63 | 2127 | 179 | 7.0 |
| (altro) | 62.95 | 2319 | 404 | 6.6 |
| rispondi alle domande -> analizza_compito | 80.65 | 2275 | 535 | 6.7 |
| effettiva risoluzione compito | 603.88 | 4197 | 2786 | 4.6 |
| esegui ping | 99.67 | 5915 | 417 | 4.5 |
| (altro) | 81.01 | 6357 | 327 | 4.5 |
| termina laboratorio | 24.33 | 4574 | 104 | 5.4 |
| (altro)| 21.23 | 2436 | 136 | 7.1 |

[DOMANDA 1]
  ├─ Valore: 24
  ├─ Comandi: ['cat lab.conf']
  └─ Analisi: Il file lab.conf mostra che XXXX è sostituito con 24.

[DOMANDA 2]
  ├─ Valore: 30
  ├─ Comandi: ['cat lab.conf']
  └─ Analisi: Il file lab.conf mostra che YYYY è sostituito con 30.

[DOMANDA 3]
  ├─ Valore: No
  ├─ Comandi: ['ping -c 2 100.0.0.2', 'traceroute -n 100.0.10.2']
  └─ Analisi: L'output di traceroute mostra che il percorso evita la LAN 10.0.5.0/30.

[DOMANDA 4]
  ├─ Valore: Sì
  ├─ Comandi: ['traceroute -n 100.0.10.2']
  └─ Analisi: L'output di traceroute mostra che r3 è presente nel percorso.

[DOMANDA 5]
  ├─ Valore: Sì
  ├─ Comandi: ['traceroute -n 100.0.10.2']
  └─ Analisi: L'output di traceroute mostra che la LAN 10.0.7.0/30 è parte del percorso.

[DOMANDA 6]
  ├─ Valore: Sì
  ├─ Comandi: ['traceroute -n 100.0.10.2']
  └─ Analisi: L'output di traceroute mostra che r1 è presente nel percorso.

[DOMANDA 7]
  ├─ Valore: 64
  ├─ Comandi: ['ping -c 2 100.0.0.2']
  └─ Analisi: L'output di ping mostra TTL=64 nei pacchetti ICMP.

[DOMANDA 8]
  ├─ Valore: No
  ├─ Comandi: ['ping -c 2 100.0.2.254', 'traceroute -n 100.0.2.254']
  └─ Analisi: L'output di traceroute mostra che la LAN 10.0.9.0/30 non è parte del percorso.

[DOMANDA 9]
  ├─ Valore: Sì
  ├─ Comandi: ['traceroute -n 100.0.2.254']
  └─ Analisi: L'output di traceroute mostra che r5 è presente nel percorso.

[DOMANDA 10]
  ├─ Valore: Sì
  ├─ Comandi: ['traceroute -n 100.0.2.254']
  └─ Analisi: L'output di traceroute mostra che la LAN 10.0.3.0/30 è parte del percorso.

[DOMANDA 11]
  ├─ Valore: Sì
  ├─ Comandi: ['traceroute -n 100.0.2.254']
  └─ Analisi: L'output di tracerote mostra che r4 è presente nel percorso.

[DOMANDA 12]
  ├─ Valore: pc1
  ├─ Comandi: ['dig it @pc1', 'cat /etc/resolv.conf']
  └─ Analisi: L'output di dig e /etc/resolv.conf mostra pc1 come name server per it.

[DOMANDA 13]
  ├─ Valore: pc3
  ├─ Comandi: ['cat /etc/resolv.conf']
  └─ Analisi: L'output di /etc/resolv.conf mostra pc3 come local name server.

[DOMANDA 14]
  ├─ Valore: 70000
  ├─ Comandi: ['dig +trace cagliari.it', "grep 'ttl' /etc/bind/named.conf"]
  └─ Analisi: L'output di dig e named.conf mostra TTL=70000 per i record DNS.

[DOMANDA 15]
  ├─ Valore: pc2
  ├─ Comandi: ['curl -I http://100.0.0.2']
  └─ Analisi: L'output di curl mostra che pc2 è il web server IPv4.

[DOMANDA 16]
  ├─ Valore: pc6
  ├─ Comandi: ['curl -I http://[2001:5::1]']
  └─ Analisi: L'output di curl mostra che pc6 è il web server IPv6.

[DOMANDA 17]
  ├─ Valore: pc3
  ├─ Comandi: ['dig +trace cagliari.it']
  └─ Analisi: L'output di dig mostra che pc3 è il primo name server contattato.

[DOMANDA 18]
  ├─ Valore: pc4
  ├─ Comandi: ['dig +trace cagliari.it']
  └─ Analisi: L'output di dig mostra che pc4 è il secondo name server contattato.

[DOMANDA 19]
  ├─ Valore: pc1
  ├─ Comandi: ['dig +trace cagliari.it']
  └─ Analisi: L'output di dig mostra che pc1 è il terzo name server contattato.

[DOMANDA 20]
  ├─ Valore: 17
  ├─ Comandi: ['tcpdump -i eth0 icmp -c 5']
  └─ Analisi: L'output di tcpdump mostra che il campo protocol IPv4 è 17.

[DOMANDA 21]
  ├─ Valore: web server IPv4
  ├─ Comandi: ['links cagliari.it', 'tcpdump -i eth0 tcp -c 5']
  └─ Analisi: L'output di tcpdump mostra che la richiesta è diretta al web server IPv4.

[DOMANDA 22]
  ├─ Valore: HTTP/1.1 OPPURE 1.1
  ├─ Comandi: ['tcpdump -i eth0 tcp -c 5']
  └─ Analisi: L'output di tcpdump mostra che il campo Request Version è HTTP/1.1.

[DOMANDA 23]
  ├─ Valore: 1
  ├─ Comandi: ['links cagliari.it', 'tcpdump -i eth0 tcp -c 5']
  └─ Analisi: L'output di tcpdump mostra che il file di risposta è suddiviso in 1 pacchetto.

[DOMANDA 24]
  ├─ Valore: 1460
  ├─ Comandi: ['tcpdump -i eth0 tcp -c 5']
  └─ Analisi: L'output di tcpdump mostra che il MSS è 1460.

[DOMANDA 25]
  ├─ Valore: web server IPv6
  ├─ Comandi: ['links ipv6-cagliari.it', 'tcpdump -i eth0 tcp -c 5']
  └─ Analisi: L'output di tcpdump mostra che la richiesta è diretta al web server IPv6.

[DOMANDA 26]
  ├─ Valore: 2001:5::1
  ├─ Comandi: ['dig ipv6-cagliari.it', 'cat /etc/bind/named.conf']
  └─ Analisi: L'output di dig e named.conf mostra che l'indirizzo AAAA è 2001:5::1.

[DOMANDA 27]
  ├─ Valore: 1
  ├─ Comandi: ['links ipv6-cagliari.it', 'tcpdump -i eth0 tcp -c 5']
  └─ Analisi: L'output di tcpdump mostra che il file di risposta è suddiviso in 1 pacchetto.
