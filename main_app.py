import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from Covid19DataHandler import getCovidDataFrame


# define style color
colors = {"background": "#000000", "text": "#ffFFFF"}

external_stylesheets = [dbc.themes.SLATE]

# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.Br(),
        html.Div(
            [  # header Div
                dbc.Row(
                    [
                        dbc.Col(
                            html.Header(
                                [
                                    html.H1(
                                        "Taiwan COVID-19 Confirm Case Analysis",
                                        style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        ),
        html.Br(),
        html.Div(
            [  # Dropdown Div
                dbc.Row(
                    [
                        dbc.Col(  # Graph type
                            dcc.Dropdown(
                                id="chart",
                                options=[
                                    {"label": "Line", "value": "Line"},
                                    {"label": "Simple Moving Average",
                                        "value": "SMA"},
                                    {
                                        "label": "Exponential Moving Average",
                                        "value": "EMA",
                                    },
                                    {"label": "MACD", "value": "MACD"},
                                    {"label": "RSI", "value": "RSI"},
                                ],
                                value="Line",
                                style={"color": "#000000"},
                            ),
                            width={"size": 3},
                        ),
                        dbc.Col(  # button
                            dbc.Button(
                                "Plot",
                                id="submit-button-state",
                                className="mr-1",
                                n_clicks=1,
                            ),
                            width={"size": 2},
                        ),
                    ]
                )
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="graph",
                                config={
                                    "displaylogo": False,
                                    "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                },
                            ),
                        )
                    ]
                )
            ]
        ),
        dcc.Markdown('''
        * Data source: [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)
        * Site Repository: [Technical-analysis-of-covid19-cases](https://github.com/ravagerWT/technical-analysis-of-covid19-cases)
        '''
        )
    ],
)

# Callback main graph
@app.callback(
    Output("graph", "figure"),
    Input("submit-button-state", "n_clicks"),
    State("chart", "value")
)
def graph_generator(n_clicks, chart_name):

    if n_clicks >= 1:  # Checking for user to click submit button

        # loading data
        # data_src = 'time_series_covid19_confirmed_global.csv'
        data_src = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        df = getCovidDataFrame(data_src)

        # selecting graph type
        # Line plot
        if chart_name == "Line":
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(df.date), y=list(df.daily_cases), fill="tozeroy", name="daily_cases"
                    )
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list([
                            dict(count=7, label="7D",step="day", stepmode="backward"),
                            dict(count=14, label="14D", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all"),
                    ])
                )
            )

        # Simple moving average
        if chart_name == "SMA":
            close_ma_10 = df.daily_cases.rolling(10).mean()
            close_ma_15 = df.daily_cases.rolling(15).mean()
            close_ma_30 = df.daily_cases.rolling(30).mean()
            close_ma_100 = df.daily_cases.rolling(100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ma_10.index), y=list(close_ma_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_15.index), y=list(close_ma_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_30.index), y=list(close_ma_15), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ma_100.index), y=list(close_ma_15), name="100 Days"
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list([
                            dict(count=7, label="7D",step="day", stepmode="backward"),
                            dict(count=14, label="14D", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all"),
                    ])
                )
            )

        # Exponential moving average
        if chart_name == "EMA":
            close_ema_10 = df.daily_cases.ewm(span=10).mean()
            close_ema_15 = df.daily_cases.ewm(span=15).mean()
            close_ema_30 = df.daily_cases.ewm(span=30).mean()
            close_ema_100 = df.daily_cases.ewm(span=100).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(close_ema_10.index), y=list(close_ema_10), name="10 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_15.index), y=list(close_ema_15), name="15 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_30.index), y=list(close_ema_30), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(close_ema_100.index),
                        y=list(close_ema_100),
                        name="100 Days",
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list([
                            dict(count=7, label="7D",step="day", stepmode="backward"),
                            dict(count=14, label="14D", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all"),
                    ])
                )
            )

        # Moving average convergence divergence
        if chart_name == "MACD":
            fig = go.Figure(
                data=[
                    go.Scatter(x=list(df.date), y=list(df.MACD), name="MACD"),
                    go.Scatter(x=list(df.date), y=list(
                        df.MACDs), name="Signal"),
                    go.Scatter(
                        x=list(df.date),
                        y=list(df['MACDh']),
                        line=dict(color="royalblue", width=2, dash="dot"),
                        name="Hitogram",
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list([
                            dict(count=7, label="7D",step="day", stepmode="backward"),
                            dict(count=14, label="14D", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all"),
                    ])
                )
            )
        
        # Relative Strength Index
        if chart_name == "RSI":
            rsi_6 = df['RSI_6']
            rsi_12 = df['RSI_12']
            fig = go.Figure(
                data=[
                    go.Scatter(x=list(df.date), y=list(
                        rsi_6), name="RSI 6 Day"),
                    go.Scatter(x=list(df.date), y=list(
                        rsi_12), name="RSI 12 Day"),
                ],
                layout={
                    "height": 1000,
                    "title": chart_name,
                    "xaxis_title" : 'Dates',                    
                    "showlegend": True,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )

            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    activecolor="blue",
                    bgcolor=colors["background"],
                    buttons=list([
                            dict(count=7, label="7D",step="day", stepmode="backward"),
                            dict(count=14, label="14D", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=3, label="3m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(step="all"),
                    ])
                )
            )
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
