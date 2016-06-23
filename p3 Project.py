# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:54:55 2015

@author: Doug
"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import codecs
import json
import tags
import operator
import re


# Used to verify data is in the correct format
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#loads the data from OSM
def load():
    data = 'toronto_canada.osm'
    return data 

''' Moves the XML document to JSON format so that MongoDB can utilize it'''

#Shapes the file of the of the FULL Toronto OSM data.     
def shape_element(element):
    node = {}
    createdn= {}
    add = {}
    nd=[]
    
    
    if element.tag == "node" or element.tag == "way" :
        #print element.attrib
        # Put together bulk of dictionary 
        
        node["id"] = element.attrib['id']
        node["type"] = element.tag
        if "visible" in element.attrib:
            node["visible"] = element.attrib['visible']
        createdn["version"] = element.attrib['version']
        createdn["changeset"] = element.attrib['changeset']
        createdn["timestamp"] = element.attrib['timestamp']
        createdn["user"] = element.attrib["user"]
        createdn["uid"] = element.attrib["uid"]
        node["created"] = createdn
        if "lon" in element.attrib:
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"]) ]
            
          
        for tag in element.iter("tag"):
              # spliting up data between addr data and none address
              #print tag.attrib
            if tag.attrib['k'][:5] == "addr:":           
                if good_data(tag.attrib['k']):               
                    if not lower_colon.search(tag.attrib['k'][5:]):
                        nname = tags.update_name(tag.attrib['v'])
                        add[tag.attrib['k'][5:]] = nname 
            else:
                if good_data(tag.attrib['k']):
                    node[tag.attrib['k']]= tag.attrib['v']
        if add != {}: 
            node["address"] = add
                
        for tag in element.iter("nd"):
            nd.append(tag.attrib["ref"])
        if nd != []:
            node["node_refs"]= nd
        return node
    else:
        return None
    
#Helper function that returns false if there are problem characters 
def good_data(tag):
    if problemchars.search(tag): 
        result= False
    else:
        result = True
    return result

#this is the second shape element that filters out ammenities that are not in Toronto
def shape_element2(element):
    node = {}
    createdn= {}
    add = {}
    nd=[]
    
    
    if element.tag == "node" or element.tag == "way" :
        #print element.attrib
        # Put together bulk of dictionary 
        if tags.istoronto(element): 
            node["id"] = element.attrib['id']
            node["type"] = element.tag
            if "visible" in element.attrib:
                node["visible"] = element.attrib['visible']
            createdn["version"] = element.attrib['version']
            createdn["changeset"] = element.attrib['changeset']
            createdn["timestamp"] = element.attrib['timestamp']
            createdn["user"] = element.attrib["user"]
            createdn["uid"] = element.attrib["uid"]
            node["created"] = createdn
            if "lon" in element.attrib:
                node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"]) ]
            
          
            for tag in element.iter("tag"):
                # spliting up data between addr data and none address
                #print tag.attrib
                if tag.attrib['k'][:5] == "addr:":           
                    if good_data(tag.attrib['k']):               
                        if not lower_colon.search(tag.attrib['k'][5:]):
                            nname = tags.update_name(tag.attrib['v'])
                            add[tag.attrib['k'][5:]] = nname 
                else:
                    if good_data(tag.attrib['k']):
                        node[tag.attrib['k']]= tag.attrib['v']
            if add != {}: 
                node["address"] = add
                
            for tag in element.iter("nd"):
                nd.append(tag.attrib["ref"])
            if nd != []:
                node["node_refs"]= nd
            return node
        else:
            return None
    else:
        return None
        

#This is the function that processes the map
def process_map(file_in):
    # You do not need to change this file
    pretty = False
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element2(element) #change from " " to 2 depending how I want to process the data
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    
if __name__ == "__main__":    
    data = load()
    process_map(data)