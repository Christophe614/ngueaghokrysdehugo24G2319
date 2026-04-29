import streamlit as st 
import pandas as pd 
import os 


st.title("FORMULAIRE DE COLLECTE DE DONNEES")

#DONNEES
niveau= st.selectbox("votre niveau d'etude",["L1","L2","L3","M1","M2"]) 
outils = st.multiselect("Quels sont les outils d'IA que vous utilisez?",["ChatGPT", "DeepSeek", "Claude", "Gemini", "NoteBookLM"]) 
meilleur_outil = st.selectbox("Quel est votre meilleur outil?",["ChatGPT", "DeepSeek", "Claude", "Gemini", "NoteBookLM"]) 
frequence = st.select_slider("Avec quel fréquence les utilisez vous?", options =["Jamais", "rarement" , "parfois", "très souvent"]) 
satisfaction = st.slider("Sur une échelle de 0 à 100 quel est votre de niveau de satisfaction globale quant aux résultats fournis par les outils d’IA que vous utilisez?",min_value=0, max_value=100, value= 50, step=1) 
prompt = st.radio("Sais tu écrire un bon prompt",["oui un peu", "oui très bien" , "non"]) 
methodes_dapprentissage = st.multiselect("Comment apprends tu avec l’IA? Tu l'utilises pour:", ["faire des résumés de cours","générer des exercices corriges","expliquer un concept comme un tuteur le ferai"]) 
fonct_avancees = st.multiselect("Quelles sont les fonctionnalités avancées que vous avez déja utilisé?",["Generation d'images","Analyse de documents pdf", "Création de GPTs personnalisés","Recherche internet integré"]) 
ethique1 = st.radio("Es ce que tu précises toujours quand tu fais un devoir à remettre avec L’IA?",["oui","non"]) 
ethique2 = st.radio("Es tu capable de refaire les TP ou devoirs que tu as déjà réaliser avec l’IA?",["oui","non"]) 
ethique3 = st.radio("Es ce que tu as le droit d’envoyer une donnée privée dans une IA publique?",["oui","non"]) 
ethique4 = st.radio(" As tu déjà envoyer un devoir à l’enseignant 100% généré par l’IA?",["oui","non"]) 

if st.button("Envoyer"): 

# CALCUL DU SCORE ETHIQUE
    score_ethique=0 
    if ethique1 == "oui": 
        score_ethique += 5 
    if ethique2 == "oui": 
        score_ethique += 5 
    if ethique3 == "non": 
        score_ethique += 5 
    if ethique4 == "non": 
        score_ethique += 5 

    data = { 
        "niveau_etude": niveau, 
        "outils":",".join(outils) if outils else "aucune", 
        "meilleur_outil": meilleur_outil, 
        "satisfaction": satisfaction, 
        "prompt": prompt, 
        "methodes_dapprentissage": ",".join(methodes_dapprentissage) if methodes_dapprentissage else "aucune", 
        "fonctionnalites_avancees": ",".join(fonct_avancees) if fonct_avancees else "aucune", 
        "ethique1": ethique1, 
        "ethique2": ethique2, 
        "ethique3": ethique3, 
        "ethique4": ethique4, 
        "score_ethique":score_ethique,
    } 

    df = pd.DataFrame([data]) 
    if os.path.exists("data.csv"): 
        df.to_csv("data.csv", mode='a', header=False, index=False) 
    else: df.to_csv("data.csv", mode='w', header=True, index=False) 

    st.success("Merci pour votre contribution! Vos réponses ont bien été enregistrées")
