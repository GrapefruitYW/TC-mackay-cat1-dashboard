import streamlit as st
from data_processing import load_data, process_data
from visualization import create_sankey_chart, create_conversion_plot
from utils import WINDOW_OPTIONS, DEFAULT_THRESHOLD, MAX_THRESHOLD, get_conversion_metrics


# File upload and data processing
uploaded_file = st.file_uploader("Choose a file", type=['csv'])
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        df = process_data(df)


        # Main page user inputs
        st.markdown("### Conversion Analysis Settings")
        
        threshold = st.slider(
            "Threshold days for patient to be seen",
            min_value=0,
            max_value=MAX_THRESHOLD,
            value=DEFAULT_THRESHOLD
        )



        # Main content
        st.markdown("## Mackay Category 1 Booking window dashboard")
        st.markdown("""
        This dashboard displays how long it takes from when a workflow patient profile is created to when their appointment is """)

        # st.markdown("""
        #     The data shows how long it takes in each step of the patient journey: 
        #     1. **Booking window** (time from patient profile creation to time of booking) 
        #     2. **Appointment window** (time from booking to time of scheduled appointment)  
        #     3. **Entire patient window** (time from patient profile creation to time of scheduled appointment)
            
            
        # """)


        # Get metrics
        window = "Booking window"
        metrics = get_conversion_metrics(df, window, threshold)


        # Display high level conversion numbers
        st.markdown("## High level conversion numbers")
        sankey_fig = create_sankey_chart()
        st.plotly_chart(sankey_fig)

        st.markdown("""
            **Notes:** Categories are organised by workflow 'status'. Booked patients are all patients that have an appointment date scheduled. Unbooked patients are all patients with no appointment date. Awaiting booking patients are patients who have 'awaitingBooking','adminAudit' status. Patient returned are patients who have 'ftaRemove','nrfc','expiredReferral' status.
        """)



        # Display results
        st.markdown(f"## Results for the {window}")
        
        # Create and display conversion plot
        fig, ax = create_conversion_plot(df, window, threshold)
        st.pyplot(fig)

        # Display metrics
        st.write(f"Total number of cat1 patients with appointment booked and valid coreplus & workflow profiles is {df.shape[0]}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Over threshold", value=f"{metrics['exceed']} patients")
        col2.metric("Mean window", value=f"{metrics['mean']} days")
        col3.metric("Median window", value=f"{metrics['median']} days")

        # Display data table
        st.write("Table of patients who exceeded the threshold time")
        st.dataframe(df[df[window] > threshold])


        # Conversion results
        # st.markdown("## Conversion summary")

    else:
        st.error("Unsupported file format. Please upload the mackay conversion CSV file.")
