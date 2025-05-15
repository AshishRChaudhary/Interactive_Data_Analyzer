import streamlit as st
from operations import data_analysis,handle_missing_data

df = None
st.title("📊 Interactive Data Analysis App")

# Upload or paste data
data_source = st.radio("Choose data source:", ("Upload CSV", "Paste Data"))

try:
    if st.sidebar.checkbox("Handle Missing Values"):
        handle_missing_data(df,data_source)

    else:
        data_analysis(df,data_source)         
            
except Exception as e:
    # Handle any parsing or DataFrame conversion error
    st.error(f"Please provde data")


