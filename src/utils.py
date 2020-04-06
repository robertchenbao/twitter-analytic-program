import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas
import os
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc


def select_train(file_name):
    DATA_DIR = os.path.dirname('/Users/robertbao/Documents/2019_SF/')

    TRAIN_DIR = os.path.join(DATA_DIR, "train")
    return os.path.join(TRAIN_DIR, file_name)


# Get all content of the top together
def Header():
    return html.Div([get_header(), html.Br([]), get_menu()])


def get_header():  # Get the header (TAP header and the background). Row 1
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.H5("Calibre Financial Index Fund Investor Shares")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href="/dash-financial-report/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )


def get_menu():  # Get the content of the menu bar. Row 2
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/tap/overview",
                className="tab first",
            ),
            dcc.Link(
                "Quantity",
                href="/tap/quantity",
                className="tab",
            ),
            dcc.Link(
                "Sentiment",
                href="/tap/sentiment",
                className="tab"
            ),
            dcc.Link(
                "Procedure",
                href="/tap/procedure",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


# Input: a data-set (pandas data-frame)
# Output: Display the average sentiment on the dashboard.
def get_average_sentiment(data):
    pass


def get_vectorizer():
    pass


# returns top indicator div
# def indicator(text, id_value):
#     return html.Div(
#         [
#             html.P(id=id_value, className="indicator_value"),
#             html.P(text, className="twelve columns indicator_text"),
#         ],
#         className="four columns indicator pretty_container",
#     )


def indicator(number, description):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(str(number), className="card-title"),
                    html.P(str(description), className="card-text"),
                ]
            ),
            # dbc.CardFooter("This is the footer"),
        ],
        style={"width": "18rem"},
    )


def modal():
    return html.Div(
        html.Div(
            [
                html.Div(
                    [
                        # modal header
                        html.Div(
                            [
                                html.Span(
                                    "Workflow",

                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="modal_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # modal form
                        html.Div(
                            [
                                # left Div
                                html.Div(
                                    [
                                        dcc.Upload(
                                            id="upload-data",
                                            children=[
                                                "Drag and Drop or ",
                                                html.A(children="Select a CSV file."),
                                            ],
                                            style={
                                                'width': '98%',
                                                'height': '100px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                            },
                                            multiple=True
                                        ),
                                        html.Div(
                                            id='output-data-upload',
                                        ),

                                        # General Text Cleaning
                                        # html.P(
                                        #     "Text Cleaning",
                                        #     style={
                                        #         "textAlign": "left",
                                        #         "marginBottom": "2",
                                        #         "marginTop": "4",
                                        #     },
                                        # ),
                                        # html.P(
                                        #     "In order to ensure the accuracy of the algorithm, we remove "
                                        #     "noise in the data. We remove URL links, user  and hashtags. "
                                        #     "We also fix punctuation errors like multiple periods. These "
                                        #     "data cleaning methods can greatly improve the accuracy of the "
                                        #     "sentiment analysis of the machine learning model of your choice."
                                        # ),
                                    ],
                                    className="six columns",
                                    style={"paddingRight": "15"},

                                ),
                                # right Div
                                html.Div(
                                    [
                                        # # Vectorizer
                                        # html.P(
                                        #     "Vectorizer",
                                        #     style={
                                        #         "textAlign": "left",
                                        #         "marginBottom": "2",
                                        #         "marginTop": "4",
                                        #     },
                                        # ),
                                        # dcc.Dropdown(
                                        #     id="vectorizer",
                                        #     options=[
                                        #         {'label': 'Count Vectorizer', 'value': 'count'},
                                        #         {'label': 'TF-IDF Vectorizer', 'value': 'tfidf'},
                                        #     ],
                                        #     value='TfidfVectorizer',
                                        #     clearable=False,
                                        # ),

                                        # Twitter Bot Detection
                                        html.P(
                                            "Twitter Bot Detection",
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="bot_detection",
                                            options=[
                                                {'label': 'Enable Bot Detection', 'value': 'Bot'},
                                                {'label': 'Disable Bot Detection', 'value': 'No_Bot'},
                                            ],
                                            value='Bot',
                                            clearable=False,
                                        ),

                                        html.P(
                                            "Sentiment Analysis Model",
                                            style={
                                                "textAlign": "left",
                                                "marginBottom": "2",
                                                "marginTop": "4",
                                            },
                                        ),

                                        # Sentiment models
                                        html.Div(
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
                                                value="logistic",
                                            )
                                        ),
                                    ],
                                    className="six columns",
                                    style={"paddingLeft": "15"},
                                ),
                            ],
                            style={"marginTop": "10", "textAlign": "center", "marginBottom": "10"},
                            className="row",
                        ),

                        # submit button
                        html.Span(
                            "Run!",
                            id="run",
                            n_clicks=0,
                            className="button button--primary add"
                        ),

                    ],
                    className="modal-content",
                    style={"textAlign": "center", "border": "1px solid #C8D4E3"},
                )
            ],
            className="modal",
        ),
        id="modal",
        style={"display": "none"},
    )


# def make_dash_table(df):
#     return dash_table.DataTable(
#         id='table',
#         columns=[{"name": i, "id": i} for i in df.columns],
#         data=df.to_dict('records'),
#     )


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def modal_switch():
    # The switch for the modal
    return html.Div(
        [
            # add button
            html.Div(
                html.Span(
                    "New workflow",
                    id="new_workflow",
                    n_clicks=0,
                    className="button button--primary add"
                ),
                className="two columns",
                style={"float": "right"},
            )
        ],
        className="row",
        style={"marginBottom": "10"},
    )
