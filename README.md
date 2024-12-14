# Device Management and log analysis system
Simple system designed for log analysis and network devices monitoring.\
Jakub Kołodziej's engineering thesis project.

## Table of contents:
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Stack](#stack)


## Features
* Log collection(using Syslog-ng)
* Log classification using unsupervised learning algorithms like:
  * K-Means,
  * AHC Clustering,
  * SOM (Self-organizing Map).
* System discovery (based on IP Ranges).
* Managed system automatic health checks (Using ICMP Ping).
* Mail notifications on incidents.
* Basic CRUD operations regarding system, location and incident management.

### To Do:
* Report generation

## Requirements
Dependencies:
  * any system supporting Docker
  * git
  * Docker

Opened firewall ports:
  * **80/tcp** - Main application
  * **5014/udp** - Syslog-ng log collection
  * **8081/tcp** - (Optional) phpMyAdmin

## Installation

1. Clone this repository
``` bash
 git clone https://github.com/koloiyolo/engineering_thesis_django.git
```
2. Enter project directory
``` bash
 cd engineering_thesis_django
```
4. Elevate permissions
``` bash
 sudo -s
```
4. Start system using docker compose
``` bash
 docker compose up
```
5. Access the application through your browser at the following address:
```bash
http://{{server_ip_address}}
```

## Stack:
### Frontend:
* HTML5
* Bootstrap
### Backend:
* Docker
* Python
  * Django
  * scikit-learn
  * minisom
  * pandas
  * plotly
  * celery
* MySQL (Planned PostgreSQL)
* Redis
* Syslog-ng
