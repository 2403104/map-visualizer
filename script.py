import folium            # For creating interactive maps
import requests          # For calling IP geolocation API
import time              # For adding delay between API calls
import platform          # To detect operating system
import webbrowser        # To open map automatically in browser
import os                # To get absolute file path

# detect OS and choose correct traceroute command
system = platform.system().lower()
if system == "windows":
    command = "tracert"
else:
    command = "traceroute"

# read destinations from file (one per line)
with open("destination_list.txt", 'r') as f:
    lst = f.read()
dests = lst.split("\n")

import subprocess
trace_log = {}

# run traceroute for each destination
for d in dests:
    print(d)
    process = subprocess.Popen(
        [command, d],                  
        stdout=subprocess.PIPE,        
        stderr=subprocess.STDOUT,
        text=True
    )
    trace_log[d] = []
    
    #read traceroute output line by line
    for line in process.stdout:
        trace_log[d].append(line)
        print(line)
    process.wait()

import re

# pattern of ip
ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

# extracting ips from traceroute output
def extract_ips(trace):
    ips = []
    for line in trace:
        ip = ip_pattern.findall(line)
        if ip:
            ips.append(ip[0])
    return ips

# saving extracted ips to ips.txt file
with open("ips.txt", 'w') as f:
    for dest, trace in trace_log.items():
        ips = extract_ips(trace)
        f.write(f"{dest}\n")
        for ip in ips:
            f.write(f"{ip}\n")
        f.write("\n")

# reconstructing paths from ips.txt
paths = {}
curr = None
with open("ips.txt", 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            curr = None
            continue
        if curr is None:
            curr = line
            paths[curr] = []
            continue
        paths[curr].append(line)

# will give the location of ips(Latitude and Longitude)
def getLocation(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        data = requests.get(url, timeout=20).json()
        lat = data["lat"]
        lon = data["lon"]
        return lat, lon
    except:
        print(f"Skipping {ip}, Found Error : f{data}")
        return None, None

geoPaths = {}
for dest, ips in paths.items():
    geoPaths[dest] = []
    for ip in ips:
        lat, lon = getLocation(ip)
        if lat is not None and lon is not None:
            geoPaths[dest].append([lat, lon])
            time.sleep(1)   # avoid API rate limit

# creating base world map
map = folium.Map(location=[20, 0], zoom_start=2)

colors = ["red", "blue", "green", "purple", "orange"]
idx = 0

# drawing roots and hop markers
for dest, geoPath in geoPaths.items():
    color = colors[idx % len(colors)]
    idx += 1
    
    # routing path
    folium.PolyLine(
        geoPath,
        color=color,
        weight=3,
        tooltip=dest
    ).add_to(map)

    # drawing indivisual hop
    for lat, lon in geoPath:
        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.8
        ).add_to(map)

# save and open map
map.save("map.html")
print("Map saved to map.html")
webbrowser.open("file://" + os.path.realpath("map.html"))
