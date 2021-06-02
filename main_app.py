# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd

from Covid19DataHandler import getCovidDataFrame, getCountryList


# define style color
colors = {"background": "#000000", "text": "#ffFFFF"}
external_stylesheets = [dbc.themes.SLATE]

# load date from Johns Hopkins University repository
# data_src = 'time_series_covid19_confirmed_global.csv'
data_src = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
raw_df = pd.read_csv(data_src, sep=',')

# get country list
country_list = getCountryList(df=raw_df.copy(deep=True))

my_meta_tags = [
    {'meta name': 'google-site-verification', 'content': '_UwS9WDWDerzEsP8hN-iypyU8en5R2C7sCboBir2ILQ'}
]

# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=my_meta_tags)
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
                                        "COVID-19確診病例技術分析",
                                        style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },
                                    ),
                                    html.H3(
                                        "Technical Analysis of COVID-19 Confirm Case",
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
                        dbc.Col(  # Country
                            dcc.Dropdown(
                                id="selected-country",
                                options=[
                                    {
                                        "label": str(country_list[i]),
                                        "value": str(country_list[i]),
                                    }
                                    for i in range(len(country_list))
                                ],
                                searchable=True,
                                value='Taiwan*',
                                placeholder="輸入國家 Enter Country",
                            ),
                            width={"size": 3, "offset": 3},
                        ),
                        dbc.Col(  # Graph type
                            dcc.Dropdown(
                                id="chart",
                                options=[
                                    {"label": "每日確診病例數 Line", "value": "Line"},
                                    {"label": "簡單移動平均 Simple Moving Average",
                                        "value": "SMA"},
                                    {
                                        "label": "指數移動平均 Exponential Moving Average",
                                        "value": "EMA",
                                    },
                                    {"label": "指數平滑異同移動平均線 MACD", "value": "MACD"},
                                    {"label": "相對強弱指數 RSI", "value": "RSI"},
                                ],
                                value="Line",
                                style={"color": "#000000"},
                            ),
                            width={"size": 3},
                        ),
                        dbc.Col(  # button
                            dbc.Button(
                                "繪圖 Plot",
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
        * 資料來源 Data source: [COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)
        * 網站原始碼 Site Repository: [Technical-analysis-of-covid19-cases](https://github.com/ravagerWT/Technical-Analysis-of-Covid19-Cases)
        '''
        )
    ],
)

# Callback main graph
@app.callback(
    Output("graph", "figure"),
    Input("submit-button-state", "n_clicks"),
    State("selected-country", "value"),
    State("chart", "value")
)
def graph_generator(n_clicks, selected_country, chart_name):

    if n_clicks >= 1:  # Checking for user to click submit button

        # processing data
        df = getCovidDataFrame(raw_dataframe=raw_df.copy(deep=True), country=selected_country, op_mode=1)

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
                    "title": "每日確診病例數 Line",
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
            close_ma_7 = df.daily_cases.rolling(7).mean()
            close_ma_30 = df.daily_cases.rolling(30).mean()
            close_ma_90 = df.daily_cases.rolling(90).mean()
            close_ma_120 = df.daily_cases.rolling(120).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(df.date), y=list(close_ma_7), name="7 Days"
                    ),
                    go.Scatter(
                        x=list(df.date), y=list(close_ma_30), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(df.date), y=list(close_ma_90), name="90 Days"
                    ),
                    go.Scatter(
                        x=list(df.date), y=list(close_ma_120), name="120 Days"
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": "簡單移動平均 Simple Moving Average",
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
            close_ema_7 = df.daily_cases.ewm(span=7).mean()
            close_ema_30 = df.daily_cases.ewm(span=30).mean()
            close_ema_90 = df.daily_cases.ewm(span=90).mean()
            close_ema_120 = df.daily_cases.ewm(span=120).mean()
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=list(df.date), y=list(close_ema_7), name="7 Days"
                    ),
                    go.Scatter(
                        x=list(df.date), y=list(close_ema_30), name="30 Days"
                    ),
                    go.Scatter(
                        x=list(df.date), y=list(close_ema_90), name="90 Days"
                    ),
                    go.Scatter(
                        x=list(df.date), y=list(close_ema_120), name="120 Days",
                    ),
                ],
                layout={
                    "height": 1000,
                    "title": "指數移動平均 Exponential Moving Average",
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
                    "title": "指數平滑異同移動平均線 MACD",
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
                    "title": "相對強弱指數 RSI",
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
    app.title = 'COVID-19確診病例技術分析 Technical Analysis of COVID-19 Confirm Case'
    app.run_server(debug=True)
