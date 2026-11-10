import streamlit as st
import pandas as pd

st.set_page_config(page_title="TrovaPrezzi GDO Romagna", page_icon="🛒", layout="wide")

st.title("🛒 TrovaPrezzi GDO - Cesena & Forlì")
st.write("Esplora le offerte reali dai volantini attivi o cerca un prodotto specifico!")

# Carichiamo il nostro file CSV
@st.cache_data
def carica_dati():
    return pd.read_csv("prezzi_supermercati.csv")

df = carica_dati()

# --- BARRA LATERALE PER I FILTRI E LA CACHE ---
st.sidebar.header("Pannello di Controllo")

# Pulsante magico per pulire la cache e ricaricare i dati freschi da GitHub
if st.sidebar.button("🔄 Aggiorna Dati da GitHub"):
    st.cache_data.clear()
    st.success("Cache pulita! Dati aggiornati.")
    # Ricarica i dati freschi dopo aver pulito la cache
    df = carica_dati()

st.sidebar.markdown("---")
st.sidebar.header("Filtri di ricerca")

# Selezione della città
città_disponibili = sorted(df['città'].unique())
città_scelta = st.sidebar.selectbox("Seleziona la città", ["Tutte"] + città_disponibili)

# Selezione del supermercato
supermercati_disponibili = sorted(df['supermercato'].unique())
supermercato_scelto = st.sidebar.selectbox("Seleziona il supermercato", ["Tutti"] + supermercati_disponibili)

# Casella di ricerca testuale
prodotto_input = st.text_input("Cosa cerchi? (Scrivi 'tutto' o lascia vuoto per vedere l'elenco completo)", "")

# --- LOGICA DI FILTRAGGIO ---
# Partiamo dall'intero dataframe
risultati = df.copy()

# 1. Filtro città
if città_scelta != "Tutte":
    risultati = risultati[risultati['città'].str.lower() == città_scelta.lower()]

# 2. Filtro supermercato
if supermercato_scelto != "Tutti":
    risultati = risultati[risultati['supermercato'].str.upper() == supermercato_scelto.upper()]

# 3. Filtro prodotto (se l'utente scrive qualcosa di diverso da vuoto o "tutto")
if prodotto_input.strip() and prodotto_input.strip().lower() != "tutto":
    risultati = risultati[risultati['prodotto'].str.contains(prodotto_input, case=False, na=False)]

# Ordinamento: dal prezzo più basso al più alto
risultati_ordinati = risultati.sort_values(by='prezzo', ascending=True)

# --- VISUALIZZAZIONE RISULTATI ---
st.subheader(f"Risultati trovati: {len(risultati_ordinati)}")

if not risultati_ordinati.empty:
    # Mostriamo la tabella interattiva con i dati ordinati
    st.dataframe(
        risultati_ordinati[['supermercato', 'città', 'prodotto', 'prezzo', 'offerta']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Nessun prodotto trovato con questi criteri di ricerca.")
