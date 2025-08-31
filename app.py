import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# the path to the formatted data file
DATA_PATH = "./formatted_sales.csv"
COLORS = {
    "primary": "#FEDBFF",
    "secondary": "#D598EB",
    "font": "#522A61"
}

# load in data
data = pd.read_csv(DATA_PATH)
data["date"] = pd.to_datetime(data["date"])
data = data.sort_values(by="date")

# initialize dash
dash_app = Dash(__name__)

# create the visualization
def generate_figure(chart_data, title="Pink Morsel Sales"):
    line_chart = px.line(chart_data, x="date", y="sales", title=title)
    line_chart.update_layout(
        plot_bgcolor=COLORS["secondary"],
        paper_bgcolor=COLORS["primary"],
        font_color=COLORS["font"]
    )
    return line_chart

# initial visualization
visualization = dcc.Graph(
    id="visualization",
    figure=generate_figure(data.groupby("date", as_index=False)["sales"].sum(), "Total Sales (All Regions)")
)

# create the header
header = html.H1(
    "Pink Morsel Visualizer",
    id="header",
    style={
        "background-color": COLORS["secondary"],
        "color": COLORS["font"],
        "border-radius": "20px",
        "padding": "10px"
    }
)

# region picker
region_picker = dcc.RadioItems(
    id="region_picker",
    options=["north", "east", "south", "west", "all"],
    value="all",
    inline=True,
    style={"margin": "20px"}
)

# define the region picker callback
@dash_app.callback(
    Output("visualization", "figure"),
    Input("region_picker", "value")
)
def update_graph(region):
    if region == "all":
        trimmed_data = data.groupby("date", as_index=False)["sales"].sum()
        return generate_figure(trimmed_data, "Total Sales (All Regions)")
    else:
        trimmed_data = data[data["region"] == region].groupby("date", as_index=False)["sales"].sum()
        return generate_figure(trimmed_data, f"Sales in {region.title()} Region")

# define the app layout
dash_app.layout = html.Div(
    [
        header,
        visualization,
        region_picker
    ],
    style={
        "textAlign": "center",
        "background-color": COLORS["primary"],
        "border-radius": "20px",
        "padding": "20px"
    }
)

# run app
if __name__ == '__main__':
    dash_app.run(debug=True, host="0.0.0.0", port=8050)
