import csv
import re
import socket

import plotly.graph_objs as go
from django.core.mail import send_mass_mail
from django.http import HttpResponse
from ping3 import ping

from logging_system.audit_log.models import AuditLog
from logging_system.config.models import Settings
from logging_system.incidents.functions import create_incident

from .models import Ping, System


# System ping task function
def ping_systems(systems: list[System], debug: bool = True) -> bool:
    """Ping all systems and log responses.

    Args:
        systems: List of System objects to ping.
        debug: Whether to print debug information (default is True).

    Returns:
        True upon completion.
    """
    emails = []
    for system in systems:
        ip = system.ip
        response_time = ping(ip, unit="ms")
        if debug:
            print(f"{ip}, {response_time}")
        if response_time not in (False, None):
            system.last_ping = f"{int(response_time)} ms"
            system.d_count = 0
            Ping.objects.create(system=system, ping=response_time)
        else:
            system.last_ping = None
            system.d_count += 1
            if system.d_count == Settings.load().ping_retries:
                email = create_incident(system=system)
                if email is not False:
                    emails.append(email)
            Ping.objects.create(system=system, ping=None)

        system.save()
    if len(emails) != 0:
        send_mass_mail(emails)

    AuditLog.objects.create(user=None, message="All systems pinged.")
    return True


def get_ping_graph(system: System, height: int = 320, width: int = 1240):
    range_ = Settings.load().graph_interval * 12
    pings = Ping.objects.filter(system=system).order_by("-id")[:range_]
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
    plot_div = figure.to_html(full_html=True)

    return plot_div


def discover_systems(
    ip_range: str, system_type: int | None = None, prefix: str = ""
) -> bool:
    """Discover systems by scanning an IP range.

    Parses the provided IP range string to extract a prefix and a start/end pair of
    numbers, iterates over them, pings each host, optionally resolves the hostname via
    DNS, and creates System model instances for responsive hosts.

    Args:
        ip_range: A string in the format "prefix.first-last" (e.g., "192.168.1.0-5").
                  The prefix part is expected to contain three dot-separated parts.
        system_type: Optional system type ID to assign to discovered systems.
        prefix: Optional custom prefix to use for naming systems if DNS resolution fails.

    Returns:
        True if the function completed successfully (even if no systems were created),
        False if the IP range format or values were invalid.
    """
    systems = []
    match = re.search(
        r"^(([^.\\-]+)\.([^.\\-]+)\.([^.\\-]+)).*?([^.\\-]+)[-]([^.\\-]+)$", ip_range
    )

    # validate match
    if not match:
        print(f"Invalid IP range format: {ip_range}")
        return False

    ip_prefix = match.group(1)
    try:
        first = int(match.group(5))
        last = int(match.group(6))
    except ValueError:
        print(f"Invalid IP range values in: {ip_range}")
        return False

    if first > last:
        print(f"Invalid range: start ({first}) is greater than end ({last})")
        return False

    for i in range(first, last + 1):
        dns_discovery = Settings.load().system_discovery_dns
        ip = f"{ip_prefix}.{i}"
        dns_name: str | None = None
        response_time = ping(ip, unit="ms")
        if response_time in (None, False):
            print(f"{ip}: host not found. Response: {response_time}")
        else:
            print(f"{ip}: host found")

            if dns_discovery:
                try:
                    dns_name = socket.gethostbyaddr(ip)[0]
                except (socket.herror, socket.gaierror):
                    dns_name = None

            system_name = dns_name if dns_name is not None else f"{prefix}{ip}"

            system = System.objects.create(
                name=system_name, ip=ip, system_type=system_type
            )
            systems.append(system)

    print("Added new systems: ")
    for system in systems:
        print(f"{system}")

    AuditLog.objects.create(user=None, text=f"New systems discovered prefix {prefix}.")
    return True


# System packet loss function
def get_packet_loss(system: System):
    range_ = Settings.load().graph_interval * 12
    pings = Ping.objects.filter(system=system).order_by("-id")[:range_]
    count = pings.count()
    none_count = 0
    for p in pings:
        if p.ping is None:
            none_count += 1
    try:
        return round(none_count / count * 100, 2)
    except ZeroDivisionError:
        return 0


def export_csv(system_type=None):
    systems = (
        System.objects.all()
        if system_type is None
        else System.objects.filter(system_type__lt=100).order_by("id")
        if system_type == 0
        else System.objects.filter(system_type__gte=100).order_by("id")
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=systems.csv"

    file = csv.writer(response)

    file.writerow(
        [
            "name",
            "ip",
            "system_type",
            "port",
            "location",
            "town",
            "address",
            "room",
            "model",
            "notes",
        ]
    )
    for system in systems:
        file.writerow(
            [
                system.name,
                system.ip,
                system.get_system_type_display(),
                system.port if system.port is not None else None,
                system.location if system.location is not None else None,
                system.location.town if system.location is not None else None,
                system.location.address if system.location is not None else None,
                system.location.room if system.location is not None else None,
                system.model if system.model is not None else None,
                system.notes if system.port is not None else None,
            ]
        )

    return response
