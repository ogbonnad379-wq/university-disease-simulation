import pandas as pd


def run_sir(population, initial_infectious, beta, gamma, days):

    if population <= 0:
        raise ValueError("Population must be greater than zero.")

    if not 0 <= initial_infectious <= population:
        raise ValueError("Initial infectious population is invalid.")

    if beta < 0 or gamma < 0:
        raise ValueError("Rates cannot be negative.")

    if days <= 0:
        raise ValueError("Simulation days must be greater than zero.")

    # Initial population compartments
    S = float(population - initial_infectious)
    I = float(initial_infectious)
    R = 0.0

    results = [{
        "Day": 0,
        "Susceptible": S,
        "Infectious": I,
        "Recovered": R,
        "New Infections": 0.0,
        "New Recoveries": 0.0
    }]

    # Run daily simulation
    for day in range(1, days + 1):

        new_infections = min(beta * S * I / population, S)

        new_recoveries = min(gamma * I, I + new_infections)

        S = S - new_infections
        I = I + new_infections - new_recoveries
        R = R + new_recoveries

        results.append({
            "Day": day,
            "Susceptible": S,
            "Infectious": I,
            "Recovered": R,
            "New Infections": new_infections,
            "New Recoveries": new_recoveries
        })

    return pd.DataFrame(results)
