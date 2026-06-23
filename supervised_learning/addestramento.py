
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import KFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

# 1. CARICAMENTO DEL DATASET

df = pd.read_csv("dataset/consumi_droni.csv")

# Separiamo le feature (X) dal target continuo da predire (y)

X = df[['velocita_vento', 'pioggia', 'temperatura', 'peso_carico']]
y = df['consumo_energetico']

# 2. CONFIGURAZIONE DELLA VALUTAZIONE RIGOROSA
# Impostiamo una 5-Fold Cross-Validation per evitare run singoli

kf = KFold(n_splits = 5, shuffle = True, random_state = 42)

# Definiamo le metriche richieste: MSE e Max Error (trasformata in positive)

metriche = {
    'mse' : 'neg_mean_squared_error',
    'max_error' : 'neg_max_error'

}

# 3. DEFINIZIONE DEI MODELLI CON IPERPARAMETRI SCELTI
# Scegliamo K = 5 per KNN e profondità massima = 5 per l'albero (scelte di progetto da documentare)

modelli = {
    'KNN Regressor (K = 5)' : make_pipeline(StandardScaler(),KNeighborsRegressor(n_neighbors = 5)),
    'Decision Tree (Max Depth = 5)' : DecisionTreeRegressor(max_depth = 5, random_state = 42 )

}

print("--- VALUTAZIONE MODELLI TRAMITE 5-FOLD CROSS-VALIDATION ---\n")

# 4. RUN E CALCOLO DI MEDIA E DEVIAZIONE STANDARD

for nome, modello in modelli.items() :
    risultati = cross_validate(modello, X, y, cv = kf, scoring = metriche)

    #Scikit-Learn restituisce valori negativi per la massimizzazione, li invertiamo

    mse_mediati = -risultati['test_mse']
    max_error_mediati = -risultati['test_max_error']

    print(f"=== {nome}===")
    print(f"MSE: {np.mean(mse_mediati):.3f} (±{np.std(mse_mediati):.3f})")
    print(f"Max Error: {np.mean(max_error_mediati):.3f} (±{np.std(max_error_mediati):.3f})")

# 5. ADDESTRAMENTO FINALE E SALVATAGGIO

print("\n--- SALVATAGGIO MODELLO VINCENTE ---")
modello_vincente = modelli['KNN Regressor (K = 5)']

# Addestramento sull'intero dataset per massimizzare la conoscenza

modello_vincente.fit(X, y)

# Salvattaggio del file .joblib

joblib.dump(modello_vincente, "supervised_learning/modello_knn.joblib")
print("Modello salvato con successo in: supervised_learning/modello_knn.joblib")