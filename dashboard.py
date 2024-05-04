


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


def dict_to_exp(dico: dict) -> shap._explanation.Explanation:
    """
    Convertir un dictionnaire en shap explanation
    """
    explanation = shap.Explanation(values=dico.values())
    return explanation


API_URL = "https://scoring-p7.onrender.com"
#API_URL="http://127.0.0.1:8000"


#Loading data……
id_client = requests.get(f"{API_URL}/ids/").json()
nb_credits=requests.get(f"{API_URL}/nb_credit/").json()
rev_moy=requests.get(f"{API_URL}/rev_moyen/").json()
credits_moy=requests.get(f"{API_URL}/credit_moyen/").json()
df_age=requests.get(f"{API_URL}/data_age/").json()
df_income=requests.get(f"{API_URL}/data_income/").json()

            #######################################
                # SIDEBAR
             #######################################

                #Title display
html_temp = """
<div style="background-color: #D54773; padding:10px; border-radius:10px">
<h1 style="color: white; text-align:center">Dashboard Scoring Credit</h1>
</div>

"""
st.markdown(html_temp, unsafe_allow_html=True)

#Customer ID selection
st.sidebar.header("**INFORMATION GENERALE**")

#st.write("STATUT DU CLIENT : ",type(id_client))

#Loading selectbox
client_id = st.sidebar.selectbox("Client ID", id_client)

response=requests.get(f"{API_URL}/data_client/{int(client_id)}").json()

data_client=pd.DataFrame(response)
#Loading general info


### Display of information in the sidebar ###
#Number of loans in the sample
st.sidebar.markdown("<u>NOMBRE DE CREDIT :</u>", unsafe_allow_html=True)
st.sidebar.text(nb_credits)

#Average income
st.sidebar.markdown("<u>REVENU MOYEN DATA:</u>", unsafe_allow_html=True)
st.sidebar.text(rev_moy)

#AMT CREDIT
st.sidebar.markdown("<u>MONTANT MOYEN DU CREDIT DATA :</u>", unsafe_allow_html=True)
st.sidebar.text(credits_moy)
    
# HOME PAGE - MAIN CONTENT
#######################################

#Customer information display : Customer Gender, Age, Family status, Children, …
st.header(" INFORMATION CLIENT SELECTIONNE ")

if st.checkbox("AFFICHER LES INFORMATIONS SUR LE CLIENT ?",key="option1"):
    st.write(" SEXE: ", data_client["CODE_GENDER"].values[0])
    st.write(" AGE : {:.0f} ans".format(int(data_client["DAYS_BIRTH"])))
    st.write("SITUATION DE FAMILLE : ", data_client["NAME_FAMILY_STATUS"].values[0])

       
    #Age distribution plot
    data_age=pd.DataFrame(df_age)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data_age["DAYS_BIRTH"], edgecolor = 'k', color="#D54773",bins=20)
    ax.axvline(int(data_client["DAYS_BIRTH"].values), color="black", linestyle='--')
    ax.set(title='AGE CLIENT', xlabel='AGE', ylabel='')
    st.pyplot(fig)


    st.subheader("REVENU (EN €)")
    st.write("REVENU TOTAL : {:.0f}".format(data_client["AMT_INCOME_TOTAL"].values[0]))
    st.write("MONTANT DU CREDIT : {:.0f}".format(data_client["AMT_CREDIT"].values[0]))
    st.write("ANNUITE DU CREDIT : {:.0f}".format(data_client["AMT_ANNUITY"].values[0]))
    st.write("MONTANT DU BIEN POUR LE CREDIT : {:.0f}".format(data_client["AMT_GOODS_PRICE"].values[0]))


    #Income distribution plot
    data_income=pd.DataFrame(df_income)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data_income["AMT_INCOME_TOTAL"], edgecolor = 'k', color="#D54773", bins=20)
    ax.axvline(int(data_client["AMT_INCOME_TOTAL"].values[0]), color="black", linestyle='--')
    ax.set(title='REVENU DES CLIENTS', xlabel='REVENU (EN €)', ylabel='')
    st.pyplot(fig)
    st.markdown("<i>…</i>", unsafe_allow_html=True)
    
    #Customer solvability display
    st.header(" ANALYSE CREDIT DEMANDE ")
    statut=requests.get(f"{API_URL}/prediction/{int(client_id)}").json()
    
    if statut==0:
        profil="client risque - crédit non accordé"
    else:
        profil = "Client non risqué - crédit accordé"
    st.write("STATUT DU CLIENT : ",profil)

else:
    st.markdown("<i>…</i>", unsafe_allow_html=True)  
    


#Feature importance / description
if st.checkbox("AFFICHER LES RESULTATS SUR LE CLIENT ?",key="Option2"):

    
    shap_id=requests.get(f"{API_URL}/shap/{int(client_id)}").json()
    #exp = dict_to_exp(shap_id) 
    premier_element = shap_id.popitem()
    #type_shap=type(shap_id)
    
    st.write("1er : ",premier_element)
    #fig, ax = plt.subplots(figsize=(10, 10))
    #shap.summary_plot(shap_id,index,plot_type ="bar", max_display=10, color_bar=False, plot_size=(5, 5))
    #st.pyplot(fig)
else:
    st.markdown("<i>…</i>", unsafe_allow_html=True)    
    
    
    








