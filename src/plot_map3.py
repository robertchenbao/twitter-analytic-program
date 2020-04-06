# This is straight out from the Plot.ly website.
# It works for tesla_quantity_16.csv!!
# This is for the quantity!

import plotly.graph_objects as go
import os
import pandas as pd

# if not os.path.exists('/Users/robertbao/Documents/plotly_output'):
#     os.mkdir('/Users/robertbao/Documents/plotly_output')

df = pd.read_csv('/Users/robertbao/Downloads/tesla_quantity_16.csv')
df['state_name'] = df['state_name'].str.upper()

for col in df.columns:
    df[col] = df[col].astype(str)

fig = go.Figure(data=go.Choropleth(
    locations=df['state_name'],
    z=df["quantity"],
    locationmode="USA-states",  # Done
    colorscale="Blues",
    # reversescale=True,
    autocolorscale=False,
    text=df['quantity'],
    type="choropleth",
    marker_line_color='white',
))

fig.update_layout(
    title_text='Hopefully it will work!',
    geo=dict(
        scope="usa",
        projection=dict(type="albers usa"),
        lakecolor="rgb(255, 255, 255)",

    ))

# fig.write_image("fig1.pdf")
fig.show()
