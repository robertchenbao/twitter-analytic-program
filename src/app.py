# The app.
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from src.backend import pipeline
import base64
import io
from dash.dependencies import Input, Output, State
import dash
import pandas as pd
from dash.exceptions import PreventUpdate
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], server=server,
                assets_folder="/Users/robertbao/Documents/2019_IF/assets", )
app.config.suppress_callback_exceptions = True
app.title = "Twitter Analytic Program"


def indicator(number, description):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H3(str(number), className="card-title"),
                    html.P(str(description), className="card-text"),
                ]
            ),
        ],
    )


modal = html.Div([dbc.Modal(
    children=[
        # dbc.ModalHeader(
        #     html.H5("Workflow",
        #             className="text-center"
        #             ),
        #     className="d-block"
        # ),
        dbc.ModalHeader("Workflow"),
        dbc.ModalBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P("Data Upload"),
                            dcc.Upload(
                                id="upload-data",
                                children=[
                                    "Drag and Drop or ",
                                    html.A(children="Select a CSV file."),
                                ],
                                style={
                                    'width': '100%',
                                    'height': '136px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                }
                            ),
                        ],
                        md=6,
                        className="col-md-6"
                    ),
                    dbc.Col(
                        [
                            html.P("Twitter Bot Detection"),
                            dcc.Dropdown(
                                id="bot_detection",
                                options=[
                                    {'label': 'Enable Bot Detection', 'value': 'Bot'},
                                    {'label': 'Disable Bot Detection', 'value': 'No_Bot'},
                                ],
                                value='Bot',
                                clearable=False,
                            ),
                            html.Br(),
                            html.P(
                                "Sentiment Analysis Model",
                            ),
                            dcc.Dropdown(
                                id="sentiment_model",
                                options=[
                                    {
                                        "label": "Logistic Regression",
                                        "value": "logistic",
                                    },
                                    {
                                        "label": "SGD Classifier",
                                        "value": "sgd",
                                    },
                                    {
                                        "label": "Multinomial Naive Bayes",
                                        "value": "mnb",
                                    },
                                    {
                                        "label": "Bernoulli Naive Bayes",
                                        "value": "bnb",
                                    }
                                ],
                                clearable=False,
                                value="logistic"),
                        ],
                        md=6,
                        className="col-md-6"
                    ),
                ]
            )
        ),
        dbc.ModalFooter(
            dbc.Button("Run!", id="run", className="mr-2", color="warning", n_clicks=0)
        )],
    size="lg",
    id="modal"
)
])

navbar2 = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.Button(
                "New workflow",
                id="new_workflow",
                n_clicks=0,
                color="warning",
                className="ml-2",
            )
        ),
    ],
    brand="Twitter Analytic Program",
    color="#10316b",
    dark=True,
    sticky="top",
)

left_column = dbc.Jumbotron(
    [
        html.H4(children="Data Facts", className="display-4"),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(html.Div(id="overview_indicator_quantity"), width=6),
                dbc.Col(html.Div(id="overview_indicator_sentiment"), width=6)
            ],
            className="my-4"
        ),
        html.Hr(className="my-2"),
        dbc.Row(
            [
                dbc.Col(html.Div(id="overview_indicator_interval"), width=6),
                dbc.Col(html.Div(id="quantity_indicator_user_number"), width=6)
            ],
            className="my-4"
        ),
        html.Hr(className="my-2"),
        dbc.Row(
            dbc.Col(
                dcc.Loading(dcc.Graph(id='pie_chart', config={"displaylogo": False}), type="default"), width=12,
                className="my-4"
            )
        ),
    ],
    className="py-3"
)

right_column = dbc.Container(
    [
        dcc.Tabs(
            id="tabs",
            children=[
                dcc.Tab(
                    label="Quantitative Analysis",
                    children=[
                        dcc.Loading(
                            id="loading-treemap",
                            children=[
                                dcc.Graph(id="quantity-map-1", config={"displaylogo": False}),
                                dcc.Graph(id="quantity-line-chart-1", config={"displaylogo": False})
                            ],
                            type="default",
                        )
                    ],
                ),
                dcc.Tab(
                    label="Sentiment Analysis",
                    children=[
                        dcc.Loading(
                            id="loading-wordcloud",
                            children=[
                                dcc.Graph(id="sentiment-map-1", config={"displaylogo": False}),
                                dcc.Graph(id="sentiment-line-chart-1", config={"displaylogo": False})
                            ],
                            type="default",
                        )
                        # html.Hr(className="my-2"),
                        # dcc.Graph(id="sentiment-map-1"),
                        # dcc.Graph(id="sentiment-line-chart-1")
                    ],
                ),
            ],
        )
    ],
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(left_column, md=5),
                dbc.Col(right_column, md=7),
            ],
            style={"marginTop": 30},
        ),
    ],
    className="mt-12",
)

app.layout = html.Div(
    [
        modal,
        navbar2,
        body,
        dcc.Store(id="data-df"),
    ]
)


# Uploaded data --> Hidden Data Div
@app.callback(
    Output("data-df", "data"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename"),
     Input("sentiment_model", "value"),
     Input("run", "n_clicks")],
)
def parse_data(list_of_contents, list_of_names, sentiment_model, n_clicks):
    if list_of_contents is not None and n_clicks > 0:
        content_type, content_string = list_of_contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in list_of_names:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in list_of_names:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        # print(df.head(10))
        df = df.drop_duplicates()
        df = df.dropna()
        df = pipeline(df, clf=sentiment_model)
        return df.to_json(orient="split")
    elif n_clicks is None:
        raise PreventUpdate
    else:
        return html.Div([
            'There was an error processing this file.'
        ])


# Name: sentiment_indicator
# Input: a pandas data-frame. Its sentiment is already analyzed.
# Output: an indicator (big text) of the average sentiment.
# ---------------
@app.callback(Output(component_id="overview_indicator_sentiment", component_property="children"),
              [Input(component_id="data-df", component_property="data")])
def sentiment_indicator(df):
    if type(df) is not dict:
        df = pd.read_json(df, orient="split")
        sentiment = df["sentiment"].mean().round(2)
        return indicator(number=sentiment, description="Sentiment Index")


# Name: interval_indicator
# Input: a pandas data-frame. May be not analyzed yet.
# Output: an indicator (big text) of the interval of the research
# ---------------
# It subtracts the last date of the tweet by the first date.
# Then, it output the result on Page 1 - Overview.
@app.callback(Output("overview_indicator_interval", "children"), [Input("data-df", "data")])
def interval_indicator(df):
    if type(df) is not dict:
        df = pd.read_json(df, orient="split")
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')
        time = df.iat[(len(df.index) - 1), 0] - df.iat[0, 0]
        day = str(time.days)
        return indicator(number="{} Days".format(day), description="Research Interval")


# Name: quantity_indicator
# Input: a pandas data-frame. May be not analyzed yet.
# Output: an indicator (big text) of the total quantity of tweets.
# ---------------
# It gets the total number of rows in the data file.
# Then, it output the result on Page 1 - Overview.
@app.callback(
    Output("overview_indicator_quantity", "children"),
    [Input("data-df", "data")])
def quantity_indicator(df):
    # if df is not None:
    if type(df) is not dict:
        df = pd.read_json(df, orient="split")
        quantity = len(df.index)
        # return dcc.Markdown("**{}**".format(quantity))
        return indicator(number=quantity, description="Tweet Quantity")


@app.callback(Output('quantity-map-1', 'figure'),
              [Input("run", "n_clicks"),
               Input("data-df", "data")
               ])
def quantity_map_1(n_clicks, df):
    if (n_clicks is None) or (type(df) is dict) or (df is None):
        raise PreventUpdate
    else:
        # print(type(df))
        df = pd.read_json(df, orient="split")
        df = df.groupby('state_name').size().reset_index(name='quantity')
        df['state_name'] = df['state_name'].str.upper()

        # scl = [[-1.0, "rgb(38, 78, 134)"], [1.0, "#0091D5"]]  # colors scale

        data = [
            dict(
                locations=df['state_name'],
                z=df["quantity"],
                locationmode="USA-states",  # Done
                colorscale="Blues",
                reversescale=True,
                autocolorscale=False,
                text=df['quantity'],
                type="choropleth",
                marker_line_color='white',
                # colorbar_title="Millions USD"
            )
        ]

        layout = dict(
            # title='Quantity of Tweets in the US',
            title=dict(text="Quantity of Tweets in the US", y=0.95),
            font=dict(
                family="Roboto, sans-serif",
            ),
            autosize=True,
            geo=dict(
                scope="usa",
                projection=dict(type="albers usa"),
                lakecolor="rgb(255, 255, 255)",
            ),
            margin=dict(l=10, r=10, t=0, b=0),
            height=400,
        )
        return dict(data=data, layout=layout)


@app.callback(
    Output("pie_chart", "figure"),
    [Input("run", "n_clicks"),
     Input("data-df", "data")
     ])
def sentiment_pie_chart_1(n_clicks, df):
    if (n_clicks is None) or (type(df) is dict) or (df is None):
        raise PreventUpdate
    else:
        # print(type(df))
        df = pd.read_json(df, orient="split")
        quantity_df = df.groupby('sentiment').size().reset_index(name='quantity')
        data = {
                   "values": quantity_df['quantity'],
                   "labels": ['Negative', 'Positive'],
                   "name": "Sentiment",
                   "hoverinfo": "label+percent+name",
                   "hole": .3,
                   "type": "pie"
               },
        layout = {
            "title": "Positive and Negative Tweet Percentage",
            'font': dict(
                family="Roboto, sans-serif",
            ),
            'height': 360,
        }
    return dict(data=data, layout=layout)


@app.callback(
    Output("sentiment-line-chart-1", "figure"),
    [Input("run", "n_clicks"),
     Input("data-df", "data")
     ])
def sentiment_line_chart_1(n_clicks, df):
    if (n_clicks is None) or (type(df) is dict) or (df is None):
        raise PreventUpdate
    else:
        # print(type(df))
        df = pd.read_json(df, orient="split")
        # Group the sentiment by date
        df.Index = pd.to_datetime(df['date'])
        day = df.Index.dt.date

        sentiment_df = df.groupby(day).sentiment.mean().reset_index(name='sentiment')
        sentiment_df.sentiment = sentiment_df.sentiment.round(2)
        # print("----------")
        # print(sentiment_df)
        data = {
                   "x": sentiment_df['date'],
                   "y": sentiment_df['sentiment'],
                   "name": "Sentiment",
                   "hoverinfo": "y+name",
                   "line": dict(shape="spline")
               },
        layout = {
            "title": "US Twitter Sentiment Trend",
            'height': 400,
            'font': dict(
                family="Roboto, sans-serif",
            )

        }
    return dict(data=data, layout=layout)


@app.callback(
    Output("quantity-line-chart-1", "figure"),
    [Input("run", "n_clicks"),
     Input("data-df", "data")
     ])
def quantity_line_chart_1(n_clicks, df):
    if (n_clicks is None) or (type(df) is dict) or (df is None):
        raise PreventUpdate
    else:
        # print(type(df))
        df = pd.read_json(df, orient="split")
        # Group the sentiment by date
        df.Index = pd.to_datetime(df['date'])
        day = df.Index.dt.date
        quantity_df = df.groupby(day).text.size().reset_index(name='quantity')
        # print("----------")
        # print(quantity_df)
        data = {
                   "x": quantity_df['date'],
                   "y": quantity_df['quantity'],
                   "name": "Quantity",
                   "hoverinfo": "y+name",
                   "line": dict(shape="spline")
               },
        layout = {
            "title": "US Tweet Quantity Trend",
            'height': 400,
            'font': dict(
                family="Roboto, sans-serif",
            )
        }
    return dict(data=data, layout=layout)


@app.callback(Output('sentiment-map-1', 'figure'),
              [Input("run", "n_clicks"),
               Input("data-df", "data")
               ])
def sentiment_map_1(n_clicks, df):
    if (n_clicks is None) or (type(df) is dict) or (df is None):
        raise PreventUpdate
    else:
        print(type(df))
        df = pd.read_json(df, orient="split")
        # df = df.groupby('state_name').size().reset_index(name='quantity')
        df = df.groupby('state_name').sentiment.mean().reset_index(name='sentiment')
        df.sentiment = df.sentiment.round(2)

        df['state_name'] = df['state_name'].str.upper()

        data = [
            dict(
                locations=df['state_name'],
                z=df["sentiment"],
                locationmode="USA-states",  # Done
                colorscale="YlGnBu",
                # reversescale=True,
                autocolorscale=False,
                text=df['sentiment'],
                type="choropleth",
                marker_line_color='white',
            )
        ]

        layout = dict(
            # title='Sentiment of Tweets in the US',
            title=dict(text="Sentiment of Tweets in the US", y=0.95),
            font=dict(
                family="Roboto, sans-serif",
            ),
            height=400,
            autosize=True,
            geo=dict(
                scope="usa",
                projection=dict(type="albers usa"),
                lakecolor="rgb(255, 255, 255)",
            ),
            margin=dict(l=10, r=10, t=0, b=0),
        )
        return dict(data=data, layout=layout)


# if new_workflow is clicked.
#   show modal
# if run is clicked
# hide modal
@app.callback(
    Output("modal", "is_open"),
    [Input("new_workflow", "n_clicks"), Input("run", "n_clicks")],
    [State("modal", "is_open")], )
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    elif n1 == 0:
        return not is_open
    return is_open


@app.callback(
    Output("quantity_indicator_user_number", "children"),
    [Input("data-df", "data")])
def user_number_indicator(df):
    # if df is not None:
    if type(df) is not dict:
        df = pd.read_json(df, orient="split")
        user = df['name'].nunique()
        # return dcc.Markdown("**{}**".format(quantity))
        return indicator(number=user, description="User Number")


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server()
