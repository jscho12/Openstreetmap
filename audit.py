#!/usr/bin/env python
# coding: utf-8

# Taken from Udacity's Case Study


import xml.etree.cElementTree as ET
import pprint
import re
import codecs
from collections import defaultdict
OSMFILE = ("Bohemia.osm")
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)



expected = ['Avenue', 'Bridge', 'Boulevard', 'Circle', 'Circuit', 'Crescent', 'Court', 'Close', 'Drive', 'Gardens',
           'Green', 'Grove', 'Gate', 'Hill', 'Heights', 'Lane', 'Line', 'Lawn', 'Mews', 'Path', 'Park', 'Parkway',
           'Place', 'Ramp', 'Road', 'Roadway', 'Square', 'Street', 'Terrace', 'Trail', 'View', 'Walk', 'Way', 'Woods', 'Wood',
            'North','South','East','West','Southeast','Southwest','Northeast','Northwest','Broadway','Brookway','Highway',
            'Shoreway','2','Row','D','Run','Loop']

mapping = { 'Ave': 'Avenue',
            'Bdge': 'Bridge',
            'Boulevard': 'Boulevard',
            'Blvd': 'Boulevard',
            'Crcl': 'Circle',
            'Cir': 'Circle',
            'cir': 'Circle',
            'Crct': 'Circuit',
            'Cres': 'Crescent',
            'Ct': 'Court',
            'court':'Court',
            'Crt': 'Court',
            'Court': 'Court',
            'Cs': 'Close',
            'Cv': 'Cove Way',
            'Dr': 'Drive',
            'Dr.': 'Drive',
            'Drive': 'Drive',       
            'Gdns': 'Gardens',
            'Grn': 'Green',
            'Grv': 'Grove',
            'Gt': 'Gate',
            'Hill': 'Hill',
            'Hts': 'Heights',
            'Hrbr': 'Harbour',
            'Ky': 'Key Way',
            'Ln': 'Lane',
            'Ldg': 'Landing',
            'Line': 'Line',
            'Lwn': 'Lawn',
            'Mews': 'Mews',
            'Path': 'Path',
            'Pk': 'Park',
            'Pkwy': 'Parkway',
            'Pl': 'Place',
            'Ramp': 'Ramp',
            'Rd': 'Road',
            'Rd.': 'Road',
            'Rdwy': 'Roadway',
            'Sq': 'Square',
            'St': 'Street',
            'Street': 'Street',
            'Ste': 'Suite',
            'Ter': 'Terrace',
            'Trl': 'Trail',
            'View': 'View',
            'Walk': 'Walk',
            'Way': 'Way',
            'Wds': 'Woods',
            'Wood': 'Wood',
            'W': 'West',
            'N': 'North',
            'S': 'South',
            'E': 'East',
            'NW':'Northwest',
            'SE':'Southeast',
            'SW':'Southwest',
            'NE':'Northeast',
            'Plz':'Plaza',
            'Hwy':'Highway',
            'highway':'Highway',
            'Highway':'Highway',
            'Lndg':'Landing',
            'street': 'Street',
            'Cross': 'Crossing',
            'Prom':'Promenade',
            'Lane':'Lane',
            'Place':'Place',
            'Avenue':'Avenue',
            'Road':'Road',
            'Brookway':'Brookway',
            'Gate':'Gate',
            'Shoreway':'Shoreway',
            'Row':'Row',
            'D':'D',
            'Row':'Row',
            'Run':'Run',
            'Loop':'Loop',
            'Parkway':'Parkway'}

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
   
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
        
def is_street_name(elem):
    return (elem.attrib['k'] == 'addr:street') 

def audit(osmfile):
    osm_file = open(osmfile, 'r')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):

        if elem.tag == 'node'or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if is_street_name(tag):
                    audit_street_type(street_types,tag.attrib['v'])
              
    osm_file.close()
    return street_types

def update(name):
  m = street_type_re.search(name).group()
  # If the street is abbreviated 
  if m not in expected:
      name = name.replace(m,mapping[m])
  
  return name

#tests to see if the name are corrected
def test():
    st_types = audit(OSMFILE)
    
    pprint.pprint(dict(st_types))
    
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update(name)
            print name, "=>", better_name
          

if __name__ == '__main__':
    test()








# In[ ]:




