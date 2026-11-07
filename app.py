
import streamlit as st
import pandas as pd

st.title("🛒 TrovaPrezzi GDO - Cesena")
st.write("Confronta i prezzi dei prodotti nei supermercati della tua zona!")

# Carichiamo il nostro file CSV in modo pulito
df = pd.read_csv("prezzi_supermercati.csv")

# Caselle di input per l'utente nella pagina web
prodotto_input = st.text_input("Cosa vuoi comprare?", "Cipolline borretane")
città_input = st.selectbox("Seleziona la città", ["Cesena", "Forlì", "Ravenna"])

# Pulsante di ricerca
if st.button("Cerca Prezzo"):
    # Filtriamo i dati
    risultati = df[
        df['prodotto'].str.contains(prodotto_input, case=False, na=False) & 
        (df['città'].str.lower() == città_input.lower())
    ]
    
    risultati_ordinati = risultati.sort_values(by='prezzo', ascending=True)
    
    if not risultati_ordinati.empty:
        st.success(f"Trovati {len(risultati_ordinati)} risultati!")
        # Mostriamo la tabella bella e colorata su Streamlit
        st.dataframe(risultati_ordinati[['supermercato', 'prodotto', 'prezzo', 'offerta']])
    else:
        st.warning("Nessun prodotto trovato con questi criteri.")
