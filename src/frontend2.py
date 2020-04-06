import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas
import os
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc


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
    return html.Div([dbc.Modal(
        children=[
            dbc.ModalHeader(
                html.P("Workflow"),
            ),
            dbc.ModalBody(
                dbc.Row(
                    [
                        dbc.Col(
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
                            ),
                            md=6,
                            className="col-md-6"
                            # align="left"
                        ),
                        dbc.Col(
                            [
                                html.P(
                                    "Twitter Bot Detection",
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
                            # align="right"
                        ),
                    ]
                )
            ),
            dbc.ModalFooter(
                dbc.Button("Run!", id="run", className="mr-2", n_clicks=0)
            )],
        size="lg",
        id="modal"
    )
    ])


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
    )
