import random

import numpy as np
import plotly.graph_objs as go
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from ping3 import ping

from logging_system.logs.models import Log
from logging_system.systems.models import Ping, System


# NumPy arrays and lists
def numpy_array_to_list(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, list):
        return [numpy_array_to_list(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: numpy_array_to_list(value) for key, value in obj.items()}
    else:
        return obj


def list_to_numpy_array(obj):
    if isinstance(obj, list):
        return np.array([list_to_numpy_array(item) for item in obj])
    else:
        return obj


def get_ping_graph(system, height=300, width=900, range=144):
    pings = Ping.objects.filter(system=system).order_by("-id")[:range]
    n = 0
    timestamps = [n + i / 12 for i, _ in enumerate(pings)]
    ping_values = [ping.ping for ping in pings][::-1]

    trace = go.Scatter(
        x=timestamps,
        y=ping_values,
        mode="lines",
        name="Ping",
        marker=dict(color="green"),
    )
    layout = go.Layout(
        xaxis=dict(title="Time range (h)"),
        yaxis=dict(title="Ping (ms)"),
        height=height,
        width=width,
    )
    figure = go.Figure(data=[trace], layout=layout)
    plot_div = figure.to_html(full_html=False)

    return plot_div


def get_uptime_graph(height=300, width=300):
    pings = Ping.objects.all().order_by("-id")[:144]
    n = 0
    positive_pings = sum(1 for ping.ping in pings if ping is not None)
    negative_pings = sum(1 for ping.ping in pings if ping is None)

    labels = ["Positive Pings", "Negative Pings"]
    values = [positive_pings, negative_pings]
    colors = ["green", "red"]

    trace_pie = go.Pie(labels=labels, values=values, marker=dict(colors=colors))
    layout_pie = go.Layout(title="Ping Status Distribution")
    figure_pie = go.Figure(data=[trace_pie], layout=layout_pie)
    pie_plot_div = figure_pie.to_html(full_html=False)

    return pie_plot_div


def get_labels_graph():
    labels = Log.objects.values_list("label", flat=True).distinct()
    n = 0
    labels = [i for i in range(len(labels))]
    values = [Log.objects.filter(label=i).count() for i in range(len(labels))]

    trace = go.Bar(x=labels, y=values, name="Ping")
    layout = go.Layout(
        xaxis=dict(title="Label"),
        yaxis=dict(title="Count"),
        height=250,
        width=400,
        title="Logs count in each label",
    )
    figure = go.Figure(
        data=[trace],
        layout=layout,
    )
    plot_div = figure.to_html(
        full_html=True,
    )

    return plot_div
