import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas
import os
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc


# Get all content of the top together


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


# # returns top indicator div
# def indicator(number, description):
#     return html.Div(
#         [
#             html.H4(number, className="indicator_value"),
#             html.P(description, className="four columns indicator_text"),
#             html.Br(),
#             html.Br(),
#         ],
#         className="four columns indicator pretty_container",
#     )


def indicator(number, description):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(str(number), className="card-title"),
                    html.P(str(description), className="card-text"),
                ]
            ),
        ],
        # style={"width": "18rem"},
    )


def modal():
    return dbc.Modal(
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
                                        )
                                    ],
                                    className="six columns",
                                    style={"paddingRight": "15"},

                                ),
                                # right Div
                                html.Div(
                                    [
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


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


# def modal_switch():
#     # The switch for the modal
#     return html.Div(
#         [
#             # add button
#             html.Div(
#                 html.Span(
#                     "New workflow",
#                     id="new_workflow",
#                     n_clicks=0,
#                     className="button button--primary add"
#                 ),
#                 className="two columns",
#                 style={"float": "right"},
#             )
#         ],
#         className="row",
#         style={"marginBottom": "10"},
#     )


def modal_switch():
    # The switch for the modal
    return html.Div(
        dbc.Button(
            "New workflow",
            id="new_workflow",
            n_clicks=0,
            className="mr-1"
        ),
        style={"float": "right"},
    )
