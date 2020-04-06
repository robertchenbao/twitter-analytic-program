# This is the demo for my overview page.
# THIS ONE IS WORKING!!! OMG!

import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from src.frontend import modal, modal_switch, indicator, get_header, get_menu
import dash_table
from src.backend import pipeline
import base64
import io
from dash.dependencies import Input, Output, State
import dash
import pandas as pd
from dash.exceptions import PreventUpdate

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    assets_folder="/Users/robertbao/Documents/2019_IF/assets",
)

# app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        # html.Div(id="data-df", style={"display": "none"}),
        # dcc.Store(id="data-df"),
        modal(),

        # Row 1 and 2: Title and Menu
        html.Div([get_header(), html.Br([]), get_menu()]),

        html.Div(
            [
                # Row 3: Big facts (indicators) and introduction paragraph
                html.Div(
                    [
                        modal_switch(),
                        html.Div(
                            [
                                # Big facts
                                html.H5("Data Facts"),
                                html.Br([]),
                                html.Div(id="overview_indicator_quantity"),
                                html.Div(id="overview_indicator_sentiment"),
                                html.Div(id="overview_indicator_interval")
                            ],
                            className="product",
                        ),
                        # Intro paragraph
                        html.Div(
                            [
                                html.H5("Introduction"),
                                html.P(
                                    "This is the introduction paragraph of this data science project."
                                )
                            ],
                            className="product",
                        )
                    ],
                    className="row",
                ),
                # Row 4: Quantity map and sentiment pie chart
                html.Div(
                    [
                        html.H6(
                            "US Quantity Heat Map",
                            className="subtitle padded",
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='quantity-map-1')
                            ],
                            className="product",
                        ),
                    ],
                    className="row",
                    style={"margin-bottom": "35px"},
                ),

                # Row 5: Sentiment map
                html.Div(
                    html.Div(
                        [
                            html.H6(
                                "US Sentiment Heat Map",
                                className="subtitle padded",
                            ),
                            # TODO: US Sentiment map goes here!
                            dcc.Graph(id='sentiment-map-1')
                        ],
                        className="product",
                    ),
                    className="row",
                    style={"margin-bottom": "35px"},
                ),

                # The data is stored here!
                dcc.Store(id="data-df"),
                # # Row 6: Tweet Data table
                # html.Div(
                #     [
                #         # Data table made with Dash component goes here
                #         html.H6("Twitter Data Table"),
                #         html.Div(
                #             # TODO: Make dash table here!
                #             # make_dash_table(id=),
                #             id="data-table",
                #             className="tiny-header",
                #         ),
                #     ],
                #     className="six columns",
                # ),
            ],
            className="sub_page",
        ),
    ],
    className="page",
)


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    # print(df.head(10))
    return df


# Uploaded data --> Hidden Data Div
@app.callback(
    Output("data-df", "data"),
    [Input("upload-data", "contents"),
     Input("upload-data", "filename"),
     Input("sentiment_model", "value"),
     Input("run", "n_clicks")],
)
def parse_data(list_of_contents, list_of_names, sentiment_model, n_clicks):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        df = children[0]
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


# # Uploaded data --> Hidden Data Div
# @app.callback(
#     Output("data-table", "children"),
#     [Input("upload-data", "contents"), Input("upload-data", "filename")],
# )
# def data_table(list_of_contents, list_of_names):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n) for c, n in
#             zip(list_of_contents, list_of_names)]
#         # data = io.StringIO(children[0])
#         df = children[0]
#         df = df.drop_duplicates()
#         df = df.dropna()
#         df = df.head(20)
#         return html.Div(
#             dash_table.DataTable(
#                 data=df.to_dict('records'),
#                 columns=[{'name': i, 'id': i} for i in df.columns]
#             )
#         )


# Name: sentiment_indicator
# Input: a pandas data-frame. Its sentiment is already analyzed.
# Output: an indicator (big text) of the average sentiment.
# ---------------
# It gets the average sentiment of the data file
# Then, it output the result on Page 1 - Overview.

# @app.callback(Output(component_id="overview_indicator_sentiment", component_property="children"),
#               [Input(component_id="data-df", component_property="data")])
# def sentiment_indicator(df):
#     df = pd.read_json(df, orient="split")
#     sentiment = len(df.index)
#     return dcc.Markdown("**{}**".format(sentiment))


# New sentiment indicator
@app.callback(Output(component_id="overview_indicator_sentiment", component_property="children"),
              [Input(component_id="data-df", component_property="data")])
def sentiment_indicator(df):
    if type(df) is not dict:
        df = pd.read_json(df, orient="split")
        sentiment = df["sentiment"].mean().round(2)
        return indicator(number=sentiment, description="sentiment of the tweets")


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
        return indicator(number=day, description="research interval")


# Name: quantity_indicator
# Input: a pandas data-frame. May be not analyzed yet.
# Output: an indicator (big text) of the total quantity of tweets.
# ---------------
# It gets the total number of rows in the data file.
# Then, it output the result on Page 1 - Overview.
@app.callback(Output("overview_indicator_quantity", "children"), [Input("data-df", "data")])
def quantity_indicator(df):
    # if df is not None:
    if type(df) is not dict:
        df = pd.read_json(df, orient="split")
        quantity = len(df.index)
        # return dcc.Markdown("**{}**".format(quantity))
        return indicator(number=quantity, description="quantity of the tweets")


@app.callback(Output('quantity-map-1', 'figure'),
              [Input("run", "n_clicks"),
               Input("data-df", "data")
               ])
def quantity_map_1(n_clicks, df):
    if (n_clicks is None) or (type(df) is dict) or (df is None):
        raise PreventUpdate
    else:
        print(type(df))
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
            autosize=True,
            geo=dict(
                scope="usa",
                projection=dict(type="albers usa"),
                lakecolor="rgb(255, 255, 255)",
            ),
            margin=dict(l=10, r=10, t=0, b=0),
        )
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
            autosize=True,
            geo=dict(
                scope="usa",
                projection=dict(type="albers usa"),
                lakecolor="rgb(255, 255, 255)",
            ),
            margin=dict(l=10, r=10, t=0, b=0),
        )
        return dict(data=data, layout=layout)


# hide/show modal
@app.callback(
    Output("modal", "style"), [Input("new_workflow", "n_clicks")]
)
def display_opportunities_modal_callback(n):
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}


# reset to 0 add button n_clicks property
@app.callback(
    Output("new_workflow", "n_clicks"),
    [
        Input("modal_close", "n_clicks"),
        Input("run", "n_clicks"),
    ],
)
def close_modal_callback(n, n2):
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)
