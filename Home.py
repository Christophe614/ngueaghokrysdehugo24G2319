import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Projet IA & Étudiants", layout="wide")

# --- HEADER ---
st.title(" Étude sur l'utilisation de l'IA chez les étudiants de la filiere informatique")
st.markdown("""
Cette application permet de :
- Collecter des données sur l’usage de l’IA
- Analyser l’éthique et la culture numérique des étudiants
- Visualiser les résultats sous forme de graphiques
""")


    

# --- INDICATEURS RAPIDES ---
st.subheader("📈 Indicateurs globaux")

if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")

    df["ethique_valide"] = df["score_ethique"] >= 12
    df["nb_fonct"] = df["fonctionnalites_avancees"].apply(lambda x: len(str(x).split(",")))
    df["culture_ia"] = df["nb_fonct"] >= 3

    taux_ethique = df["ethique_valide"].mean() * 100
    taux_culture = df["culture_ia"].mean() * 100

    col1, col2 = st.columns(2)

    col1.metric("Étudiants éthiques (%)", round(taux_ethique, 1))
    col2.metric("Bonne culture IA (%)", round(taux_culture, 1))

else:
    st.warning("Aucune donnée disponible pour le moment.")

# --- APERÇU ---
st.subheader("🗂 Aperçu des données")

if os.path.exists("data.csv"):
    st.dataframe(df.head())

# --- NAVIGATION ---
st.subheader("🚀 Accès rapide")

col1, col2 = st.columns(2)

with col1:
    if st.button("Accéder au formulaire de collecte"):
        st.switch_page("pages/collecte.py")

with col2:
    if st.button(" Voir le tableau de bord d’analyse"):
        st.switch_page("pages/analyse.py")

