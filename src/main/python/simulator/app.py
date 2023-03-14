import sys
import time
import random
import boto3
import xml.etree.ElementTree as ET
import json

from math import sin, cos, sqrt, atan2, radians

path=sys.argv[1]
streamName=sys.argv[2]

def distance(la1,lo1,la2,lo2):
  # Approximate radius of earth in km
  R = 6373.0

  lat1 = radians(la1)
  lon1 = radians(lo1)
  lat2 = radians(la2)
  lon2 = radians(lo2)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  distance = R * c
  return distance * 1000

# set up AWS Kinesis client
kinesis = boto3.client('kinesis', region_name='us-east-1')

# read KML file containing the bus route using XML
tree = ET.parse(path)
root = tree.getroot()
coordinates = []
for element in root.iter('{http://www.opengis.net/kml/2.2}coordinates'):
    coord_string = element.text.strip()
    coords = coord_string.split()
    for coord in coords:
        lon, lat, _ = coord.split(',')
        coordinates.append((float(lon), float(lat)))

# set up initial values for latitude, longitude, and speed
index = 0
lat = coordinates[index][1]
lon = coordinates[index][0]
speed = 0

while True:
    # simulate random traffic condition by randomly changing the speed
    speed = random.uniform(0, 60)
    
    # calculate the new latitude and longitude based on speed and bus route
    found=False
    n=0
    while ( found != True ):
      tla = coordinates[index + n][1]
      tlo = coordinates[index + n][0]
      dnext = distance(lat,lon,tla,tlo)
      dlimit = speed * 1000 / 3600 * 5 
      if ( dnext >= dlimit):
         index = index+n
         found=True
         break
      else:
         n = n + 1
         if ((index + n) >= len(coordinates)):
           index=0
           n=0

    lat = coordinates[index][1]
    lon = coordinates[index][0] 
    
    
    # construct JSON object with latitude, longitude, and timestamp
    event = {
        'speed': speed,
        'latitude': lat,
        'longitude': lon,
        'timestamp': int(time.time()),
        'index': index
    }
    
    # put JSON object into AWS Kinesis stream
    kinesis.put_record(
        StreamName=streamName,
        Data=json.dumps(event),
        PartitionKey=str(random.randint(0,100))
    )
    
    print(event)    

    # wait for 5 seconds before publishing the next event
    time.sleep(5)

