# Upute za instalacije i pokretanje programa

- Potrebno je instalirati instalacijsku skriptu
- Unutar instalacijske skripte nalazi se Python3.10 verzija koju je potrebno promijeniti da verziju Python3.9.
- Promjena Python verzije:
  1. sudo apt update
  2. sudo apt install wget software-properties-common
  3. sudo add-apt-repository ppa:deadsnakes/ppa
  4. sudo apt update
  5. sudo apt install python3.9
  6. Provjera verzije: python3.9 -V ili python3.9 –version
- Nakon toga potrebno preuzeti pip skriptu https://bootstrap.pypa.io/get-pip.py 
  1. python3.9 get-pip.py --user
  2. sudo apt install python3.9-distutils
- Instalacija biblioteke: pip install ProbPy
- Pokretanje programa: 
  1. conda activate base
  2. python nazivPrograma.py
  3. NAPOMENTA: Prvo je potrebno pokrenuti svakog agenta za sebe, a zatim gamemastera
  

# Agenti

NAZIV | JID  | LOZINKA
-------------|------------- | -------------
AGENT1 |kmedenjak_agent1@5222.de  | 12345
AGENT2 |kmedenjak_agent2@5222.de  | 12345 
AGENT3 |kmedenjak_agent3@5222.de  | 12345
AGENT4 |kmedenjak_agent4@5222.de  | 12345 
AGENT6 |kmedenjak_agent5@5222.de  | 12345
AGENT6 |kmedenjak_agent6@5222.de  | 12345 
GAMEMASTER |kmedenjak_igra@5222.de | 12345
