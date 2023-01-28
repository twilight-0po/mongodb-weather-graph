import pymongo
import dotenv
import os
from pprint import pprint
import datetime
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

date_pressure_dict = {}
date_list = []
pressure_list = []
temp_list = []

dotenv.load_dotenv()

MONGODB_URL = os.environ["MONGODB_URL"]

client = pymongo.MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)

db = client['sample_weatherdata']
data = db['data']

weatherdata = data.find({
    "ts": {"$gte": datetime.datetime(1984, 3, 5), "$lt": datetime.datetime(1984, 3, 6)}})

for daily_data in weatherdata:
    if daily_data["pressure"]["value"] and daily_data["ts"] not in date_list:
        daily_pressure = int(daily_data["pressure"]["value"])
        daily_temp = int(daily_data["airTemperature"]["value"])
        if daily_pressure != 9999:
            date_pressure_dict[daily_data["ts"]] = (daily_pressure, daily_temp)
            date_list.append(daily_data["ts"])
date_list.sort()
for date in date_list:
    pressure_list.append(date_pressure_dict.get(date)[0])
    temp_list.append(date_pressure_dict.get(date)[1])


df1 = pd.DataFrame({
    "date": date_list,
    "pressure": pressure_list,
})

df2 = pd.DataFrame({
    "date": date_list,
    "temperature": temp_list,
})

app = Dash(__name__)

fig1 = px.line(df1, x="date", y="pressure",
               title='Pressure Change', markers=True)
fig2 = px.line(df2, x="date", y="temperature",
               title='Temperature Change', markers=True)


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig1
    ),

    html.Div(children='''
        this is temperature graph
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig2
    ),

])

if __name__ == '__main__':
    app.run_server(debug=True)
