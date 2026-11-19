import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sir_model import run_sir

st.set_page_config(
    page_title="University Disease Simulator",
    page_icon="🦠",
    layout="wide"
)

st.title("University Disease Transmission Simulator")

st.write(
    "Explore how infectious diseases spread through "
    "a hypothetical university community using the SIR model."
)

st.info(
    "This application produces simulated results, "
    "not actual university disease statistics."
)

st.sidebar.header("Simulation Parameters")

population = st.sidebar.number_input(
    "Total Population",
    min_value=1,
    value=1000
)

initial_infectious = st.sidebar.number_input(
    "Initial Infectious Population",
    min_value=0,
    value=10
)

beta = st.sidebar.number_input(
    "Transmission Rate (β)",
    min_value=0.0,
    value=0.3,
    step=0.05
)

gamma = st.sidebar.number_input(
    "Recovery Rate (γ)",
    min_value=0.0,
    value=0.1,
    step=0.05
)

days = st.sidebar.number_input(
    "Simulation Duration (Days)",
    min_value=1,
    value=30
)

if st.sidebar.button("Run Simulation"):

    if initial_infectious > population:
        st.error("Initial infectious population cannot exceed total population.")

    else:
        results = run_sir(
            int(population),
            int(initial_infectious),
            float(beta),
            float(gamma),
            int(days)
        )

        st.success("Simulation completed successfully!")

        final = results.iloc[-1]

        peak_index = results["Infectious"].idxmax()
        peak = results.loc[peak_index]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Final Susceptible",
            f"{final['Susceptible']:.2f}"
        )

        col2.metric(
            "Final Infectious",
            f"{final['Infectious']:.2f}"
        )

        col3.metric(
            "Final Recovered",
            f"{final['Recovered']:.2f}"
        )

        st.subheader("Infection Summary")

        st.write(
            f"Peak infectious population: "
            f"{peak['Infectious']:.2f}"
        )

        st.write(
            f"Peak infection day: {int(peak['Day'])}"
        )

        st.subheader("Disease Transmission Trend")

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(results["Day"], results["Susceptible"], label="Susceptible")
        ax.plot(results["Day"], results["Infectious"], label="Infectious")
        ax.plot(results["Day"], results["Recovered"], label="Recovered")

        ax.set_xlabel("Days")
        ax.set_ylabel("Population")
        ax.set_title("SIR Disease Transmission Simulation")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        st.subheader("Daily Simulation Results")

        st.dataframe(results, use_container_width=True)

        csv = results.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="disease_simulation_results.csv",
            mime="text/csv"
        )
