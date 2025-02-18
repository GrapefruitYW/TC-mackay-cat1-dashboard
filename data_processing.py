import pandas as pd
from typing import Optional
import streamlit as st

def load_data(uploaded_file) -> Optional[pd.DataFrame]:
    """Load and validate the uploaded CSV file."""
    if uploaded_file is None:
        return None
        
    file_type = uploaded_file.name.split('.')[-1]
    if file_type != 'csv':
        return None
        
    return pd.read_csv(uploaded_file, parse_dates=['Creation Date', 'Appointment Date', 'Referrer Expiry Date'])


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process and clean the patient data."""
    # Filter for Category 3
    if 'Category' in df.columns:
        df = df[df['Category'].astype(str) == '3']
        if df.empty:
            st.warning("No data found for Category 3. Showing all data instead.")
            df = pd.read_csv(uploaded_file, parse_dates=['Creation Date', 'Appointment Date', 'Referrer Expiry Date'])
    
    # Drop unnecessary columns
    df = df.drop(columns=['Client','DOB','Case Manager'])

    
    # Rename columns
    df.rename(columns={
        'Status': 'Workflow status',
        'APPOINTMENT STATUS': 'Coreplus status'
    }, inplace=True)
    
    # Add validation for required columns
    required_cols = ['Creation Date', 'Appointment Date', 'Referrer Expiry Date']
    if not all(col in df.columns for col in required_cols):
        st.error(f"Missing required columns: {required_cols}")
        return pd.DataFrame()

    
    # Calculate window times
    # Calculate window times in days
    df['Booking window'] = (df['Appointment Date'] - df['Creation Date']).dt.days

    
    # Validate window calculations
    if df[['Booking window']].isnull().any().any():
        st.warning("Some date calculations resulted in null values. Please check your date columns.")

    
    return df
