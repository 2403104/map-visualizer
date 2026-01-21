# Traceroute Visualization Project

## Overview
This project performs **network path analysis** using `traceroute / tracert` and visualizes the routing paths of multiple destinations on a **world map**.

The script:
- Reads a list of destinations from a file
- Runs traceroute to each destination
- Extracts intermediate IP addresses
- Finds their geographical locations
- Plots the routing paths on an interactive map using **Folium**

- Run command : "python script.py"
---

## Features
- Supports **Windows and Linux**
- Automatically detects OS (`tracert` vs `traceroute`)
- Parses traceroute output to extract IP addresses
- Uses online IP geolocation API
- Interactive map with colored routes
- Automatically opens the map in the browser

