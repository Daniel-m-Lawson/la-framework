"""Provides LaPlot utility for visualizing LaList of LaKline data with Plotly."""

from datetime import datetime
from typing import Optional

import plotly.graph_objects as go
from ..core import LaList, LaKline


class LaPlotKline:
    """Utility class to visualize LaList data using Plotly."""

    def __init__(self, title: str = "Framework Plot"):
        self.fig = go.Figure()
        self.fig.update_layout(
            title=title,
            xaxis_title="Time",
            template="plotly_dark",
            # We set this to False initially, but it can be toggled by methods
            xaxis_rangeslider_visible=False,
        )

    def add_kline_list(self, data: LaList[LaKline], name: str = "Price"):
        """Adds a candlestick trace and enables the rangeslider."""
        self.fig.add_trace(
            go.Candlestick(
                x=[item.open_time for item in data],
                open=[item.open for item in data],
                high=[item.high for item in data],
                low=[item.low for item in data],
                close=[item.close for item in data],
                name=name,
            )
        )
        # Financial charts almost always need the rangeslider for zooming
        self.add_rangeslider(True)
        return self

    def add_rangeslider(self, visible: bool = True):
        """
        Toggles the rangeslider window at the bottom of the graph.

        Args:
            visible: Whether to show or hide the slider.
        """
        self.fig.update_layout(xaxis_rangeslider_visible=visible)
        return self

    def show(self):
        """Renders the plot."""
        self.fig.show()


BINANCE_COLORS = [
    "#F3BA2F",  # Binance yellow (highlight)
    "#1E2329",
    "#2B3139",
    "#3A4149",
    "#4A535D",
    "#5C6670",
    "#6E7882",
    "#848E9C",
    "#A7B1BC",
    "#C2C9D1",
]


class LaPlotTimeSeries:
    """Utility class for plotting time series of coins or other data."""

    def __init__(self, title: Optional[str] = "Time Series"):
        self.fig = go.Figure()
        self.fig.update_layout(
            title=title or "",  # ensure str, not None
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Market Cap (USD)",
            xaxis=dict(rangeslider=dict(visible=True)),  # show rangeslider
            font=dict(color="white"),
        )

    def add_series(
        self,
        dates: list[datetime],
        values: list[float],
        name: str,
        color: Optional[str] = None,
    ):
        """Add a line series to the plot."""
        self.fig.add_trace(
            go.Scatter(
                x=dates,
                y=values,
                mode="lines+markers",
                name=name or "",  # ensure str
                line=dict(color=color or BINANCE_COLORS[0], width=2),
            )
        )
        return self

    def show(self):
        """Render the plot."""
        self.fig.show()


class LaPlotPie:
    """Utility class to create Binance-themed pie charts using Plotly."""

    def __init__(self, title: str = "Market Cap Distribution"):
        self.fig = go.Figure()
        self.fig.update_layout(
            title=title,
            template="plotly_dark",
            font=dict(color="white"),
        )

    def add_data(
        self,
        data: dict[str, float],
        name: str = "Distribution",
        display: str = "percent",  # percent | value | both | none
    ):
        labels = list(data.keys())
        values = list(data.values())

        colors = [BINANCE_COLORS[i % len(BINANCE_COLORS)] for i in range(len(labels))]

        # Format hover + text display
        if display == "percent":
            textinfo = "label+percent"
            texttemplate = None
        elif display == "value":
            textinfo = "label"
            texttemplate = "%{label}<br>$%{value:,.0f}"
        elif display == "both":
            textinfo = "label+percent"
            texttemplate = "%{label}<br>%{percent}<br>$%{value:,.0f}"
        else:  # "none"
            textinfo = "none"
            texttemplate = None

        self.fig.add_trace(
            go.Pie(
                labels=labels,
                values=values,
                name=name,
                marker=dict(
                    colors=colors,
                    line=dict(color="#111111", width=1),
                ),
                hole=0.35,
                textinfo=textinfo,
                texttemplate=texttemplate,
                hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
            )
        )

        return self

    def show(self):
        self.fig.show()
