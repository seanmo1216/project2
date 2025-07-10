# streamlit_funnel_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Customer Journey Funnel Dashboard")

uploaded_file = st.file_uploader("Upload Journey CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Clean and sort data
    df_sorted = df.sort_values(by=['User ID', 'Timestamp'])
    df_unique = df_sorted.drop_duplicates(subset=['User ID', 'Stage'], keep='first')

    # Define stage order
    stage_order = ['Awareness', 'Interest', 'Contact', 'Demo', 'Purchase']
    df_unique['Stage'] = pd.Categorical(df_unique['Stage'], categories=stage_order, ordered=True)

    # Calculate funnel metrics
    stage_counts = df_unique.groupby('Stage')['User ID'].nunique().reindex(stage_order).fillna(0)
    stage_data = pd.DataFrame({
        'Stage': stage_counts.index,
        'User Count': stage_counts.values
    })
    stage_data['Conversion Rate (%)'] = stage_data['User Count'].pct_change(-1).abs().fillna(0) * 100
    stage_data['Drop-off (%)'] = 100 - stage_data['Conversion Rate (%)']

    # Display funnel table
    st.subheader("Funnel Summary Table")
    st.dataframe(stage_data)

    # Plot funnel chart
    st.subheader("Funnel Chart")
    fig, ax = plt.subplots()
    ax.barh(stage_data['Stage'], stage_data['User Count'], color='skyblue')
    ax.invert_yaxis()
    ax.set_xlabel('Number of Users')
    ax.set_title('Customer Journey Funnel')
    st.pyplot(fig)

    # Download results
    csv = stage_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Funnel Summary", csv, "funnel_summary.csv", "text/csv")
else:
    st.info("Please upload a journey_input.csv file with columns: User ID, Timestamp, Stage")
