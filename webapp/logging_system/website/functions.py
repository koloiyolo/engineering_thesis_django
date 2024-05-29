import numpy as np
import plotly.graph_objs as go
from .models import Ping, Log
from ping3 import ping

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



def get_ping_graph(service_ip, height=300, width=1200, range=144):
    range = range
    pings = Ping.objects.filter(ip=service_ip).order_by('-id')[:range]
    n = 0
    timestamps = [n + i/12 for i,_ in enumerate(pings)]
    ping_values = [ping.ping for ping in pings][::-1]

    trace = go.Scatter(x=timestamps, y=ping_values, mode='lines', name='Ping', marker=dict(color='green'))
    layout = go.Layout(xaxis=dict(title='Time range (h)'), 
                       yaxis=dict(title='Ping (ms)'),
                       height=height,
                       width=width,)
    figure = go.Figure(data=[trace], layout=layout)
    plot_div = figure.to_html(full_html=False)

    return plot_div



def get_labels_graph():

    labels = Log.objects.values_list('label', flat=True).distinct()
    n = 0
    labels = [i for i in range(len(labels))]
    values = [Log.objects.filter(label=i).count() for i in range(len(labels))]

    trace = go.Bar(x=labels, y=values, name='Ping')
    layout = go.Layout(xaxis=dict(title='Label'), 
                       yaxis=dict(title='Count'),
                       height=250,
                       width=400,
                       title="Logs count in each label")
    figure = go.Figure(data=[trace], layout=layout,)
    plot_div = figure.to_html(full_html=True, )

    return plot_div


def ping_objects(objects):
    for object in objects:
        ip = object.ip
        response_time = ping(object.ip, unit='ms')

        if response_time is not None:
            object.ping = f'{int(response_time)} ms'
            object.d_count = 0
            object.save()
        else: 
            object.ping = None
            object.d_count = object.d_count + 1
            if object.d_count >= 5:

                # !!! Change to send_email() !!!

                # send_mail(
                #     f'Abnormal record detected, label: {label}',
                #     f'{log.host} {log.tags} {log.message} {log.datetime}',
                #     'from@example.com',
                #     ["to@example.com"],
                #     fail_silently=False,

                # )

                print(f'{object.id} {object.name} IP: {object.ip} is down')
                object.d_count = 0

            object.save()

        Ping.objects.create(ip=ip, ping=response_time)