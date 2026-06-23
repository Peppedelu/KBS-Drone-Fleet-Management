
import pandas as pd
import numpy as np

# Impostiamo un seme casuale per avere dati replicabili

np.random.seed(42)
n_campioni = 500

# Generiamo le feature ambientali e fisiche

velocita_vento = np.random.uniform(0, 45, n_campioni) # km/h
pioggia = np.random.choice([0,1], size = n_campioni, p = [0.8, 0.2]) # 0 = No, 1 = Si
temperatura = np.random.uniform(5, 35, n_campioni) # Gradi Celsius
peso_carico = np.random.uniform(0.5, 5.0, n_campioni) # kg

# Calcoliamo il target (Consumo Energetico in Wh) con una formula fisica simulata + rumore
# Consumo base = 50 Wh. Il vento influisce molto, il carico anche, la pioggia aumenta l'attrito

rumore = np.random.normal(0, 5, n_campioni)
consumo = 50 + (velocita_vento * 1.2) + (pioggia * 15) - (temperatura * 0.1) + (peso_carico * 8) + rumore

# Arrotondiamo i valori per renderli puliti

consumo = np.clip(consumo, 20, 200) #Evita valori assurdi negativi

# Creiamo il DataFrame di Pandas

df = pd.DataFrame({

    'velocita_vento' : np.round(velocita_vento, 1),
    'pioggia' : pioggia,
    'temperatura' : np.round(temperatura, 1),
    'peso_carico' : np.round(peso_carico, 2),
    "consumo_energetico" : np.round(consumo, 1)
})

# Salviamo il file CSV ditrettamente dentro la cartella dataset

df.to_csv('dataset/consumi_droni.csv', index = False)
print("--- DATASET SINTETICO GENERATO CON SUCCESSO (500 RIGHE) ---")