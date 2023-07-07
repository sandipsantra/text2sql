import streamlit as st
import pandas as pd
import requests
import json
from azure.storage.blob import BlobClient,BlobServiceClient

class text2sql:
    
    def __init__(self):     
        self.rest_api='https://unum-mlprdpmcv-text2sqlschema.eastus.inference.ml.azure.com/score'
        self.api_key='yCt9Zovh5zYSbCvl8uDJah6yMwNhzuo1'
        self.headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ self.api_key), 'azureml-model-deployment': 'text2sql-1' }
        self.conn_string="DefaultEndpointsProtocol=https;AccountName=mlstorageprdajsa;AccountKey=JmQcHKIwuWyr5m6YDDOeInfe3r88AHPTXd73iJ+8aetUDpNcOoPaW0mQT6SK/vs3pnycnfOVQhD2F5DJWFc7xA==;EndpointSuffix=core.windows.net"
        self.container_name = 'unumdata'
        self.container_path="https://mlstorageprdajsa.blob.core.windows.net/unumdata/"
        self.token="?sp=r&st=2023-07-03T13:36:49Z&se=2023-12-08T21:36:49Z&spr=https&sv=2022-11-02&sr=c&sig=cxewsu5%2BcH2wpnF5I9fQPGmWfkmgt%2BaYTW4Apn8JIJA%3D"

    def upload_blob_file(self,uploaded_file,file_data):           
        blob_service_client = BlobServiceClient.from_connection_string(self.conn_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=uploaded_file.name)
        blob_client.upload_blob(file_data, overwrite=True)
        return
    
    def read_dataframe(self,filename):       
        df=pd.read_csv(self.container_path+str(filename)+self.token,encoding = "ISO-8859-1")
        st.dataframe(df)
        return True

    def question_answer(self,question,filename):
        
        data={"inputdata":{"question":str(question),"path":self.container_path+str(filename)+self.token}}
        r=requests.post(self.rest_api,json.dumps(data),headers=self.headers)
        st.markdown('''<style>[data-testid="stMarkdownContainer"] ul{text-align:left;color:Blue;font-size:20px;}</style>''',unsafe_allow_html=True)
        st.markdown("Result: "+str(r.json()["inputdata"]["result"]))
        st.markdown("Summary: "+r.json()["inputdata"]["summary"])
        return        
        
if __name__ == '__main__': 

    st.header('Text-2-SQL') 
#     col1,col2 =st.columns([0.5,0.5],gap="large")
    if "load_state" not in st.session_state:
        st.session_state.load_state = False
    t2s=text2sql()
    uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
    btn=st.button('Upload')  
    if uploaded_file:
        file_data = uploaded_file.getvalue()
        if btn or st.session_state.load_state:
            t2s.upload_blob_file(uploaded_file,file_data)
            st.write("File Upload Successfully Completed")
            flag=t2s.read_dataframe(uploaded_file.name)
            st.session_state.load_state=True
            text=st.text_input("Write your Query","show me Class name which contain measure_code repeat_lact_minutes")
            if st.button("Submit") or st.session_state.load_state:
                t2s.question_answer(str(text),uploaded_file.name)
                st.session_state.load_state=True
            
            
            
            
                
                
    
