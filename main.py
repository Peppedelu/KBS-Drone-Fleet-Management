
from pyswip import Prolog

prolog = Prolog()
prolog.consult("mappa.pl.txt")

print("--- PONTE PYTHON - PROLOG ATTIVATO ---")

# 1. QUERY SEMPLICE: Verifica deposito

risultato_deposito = list(prolog.query("deposito(deposito_alfa)."))

if risultato_deposito:
    print("Deposito Alfa verificato con successo.")

else:
    print("Errore: Deposito non trovato.")

print("-" * 40)

# 2. QUERY CON VARIABILE: Recupero distanza

query_distanza = "corridoio(cliente_rossi, deposito_alfa, Distanza)"
risultato_distanza = list(prolog.query(query_distanza))

if risultato_distanza:
    distanza_estratta = risultato_distanza[0]['Distanza']
    print(f"Distanza calcolata da Prolog: {distanza_estratta} metri")

else:
    print("Impossibile calcolare la distanza.")