import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Options Gamma Exposure Analyzer",
    page_icon="📈",
    layout="wide"
)

# Sidebar controls
with st.sidebar:
    st.header("Data Input")
    uploaded_file = st.file_uploader("Upload Options Chain Excel File", type=["xlsx"])
    
    st.header("Chart Settings")
    size_max = st.slider("Maximum Bubble Size", 10, 100, 40)
    show_data = st.checkbox("Show Raw Data Preview")

# Main app
st.title("📊 Options Greek Exposure Visualization")
st.markdown("### Interactive Bubble Chart for Gamma/Delta/Vanna Analysis")

if uploaded_file:
    try:
        # Read and process data
        df = pd.read_excel(uploaded_file)
        
        # Validate required columns
        required_cols = {'Gamma', 'Delta', 'Vanna'}
        if not required_cols.issubset(df.columns):
            missing = required_cols - set(df.columns)
            st.error(f"Missing required columns: {', '.join(missing)}")
            st.stop()
            
        # Calculate gamma metrics
        df['Gamma Exposure'] = df['Gamma'].abs()
        df['Gamma Scaled'] = df['Gamma Exposure'] / df['Gamma Exposure'].max()
        
        # Column selection
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            x_col = st.selectbox("X-Axis", df.columns, index=df.columns.get_loc('Delta'))
        with col2:
            y_col = st.selectbox("Y-Axis", df.columns, index=df.columns.get_loc('Vanna'))
        with col3:
            color_col = st.selectbox("Color By", df.columns, index=df.columns.get_loc('Moneyness'))
        with col4:
            hover_col = st.selectbox("Hover Info", df.columns, index=df.columns.get_loc('Option_Type'))

        # Create visualization
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            size='Gamma Scaled',
            color=color_col,
            hover_name=hover_col,
            size_max=size_max,
            title=f"Options Exposure: {x_col} vs {y_col}",
            labels={'Gamma Scaled': 'Normalized Gamma Exposure'},
            hover_data=[c for c in df.columns if c not in ['Gamma Scaled', 'Gamma Exposure']]
        )

        # Enhanced styling
        fig.update_layout(
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="monospace"
            ),
            xaxis=dict(
                gridcolor='#e9ecef',
                title_font=dict(size=18)
            ),
            yaxis=dict(
                gridcolor='#e9ecef',
                title_font=dict(size=18)
            )
        )

        # Display chart
        st.plotly_chart(fig, use_container_width=True)

        # Show data preview if requested
        if show_data:
            st.subheader("Data Preview")
            st.dataframe(df.sort_values('Gamma Exposure', ascending=False), height=300)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.markdown("""
    ### How to Use:
    1. Upload your options chain Excel file
    2. Ensure columns include: **Gamma, Delta, Vanna**
    3. Configure chart parameters in the sidebar
    4. Interact with the visualization
    
    ### Expected File Format:
    | Strike | Expiration | Option_Type | Moneyness | Delta | Gamma | Vanna | ... |
    |--------|------------|-------------|-----------|-------|-------|-------|-----|
    """)

# Add requirements section
st.sidebar.markdown("""
**Requirements:**
- Excel file with options chain data
- Required columns: Gamma, Delta, Vanna
- Supported formats: .xlsx
""")