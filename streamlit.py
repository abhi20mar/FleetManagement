import streamlit as st
import pandas as pd
import pymongo
import os
import ssl

st.title("Vehicle Batcave")
# Load environment variables for MongoDB credentials
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@cluster0.dd5kr.mongodb.net/mydatabase?retryWrites=true&w=majority")

def get_mongo_data():
    client = pymongo.MongoClient(MONGO_URI, ssl_cert_reqs=ssl.CERT_NONE)

    db = client['mydatabase']
    collection = db['obd_data']
        
    # Fetch the data from the collection
    data = list(collection.find({}))  # You can add query filters if needed
    return data
    
def clean_data(df):
    # Convert columns with numeric values stored as strings with commas
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        
    # Remove percentage symbols and convert to floats
    percentage_cols = ['FUEL_LEVEL', 'THROTTLE_POS', 'TIMING_ADVANCE', 'EQUIV_RATIO']
    for col in percentage_cols:
        if col in df.columns:
            df[col] = df[col].str.replace('%', '', regex=False).astype(float)
    
    # Fill NaN values with None (MongoDB friendly)
    df = df.where(pd.notna(df), None)
    
    return df

data = pd.DataFrame(get_mongo_data())

tab1, tab2 = st.tabs(["Upload CSV to Mongdb", "Display Data"])

with tab1:
    # Streamlit app
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df = clean_data(df)
        
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URI)
        db = client["mydatabase"]
        collection = db["obd_data"]
        
        # Insert data into MongoDB
        records = df.to_dict(orient="records")
        collection.insert_many(records)
        
        st.success("Data uploaded successfully!")

with tab2:
    st.write('display data')
    car_brands = st.multiselect('Filter Data',data['MARK'].unique())
    data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], unit='ms')
    st.write(data.loc[data['MARK'].isin(car_brands),])
