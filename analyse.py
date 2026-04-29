import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Analyse des données - Étudiants & IA")

# Chargement
df = pd.read_csv("data.csv")

# --- Prétraitement ---
# transformer les colonnes texte en listes
df["outils_list"] = df["outils"].apply(lambda x: x.split(",") if pd.notna(x) else [])
df["fonct_list"] = df["fonctionnalites_avancees"].apply(lambda x: x.split(",") if pd.notna(x) else [])

# variables calculées
df["nb_outils"] = df["outils_list"].apply(len)
df["nb_fonct"] = df["fonct_list"].apply(len)

df["ethique_valide"] = df["score_ethique"] >= 12
df["culture_ia"] = df["nb_fonct"] >= 3

st.subheader("Aperçu des données")
st.dataframe(df)

st.subheader("Répartition des étudiants selon l'éthique")

ethique_counts = df["ethique_valide"].value_counts()

#affichage
df["ethique_label"] = df["ethique_valide"].map({
    True: "Éthique (>= 12)",
    False: "Non éthique (< 12)"
})
df["culture_label"] = df["culture_ia"].map({
    True: "Bonne culture IA",
    False: "Faible culture IA"
})

#3. 📊 Graphique Éthique (propre et lisible)

ethique_counts = df["ethique_label"].value_counts().reset_index()
ethique_counts.columns = ["Categorie", "Nombre"]
fig = px.bar(
    ethique_counts,
    x="Categorie",
    y="Nombre",
    title="Répartition des étudiants selon le niveau d'éthique",
    labels={
        "Categorie": "Niveau d'éthique",
        "Nombre": "Nombre d'étudiants"
    },
    text="Nombre"
)
st.plotly_chart(fig)

#4. 📊 Graphique Culture IA
culture_counts = df["culture_label"].value_counts().reset_index()
culture_counts.columns = ["Categorie", "Nombre"]
fig = px.bar(
    culture_counts,
    x="Categorie",
    y="Nombre",
    title="Niveau de culture de l'IA",
    labels={
        "Categorie": "Culture",
        "Nombre": "Nombre d'étudiants"
    },
    text="Nombre"
)
st.plotly_chart(fig)

#5. 📊 Outils IA (avec axes clairs)
outils_counts = df["outils_list"].explode().value_counts().reset_index()
outils_counts.columns = ["Outil", "Nombre"]
fig = px.bar(
    outils_counts,
    x="Outil",
    y="Nombre",
    title="Outils d'IA les plus utilisés",
    labels={
        "Outil": "Outil IA",
        "Nombre": "Nombre d'utilisations"
    },
    text="Nombre"
)
st.plotly_chart(fig)

#groupage des donnees
grouped = df.groupby("niveau_etude")[["ethique_valide", "culture_ia"]].mean().reset_index()
# convertir en pourcentage
grouped["ethique_valide"] = grouped["ethique_valide"] * 100
grouped["culture_ia"] = grouped["culture_ia"] * 100

grouped = grouped.rename(columns={
    "ethique_valide": "Ethique (%)",
    "culture_ia": "Culture IA (%)"
})
#A. Éthique par niveau
fig = px.bar(grouped,
    x="niveau_etude",
    y="Ethique (%)",
    title="Éthique par niveau d'étude",
    labels={
        "niveau_etude": "Niveau",
        "Ethique (%)": "Pourcentage d'étudiants éthiques"
    },
    text_auto=True
)
st.plotly_chart(fig)

#B. Culture IA par niveau
fig = px.bar(
    grouped,
    x="niveau_etude",
    y="Culture IA (%)",
    title="Culture IA par niveau d'étude",
    labels={
        "niveau_etude": "Niveau",
        "Culture IA (%)": "Pourcentage de culture IA"
    },
    text_auto=True
)
st.plotly_chart(fig)



#2) Satisfaction vs culture IA
#uestion : ceux qui maîtrisent mieux l’IA sont-ils plus satisfaits ?
satisfaction_culture = df.groupby("culture_ia")["satisfaction"].mean().reset_index()
satisfaction_culture["culture_label"] = satisfaction_culture["culture_ia"].map({
    True: "Bonne maîtrise IA",
    False: "Faible maîtrise IA"
})
fig = px.bar(
    satisfaction_culture,
    x="culture_label",
    y="satisfaction",
    title="Satisfaction moyenne selon la maîtrise de l'IA",
    labels={
        "culture_label": "Niveau de maîtrise",
        "satisfaction": "Satisfaction moyenne"
    },
    text_auto=True
)
st.plotly_chart(fig)

#3) Identifier les profils “à risque”

risque = df[(df["ethique_valide"] == False) & (df["culture_ia"] == False)]
st.subheader("Étudiants à risque")
st.dataframe(risque)
