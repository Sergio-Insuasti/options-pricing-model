import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
def display_binomial_convergence(df: pd.DataFrame):
# --------------------------------
    # Plot
    # --------------------------------
    st.subheader("Binomial Convergence to Black Scholes")
    st.write(
        "This plot visualises how the binomial pricing model converges "
        "to the Black Scholes benchmark under the current parameter assumptions."
    )
    fig, ax = plt.subplots(facecolor="#121212")
    ax.set_facecolor("#121212")
    ax.grid(visible=True)

    window = 7
    df["upper"] = (
        df["relative_deviation"]
        .rolling(window=window, center=True, min_periods=1)
        .max()
    )
    df["lower"] = (
        df["relative_deviation"]
        .rolling(window=window, center=True, min_periods=1)
        .min()
    )

    ax.fill_between(
        df["binomial_steps"],
        df["lower"],
        df["upper"],
        color="#4EA8DE",
        alpha=0.25,
        linewidth=0
    )

    ax.plot(
        df["binomial_steps"],
        df["relative_deviation"],
        color="#4EA8DE",
        linewidth=2.2,
        alpha=0.95
    )

    ax.scatter(
        df["binomial_steps"],
        df["relative_deviation"],
        s=10,
        color="#F4A261",
        alpha=0.6
    )

    ax.axhline(
        0.0,
        color="#E0E0E0",
        linewidth=1,
        alpha=0.8
    )

    ax.set_xlabel(
        "Number of Binomial Steps",
        color="#EAEAEA"
    )
    ax.set_ylabel(
        "Relative deviation (Binomial to Black Scholes)",
        color="#EAEAEA"
    )

    ax.tick_params(
        axis="both",
        colors="#EAEAEA"
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)