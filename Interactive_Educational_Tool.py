import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV files
data_path_co2 = "annual-co2-emissions-per-country.csv"  
data_path_energy = "energy-consumption-by-source-and-country.csv"  

data_co2 = pd.read_csv(data_path_co2)
data_energy = pd.read_csv(data_path_energy)


st.title("CO₂ Emissions and Energy Consumption Interactive Educational Tool for SEES 502 Energy Systems and Sustainability")
tab1, tab2, tab3, tab4 = st.tabs(["Introduction","View Data", "Calculate CO₂ Emissions","Contact"])

#Choosing years between 2000-2022, could be extended based on available data
data_co2 = data_co2[(data_co2['Year'] >= 2000) & (data_co2['Year'] <= 2022)]

#Choosing years between 2000-2022, could be extended based on available data
data_energy = data_energy[(data_energy['Year'] >= 2000) & (data_energy['Year'] <= 2022)]


entities = sorted(data_co2['Entity'].unique())
years = sorted(data_co2['Year'].unique())

with tab1:
   
    st.markdown("""
    This interactive tool is designed for the **SEES 502 Energy Systems and Sustainability** course at **METU NCC**.

    It provides students with the opportunity to understand the crucial role of renewable energy in promoting sustainability. The tool leverages comprehensive datasets from **Our World in Data**, allowing users to explore and analyze how renewable energy adoption affects CO2 emissions.
    """)

    st.header("Key Features:")

    st.subheader("1. Visualizing Energy Consumption & CO2 Emissions")
    st.markdown("""
    - View energy consumption from various sources across all countries from **2000-2022**.
    - Explore the corresponding **CO2 emissions** using interactive visualizers.
    - See the direct impact of different energy mixes on global greenhouse gas emissions.
    """)

    st.subheader("2. Displaying CO2 Emissions Based on Energy Mix")
    st.markdown("""
    - Display the amount of CO2 emissions based on any **energy mix** from all sources.
    - Compare and analyze how changes in energy sources affect emissions.
    """)

    st.markdown("By using this tool, students gain valuable insights into the **relationship between energy use and climate change**, helping them better understand the importance of adopting renewable energy solutions.")

    st.markdown("Data is obtained from Our World in Data organization <a href='https://ourworldindata.org/' target='_blank' style='font-size:18px; color:#bf5454;'> 🔗",unsafe_allow_html=True)

with tab2:

    selected_entity = st.selectbox("Select an Entity:", entities)

    selected_year = st.selectbox("Select a Year:", years)

    filtered_co2_data = data_co2[(data_co2['Entity'] == selected_entity) & (data_co2['Year'] == selected_year)]

    if not filtered_co2_data.empty:
        co2_emissions = filtered_co2_data['Annual CO₂ emissions'].values[0]
        st.markdown(
            f"""<div style="text-align: center; font-size: 28px; font-weight: bold; color: #2E86C1; margin-top: 20px;">
            CO₂ Emissions for {selected_entity} in {selected_year}: {co2_emissions} metric tons
            </div>""", unsafe_allow_html=True
        )
    else:
        st.write("No CO₂ data available for the selected entity and year.")

    filtered_energy_data = data_energy[(data_energy['Entity'] == selected_entity) & (data_energy['Year'] == selected_year)]

    if not filtered_energy_data.empty:
        st.write("### Energy Consumption Data (in TWh):")
        energy_columns = [
            "Other renewables (including geothermal and biomass) - TWh",
            "Biofuels consumption - TWh",
            "Solar consumption - TWh",
            "Wind consumption - TWh",
            "Hydro consumption - TWh",
            "Nuclear consumption - TWh",
            "Gas consumption - TWh",
            "Coal consumption - TWh",
            "Oil consumption - TWh"
        ]
        energy_data = filtered_energy_data[energy_columns].iloc[0]

        energy_df = pd.DataFrame({
            "Energy Source": energy_columns,
            "Consumption (TWh)": energy_data.values
        })

        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.write("Energy Consumption Table")
        st.dataframe(energy_df, height=400)
        st.markdown("</div>", unsafe_allow_html=True)

        fig = px.pie(
            energy_df, 
            values="Consumption (TWh)", 
            names="Energy Source",
            title=f"Energy Consumption Breakdown for {selected_entity} in {selected_year}",
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.write("No energy consumption data available for the selected entity and year.")

with tab3:
    st.header("Calculate CO₂ Emissions Based on Energy Mix")
      
    st.write("Enter your annual energy generation by source (in TWh):")
    other_renewables = st.number_input("Other Renewables (e.g. geothermal, tidal, etc.)", min_value=0.0, step=0.1)
    biofuels = st.number_input("Biofuels", min_value=0.0, step=0.1)
    solar = st.number_input("Solar", min_value=0.0, step=0.1)
    wind = st.number_input("Wind", min_value=0.0, step=0.1)
    hydro = st.number_input("Hydro", min_value=0.0, step=0.1)
    nuclear = st.number_input("Nuclear", min_value=0.0, step=0.1)
    gas = st.number_input("Gas", min_value=0.0, step=0.1)
    coal = st.number_input("Coal", min_value=0.0, step=0.1)
    oil = st.number_input("Oil", min_value=0.0, step=0.1)
   
    # -------------------------------------------------------------------------
    # Emission Factors:
    # These are approximate lifecycle values in METRIC TONS of CO₂ per TWh.
    # (Derived from the more common g/kWh by multiplying by 1,000.)
    # -------------------------------------------------------------------------
    emission_factors = {
        "Other Renewables": 25_000,   # e.g., 25 g/kWh => 25,000 t/TWh
        "Biofuels": 75_000,          # e.g., 75 g/kWh => 75,000 t/TWh
        "Solar": 50_000,             # e.g., 50 g/kWh => 50,000 t/TWh
        "Wind": 15_000,              # e.g., 15 g/kWh => 15,000 t/TWh
        "Hydro": 5_000,              # e.g., 5 g/kWh => 5,000 t/TWh
        "Nuclear": 12_000,           # e.g., 12 g/kWh => 12,000 t/TWh
        "Gas": 450_000,              # e.g., 450 g/kWh => 450,000 t/TWh
        "Coal": 900_000,             # e.g., 900 g/kWh => 900,000 t/TWh
        "Oil": 750_000               # e.g., 750 g/kWh => 750,000 t/TWh
    }
   
    # Calculate total emissions (in metric tons of CO₂)
    total_emissions = (
        other_renewables * emission_factors["Other Renewables"] +
        biofuels         * emission_factors["Biofuels"] +
        solar            * emission_factors["Solar"] +
        wind             * emission_factors["Wind"] +
        hydro            * emission_factors["Hydro"] +
        nuclear          * emission_factors["Nuclear"] +
        gas              * emission_factors["Gas"] +
        coal             * emission_factors["Coal"] +
        oil              * emission_factors["Oil"]
    )
   
    # Display result
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 24px; font-weight: bold; 
                    color: #E74C3C; margin-top: 20px;">
            Total CO₂ Emissions: {total_emissions:,.2f} metric tons per year
        </div>
        """,
        unsafe_allow_html=True
    )

with tab4:
    st.title("Contact Information")
    
    st.markdown("""
    If you have any questions or feedback about this tool, feel free to reach out to me!

    ## Developed by Hamzeh Abu Ali
    **MSc Student in Computer Engineering at METU NCC**
    
    You can contact me via email or explore my work on GitHub:
    """)

    # Styled Email Link
    st.markdown("<a href='mailto:hamzeh.abu@metu.edu.tr' style='font-size:18px; color:#1a73e8;'>✉️ Email: hamzeh.abu@metu.edu.tr</a>", unsafe_allow_html=True)

    # Space for separation
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Styled GitHub Link
    st.markdown("<a href='http://your-github-repository-link' target='_blank' style='font-size:18px; color:#bf5454;'>🔗 GitHub Repository</a>", unsafe_allow_html=True)

    st.markdown("""
    I'm always happy to discuss the tool and any improvements or contributions you'd like to make.
    """)
