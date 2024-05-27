import numpy as np
import plotly.graph_objs as go
from .models import Ping

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

def get_graph(service_ip):
    pings = Ping.objects.filter(ip=service_ip).order_by('-id')[:144]
    n = 0
    timestamps = [n + i/12 for i in range(72)]
    ping_values = [ping.ping for ping in reversed(pings)]

    trace = go.Bar(x=timestamps, y=ping_values, name='Ping', marker=dict(color='green'))
    layout = go.Layout(xaxis=dict(title='Time range (h)'), 
                       yaxis=dict(title='Ping (ms)'),
                       height=300,
                       width=1200,)
    figure = go.Figure(data=[trace], layout=layout)
    plot_div = figure.to_html(full_html=False)

    return plot_div
