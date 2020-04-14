#!/usr/bin/env python
# coding: utf-8

# In[8]:


#code retrieved from Udacity Case Study.
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
#cerberus will not load in python version 2.7
#import cerberus
#used a seperate schema
#import schema

OSM_PATH = "Bohemia.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#SCHEMA = schema.Schema(schema)

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    position = 0
    if element.tag == 'way':
            for way in element.iter('way'):
                way_attribs = way.attrib
                
            for child in element:
                way_node={}
                if child.tag =='nd':         
                    way_node['id'] = element.attrib['id']
                    way_node['node_id'] = child.attrib['ref']
                    way_node['position'] = position
                    position = position + 1
                    way_nodes.append(way_node)
            for child in element:
                way_tag = {}
                
                if child.tag == 'tag':
                    if PROBLEMCHARS.match(child.attrib['k']):
                        continue
                    elif LOWER_COLON.match(child.attrib['k']):
                        way_tag['type'] = child.attrib['k'].split(':',1)[0]
                        way_tag['key'] = child.attrib['k'].split(':',1)[1]
                        way_tag['id'] = element.attrib['id']
                        way_tag['value'] = child.attrib['v']
                        tags.append(way_tag)
                    else:
                        way_tag['type'] = 'regular'
                        way_tag['key'] = child.attrib['k']
                        way_tag['id'] = element.attrib['id']
                        way_tag['value'] = child.attrib['v']
                        tags.append(way_tag)
                        
            
            
            return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}
            
    if element.tag == 'node':
            for node in element.iter('node'):
                node_attribs = node.attrib
            for child in element:
                node_tag = {}
                if PROBLEMCHARS.match(child.attrib['k']):
                        continue
                elif LOWER_COLON.match(child.attrib['k']):
                    node_tag['type'] = child.attrib['k'].split(':',1)[0]
                    node_tag['key'] = child.attrib['k'].split(':',1)[1]
                    node_tag['id'] = element.attrib['id']
                    node_tag['value'] = child.attrib['v']
                    tags.append(node_tag)
                else:
                    node_tag['type'] = 'regular'
                    node_tag['key'] = child.attrib['k']
                    node_tag['id'] = element.attrib['id']
                    node_tag['value'] = child.attrib['v']
                    tags.append(node_tag)
            return {'node': node_attribs, 'node_tags': tags}
                           
    
               
   
     
    
  
    
        

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()





class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({k: (v.encode(unicode) if isinstance(v,unicode) else v) for k, v in row.items()})

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""
#added encoding utf-8 #
    with codecs.open(NODES_PATH, 'w',encoding ='utf-8') as nodes_file,         codecs.open(NODE_TAGS_PATH, 'w',encoding='utf-8') as nodes_tags_file,        codecs.open(WAYS_PATH, 'w',encoding='utf-8') as ways_file,        codecs.open(WAY_NODES_PATH, 'w',encoding='utf-8') as way_nodes_file,        codecs.open(WAY_TAGS_PATH, 'w',encoding='utf-8') as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)
        
        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

       # validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
       process_map(OSM_PATH, validate=False)


