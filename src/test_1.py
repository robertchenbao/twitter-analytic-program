# This is a demo app! It works, but it is just for testing.
# This is not for any serious purpose.
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime
import io
import dash_table
import pandas as pd
from src.utils import indicator

app = dash.Dash()

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    dcc.Store(id="output-data-upload"),
    # dcc.Graph(id='quantity-map-1'),
    # indicator("Quantity of Tweets", "overview_indicator_quantity"),
])


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
    return df.to_json(orient="split")


# @app.callback(Output("overview_indicator_quantity", "children"), [Input("data-df", "data")])
# def quantity_indicator(df):
#     df = pd.read_json(df, orient="split")
#     quantity = len(df.index)
#     return dcc.Markdown("**{}**".format(quantity))


@app.callback(Output('output-data-upload', 'data'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        print(children)
        print(type(children[0]))
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
