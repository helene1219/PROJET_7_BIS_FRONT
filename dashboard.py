import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import plotly.express as px
import shap
import requests

# Change the console encoding
sys.stdout.reconfigure(encoding='utf-8')



API_URL = "http://127.0.0.1:8000"
    
#Loading data……
id_client = requests.get(f"{API_URL}/ids/").json()
nb_credits=requests.get(f"{API_URL}/nb_credit/").json()
rev_moy=requests.get(f"{API_URL}/rev_moyen/").json()
credits_moy=requests.get(f"{API_URL}/credit_moyen/").json()
df_age=requests.get(f"{API_URL}/age/").json()
df_income=requests.get(f"{API_URL}/data_plot/").json()
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

#Loading selectbox
chk_id = st.sidebar.selectbox("Client ID", id_client)

data_id=requests.get(f"{API_URL}/data_client/{chk_id}").json()
data_client=pd.DataFrame(data_id)

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
    #st.write(" SEXE: ", data_client["CODE_GENDER"].values[0])
    #st.write(" AGE : {:.0f} ans".format(int(data_client["DAYS_BIRTH"]/-365)))
    #st.write(" AGE : {:.0f} ans".data_client["DAYS_BIRTH"]/-365)
    #st.write("SITUATION DE FAMILLE : ", data_client["NAME_FAMILY_STATUS"].values[0])
    #st.write("NOMBRE D'ENFANT : {:.0f}".format(data_client["CNT_CHILDREN"].values[0]))

        
    #Age distribution plot
    #data_age = load_age_population(data)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_age, edgecolor = 'k', color="#D54773",bins=20)
    #ax.axvline(int(-infos_client["DAYS_BIRTH"].values /365), color="black", linestyle='--')
    ax.set(title='AGE CLIENT', xlabel='AGE', ylabel='')
    st.pyplot(fig)


    #st.subheader("REVENU (EN €)")
    #st.write("REVENU TOTAL : {:.0f}".format(infos_client["AMT_INCOME_TOTAL"].values[0]))
    #st.write("MONTANT DU CREDIT : {:.0f}".format(infos_client["AMT_CREDIT"].values[0]))
    #st.write("ANNUITE DU CREDIT : {:.0f}".format(infos_client["AMT_ANNUITY"].values[0]))
    #st.write("MONTANT DU BIEN POUR LE CREDIT : {:.0f}".format(infos_client["AMT_GOODS_PRICE"].values[0]))


    #Income distribution plot
    data_income = load_income_population(data)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data_income["AMT_INCOME_TOTAL"], edgecolor = 'k', color="#D54773", bins=10)
    #ax.axvline(int(infos_client["AMT_INCOME_TOTAL"].values[0]), color="black", linestyle='--')
    ax.set(title='REVENU DES CLIENTS', xlabel='REVENU (EN €)', ylabel='')
    st.pyplot(fig)

else:
    st.markdown("<i>…</i>", unsafe_allow_html=True)
    
    #Customer solvability display
    st.header(" ANALYSE CREDIT DEMANDE ")
    prediction,statut = load_prediction(sample,X_test, chk_id, clf)
    st.write(" PROBABLITE DE DEFAUT : {:.0f} %".format(round(float(prediction)*100, 2)))
    st.write("STATUT DU CLIENT : ",statut)
    
    
#Feature importance / description
if st.checkbox("AFFICHER LES RESULTATS SUR LE CLIENT ?",key="Option2"):
    nbligne=sample.loc[sample['SK_ID_CURR'] == int(chk_id)].index.item()
    fig, ax = plt.subplots(figsize=(10, 10))
    explainer = shap.Explainer(clf)
    shap_values = explainer.shap_values(X_test)
    shap_vals = explainer(X_test)
    shap.waterfall_plot(shap_vals[nbligne][:, 0],show = False)
    st.pyplot(fig)
        
else:
    st.markdown("<i>…</i>", unsafe_allow_html=True)    
    
    
    








