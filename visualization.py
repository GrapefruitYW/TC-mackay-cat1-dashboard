import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from typing import Tuple

def create_sankey_chart(df, threshold: int,window) -> go.Figure:
    """Create the Sankey chart showing patient conversion flow."""

    # filter for category 1
    df_cat1 = df[df['Category'].astype(str) == '1']

    # calculate key metrics
    x_cat1 = len(df_cat1)
    x_booked = len(df[~df_cat1['Appointment Date'].isnull()])
    x_unbooked = x_cat1-x_booked
    x_overthreshold = len(df_cat1[df_cat1[window] > threshold])
    x_underthreshold = x_booked - x_overthreshold


    fig = go.Figure(go.Sankey(
        node = dict(
            label = ["Cat1 patients","Booked","Unbooked",f"Over {threshold} days",f"Under {threshold} days"],
        ),
        link = dict(
            source = [0, 0, 1, 1], 
            target = [1, 2, 3, 4],
            value = [x_booked, x_unbooked, x_overthreshold, x_underthreshold],
            customdata = ["78.7%","21.3%","13.9%","7.4%"],
            hovertemplate='<br />%{value} patients' +
                '<br />%{customdata} of total cat1 patients<extra></extra>',
        )
    ))
    fig.update_layout(title_text="Conversion summary of patients", font_size=14)
    return fig

def create_conversion_plot(df: pd.DataFrame, window: str, threshold: int) -> Tuple[plt.Figure, plt.Axes]:
    """Create histogram plot of conversion times."""
    fig, ax = plt.subplots()
    ax.hist(df[window], bins=30, alpha=0.75, color='#0552F0', edgecolor='#171D4D')
    ax.axvline(x=threshold, color='red', linestyle='--', label=f'Threshold ={threshold}')
    ax.set_xlabel("Number of days")
    ax.set_ylabel("Number of patients")
    ax.set_title(f"Distribution of {window} times")
    ax.legend(fontsize=8)
    return fig, ax
