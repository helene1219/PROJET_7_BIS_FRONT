

# Importation librairie
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import plotly.express as px

import requests
import shap
import streamlit as st
shap.initjs()
from streamlit_shap import st_shap



# Change the console encoding
sys.stdout.reconfigure(encoding='utf-8')


API_URL = "https://scoring-p7.onrender.com"
#API_URL="http://127.0.0.1:8000"


#Loading data……
id_client = requests.get(f"{API_URL}/ids/").json()
nb_credits=requests.get(f"{API_URL}/nb_credit/").json()
rev_moy=requests.get(f"{API_URL}/rev_moyen/").json()
credits_moy=requests.get(f"{API_URL}/credit_moyen/").json()
df_age=requests.get(f"{API_URL}/data_age/").json()
df_income=requests.get(f"{API_URL}/data_income/").json()
feature=requests.get(f"{API_URL}/feature/").json()

#######################################
# SIDEBAR
#######################################


html_temp = """
<div style="background-color: #D54773; padding:10px; border-radius:10px">
<h1 style="color: white; text-align:center">Dashboard Scoring Credit</h1>
</div>

"""
st.markdown(html_temp, unsafe_allow_html=True)

st.sidebar.header("**INFORMATION GENERALE**")


#Selection de l'id_client
client_id = st.sidebar.selectbox("Client ID", id_client)

response=requests.get(f"{API_URL}/data_client/{int(client_id)}").json()

data_client=pd.DataFrame(response)

#Nombre de crédit dans échantillon
st.sidebar.markdown("<u>NOMBRE DE CREDIT :</u>", unsafe_allow_html=True)
st.sidebar.text(nb_credits)

#Revenu moyen
st.sidebar.markdown("<u>REVENU MOYEN DATA:</u>", unsafe_allow_html=True)
st.sidebar.text(int(rev_moy))

#Montant crédit moyen
st.sidebar.markdown("<u>MONTANT MOYEN DU CREDIT DATA :</u>", unsafe_allow_html=True)
st.sidebar.text(int(credits_moy))
    
# PAGE PRINCIPAL
#######################################

#Information client sélectionné
st.header(" INFORMATION CLIENT SELECTIONNE ")

st.write(" SEXE: ", data_client["CODE_GENDER"].values[0])
st.write(" AGE : {:.0f} ans".format(int(data_client["DAYS_BIRTH"])))
st.write("SITUATION DE FAMILLE : ", data_client["NAME_FAMILY_STATUS"].values[0])

       
#Distribution Age
data_age=pd.DataFrame(df_age)
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data_age["DAYS_BIRTH"], edgecolor = 'k', color="#ADADAD",bins=20)
ax.axvline(int(data_client["DAYS_BIRTH"].values), color="black", linestyle='--')
ax.set(title='AGE CLIENT', xlabel='AGE', ylabel='')
st.pyplot(fig)


st.subheader("REVENU (EN €)")
st.write("REVENU TOTAL : {:.0f}".format(data_client["AMT_INCOME_TOTAL"].values[0]))
st.write("MONTANT DU CREDIT : {:.0f}".format(data_client["AMT_CREDIT"].values[0]))
st.write("ANNUITE DU CREDIT : {:.0f}".format(data_client["AMT_ANNUITY"].values[0]))
st.write("MONTANT DU BIEN POUR LE CREDIT : {:.0f}".format(data_client["AMT_GOODS_PRICE"].values[0]))


#Distribution Revenu
data_income=pd.DataFrame(df_income)
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(data_income["AMT_INCOME_TOTAL"], edgecolor = 'k', color="#ADADAD", bins=20)
ax.axvline(int(data_client["AMT_INCOME_TOTAL"].values[0]), color="black", linestyle='--')
ax.set(title='REVENU DES CLIENTS', xlabel='REVENU (EN €)', ylabel='')
st.pyplot(fig)
st.markdown("<i>…</i>", unsafe_allow_html=True)

#Réponse crédit
st.subheader(" STATUT DU CLIENT ")
    
statut=requests.get(f"{API_URL}/prediction/{int(client_id)}").json()

if statut==0:
    html_temp = """
    <div style="background-color: #D54773; padding:2px; border-radius:10px">
    <h1 style="color: white; font-size:20px; text-align:center">CLIENT RISQUE - CREDIT NON ACCORDE</h1>
    </div>
    
    """
    st.markdown(html_temp, unsafe_allow_html=True)

else:
    html_temp = """
    <div style="background-color: #D54773; padding:2px; border-radius:10px">
    <h1 style="color: white; font-size:20px; text-align:center">CLIENT NON RISQUE - CREDIT ACCORDE</h1>
    </div>
    
    """
    st.markdown(html_temp, unsafe_allow_html=True)

st.write("")
st.write("")
    
#Feature importance / description
st.subheader(" IMPORTANCE DES FEATURES ")

shap_id=requests.get(f"{API_URL}/shap/{int(client_id)}").json()


df_shap=pd.DataFrame.from_dict(shap_id, orient='index', columns=['Valeur']).reset_index()
df_feature=pd.DataFrame(feature, columns=['Feature']).reset_index()     
    
df=pd.concat([df_shap['Valeur'], df_feature['Feature']], axis=1)
df_neg=df.loc[df['Valeur'] < 0].sort_values(by='Valeur', ascending=True)
df_pos=df.loc[df['Valeur'] > 0].sort_values(by='Valeur', ascending=False)

st.write("FEATURES AYANT DES VALEURS DE SHAP NEGATIVES : ",df_neg.head())    
    
fig, ax = plt.subplots(figsize=(10, 5))
df=df_neg[:10]
sns.barplot(df, x="Valeur", y="Feature", color="#ADADAD")
st.pyplot(fig)   
    
    
    
st.write("FEATURES AYANT DES VALEURS DE SHAP POSTIVIES : ",df_pos.head())         
       
fig, ax = plt.subplots(figsize=(10, 5))
df=df_pos[:10]
sns.barplot(df, x="Valeur", y="Feature", color="#ADADAD")
st.pyplot(fig)

    
    








