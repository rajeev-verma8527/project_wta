import plotly.express as px
import pandas as pd
from sqlalchemy import select
from database import PageVisit, ENGINE
import json


class GraphEntity:
    # used in jinja context
    def __init__(self, fig, title=None, subtext=None):
        self.title = title
        self.subtext = subtext

        # plotly fig exported as html div
        self.graph = fig.to_html(full_html=False, include_plotlyjs=False)


def load_data():
    # pandas can read from a engine connection and select query or text query

    with ENGINE.connect() as con:
        df = pd.read_sql(select(PageVisit), con=con)
    return pd.read_csv("livedata.csv",parse_dates=['time'])


def graphs():
    df = load_data()
    graphs = []

    # views vs loadtime
    fig = px.area(
        df,
        x=df.index,
        y=df.loadtime,
        title="Page Load time",
        labels={"index": "Page Views", "loadtime": "Load time (ms)"},
    )
    graphs.append(GraphEntity(fig, "Page Views vs Page Loading time"))


    # date vs mean loadtime
    load_timedf = df.set_index("time")["loadtime"].resample("D").mean().reset_index()
    fig = px.bar(
        load_timedf,
        x="time",
        y="loadtime",
        title="Mean Load time",
        labels={"time": "Date", "loadtime": "Loadtime (ms)"},
    )
    graphs.append(GraphEntity(fig, "Daily mean loadtime"))


    # Page visites
    page_visit = (
        df["page"]
        .apply(lambda x: "/" + x.split("/", maxsplit=3)[-1])
        .value_counts()
        .reset_index()
    )
    fig = px.bar(
        page_visit,
        x="page",
        y="index",
        color="index",
        labels={"index": "Page", "page": "Views"},
    )
    graphs.append(GraphEntity(fig, title="Page Visits"))


    # district views
    city_df = df.city.value_counts().reset_index()
    fig = px.bar_polar(
        city_df,
        r="city",
        theta="index",
        log_r=True,
        color="city",
        title="District Wise Page Visit",
        labels={"city": "Views", "index": "District"},
    )
    graphs.append(GraphEntity(fig, title="District wise Visits"))

    dates = df.time.dt.date
    unique_visitors = df.groupby([dates, "ip"])["page"].count().groupby("time").count()
    total_visitors = df.groupby(dates)["ip"].count().reset_index()
    total_visitors["unique"] = unique_visitors.to_list()
    total_visitors["repeated"] = total_visitors.apply(
        lambda x: x.ip - x["unique"], axis=1
    )
    total_visitors.reindex({"ip": "total"})
    fig = px.bar(
        total_visitors,
        x=["repeated", "unique"],
        y="time",
        labels={"value": "Visitors", "time": "Date"},
    )
    fig.update_yaxes(dtick=86400000.0)
    graphs.append(GraphEntity(fig, title="Unique and repeated Views"))


    # hourly views
    hourly = df.groupby(df.time.dt.hour).count()["page"].reset_index()
    fig = px.bar(
        hourly, x="time", y="page", labels={"time": "Hour of the day", "page": "Views"}
    )
    fig.update_xaxes(dtick=1)
    graphs.append(GraphEntity(fig, title="Views in hours of the day"))



    # choropleth
    india_states = json.load(open("states_india.geojson", "r"))
    state_id_map = {}
    for features in india_states["features"]:
        features["id"] = features["properties"]["state_code"]
        state_id_map[features["properties"]["st_nm"]] = features["id"]

    def get_state_id(x):
        try:
            return state_id_map[x]
        except:
            return 7

    df["id"] = df["state"].apply(get_state_id)
    a = df.groupby(["id", "state"])["page"].count().reset_index()
    fig = px.choropleth_mapbox(
        a,
        locations="id",
        geojson=india_states,
        color="page",
        hover_name="state",
        hover_data=["page"],
        mapbox_style="carto-positron",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5,
        labels={"page": "Visites", "id": "State ID",},
    )
    graphs.append(GraphEntity(fig,title="State Visits"))

    return graphs

