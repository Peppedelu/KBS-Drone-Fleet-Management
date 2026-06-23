import os
import joblib
import pandas as pd
from pyswip import Prolog

# 1. INIZIALIZZAZIONE E CARICAMENTO KB PROLOG (Moduli 1 & 2)
prolog = Prolog()
prolog.consult("mappa.pl.txt")

# 2. CARICAMENTO DEL MODELLO PREVENTIVAMENTE ADDESTRATO (Modulo 3)
modello_path = os.path.join("supervised_learning", "modello_knn.joblib")
if not os.path.exists(modello_path):
    raise FileNotFoundError(f"Errore: file del modello non trovato in {modello_path}")

knn_model = joblib.load(modello_path)

# 3. CORE LOGIC: PROCESSO DECISIONALE INTEGRATO
def pianifica_missione(nodo_partenza, nodo_destinazione, meteo_sensori, drone_stato):
    print("=" * 65)
    print(f"KBS DRONI - VERIFICA FLUTTUAZIONE TRATTA: [{nodo_partenza} → {nodo_destinazione}]")
    print("=" * 65)

    # Interrogazione del motore inferenziale Prolog per il calcolo dinamico del percorso
    query_string = f"calcola_percorso({nodo_partenza}, {nodo_destinazione}, Distanza)"
    risultati_prolog = list(prolog.query(query_string))
    
    if not risultati_prolog:
        print(f"ESITO: Missione respinta. Tratta non raggiungibile secondo la KB Prolog.")
        print("=" * 65)
        return

    print("-> [KB Prolog] Validazione topologia superata: percorso esistente.")
 
    # Estrazione dinamica della distanza dalla prima soluzione restituita da Prolog
    distanza_metri = float(risultati_prolog[0]['Distanza'])
    distanza_km = distanza_metri / 1000.0
    print(f" → [KB Prolog] Distanza calcolata dinamicamente: {distanza_metri} metri ({distanza_km:.2f} km)")
 
    # Preparazione dei dati correnti per l’interrogazione dell’oracolo ML
    dati_sensori = pd.DataFrame([{
        'velocita_vento': meteo_sensori['velocita_vento'],
        'pioggia': meteo_sensori['pioggia'],
        'temperatura': meteo_sensori['temperatura'],
        'peso_carico': drone_stato['peso_carico']
    }])

    # Predizione del consumo energetico base (Wh/km)
    consumo_base = float(knn_model.predict(dati_sensori)[0])

    # Scaliamo il consumo energetico totale sulla reale distanza fornita dalla KB
    consumo_totale_stimato = consumo_base * distanza_km
    
    print(f" → [ML KNN] Consumo specifico stimato (meteo + carico): {consumo_base:.2f} Wh/km")
    print(f" → [KBS] Consumo complessivo calcolato per la tratta: {consumo_totale_stimato:.2f} Wh")
    print(f" → [Drone] Stato Batteria Residua del vettore: {drone_stato['batteria_residua']:.2f} Wh") 

    # Ragionamento basato su vincoli fisici e decisionali
    if drone_stato['batteria_residua'] >= consumo_totale_stimato:
        autonomia_rimanente = drone_stato['batteria_residua'] - consumo_totale_stimato
        print(f"\n SEMAFORO VERDE: Autonomia sufficiente. Batteria residua all’arrivo: {autonomia_rimanente:.2f} Wh")
    else:
        print("\n SEMAFORO ROSSO: Autonomia insufficiente! Il KBS blocca il decollo e richiede ricarica.")

    print("=" * 65)

# 4. RUN DI SIMULAZIONE OPERATIVA
if __name__ == "__main__":
    # Esempio di telemetria meteo real_time
    condizioni_meteo = {
        'velocita_vento': 12.5,
        'pioggia': 0,           # 0 = Sereno, 1 = Pioggia
        'temperatura': 20.0  
    }
    
    # Esempio di stato energetico e logistico del drone
    stato_veicolo = {
        'peso_carico': 1.2, # Kg
        'batteria_residua': 120.0 # Wh disponibili
    }

    # Eseguiamo il test con i nodi reali presenti in mappa.pl.txt
    pianifica_missione("deposito_alfa", "cliente_rossi", condizioni_meteo, stato_veicolo)
