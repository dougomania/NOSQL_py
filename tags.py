# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 20:27:31 2015

@author: Doug
"""

import xml.etree.cElementTree as ET
import pprint
import itertools
import re
from collections import defaultdict

postal = re.compile(r'^[Mm]{1}\d{1}[A-Za-z]{1}\s*\d{1}[A-Za-z]{1}\d{1}$')


street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Grove"]

#Listing all the ways that Toronto is listed
cities = ["Toronto", "Etobicoke", "Scarborough", "North York","toronto", "City of Toronto", "Etobicoke, Toronto"]

# full mapping of streets 
mapping = { "St": "Street",
            "St.": "Street",
            "Ave" : "Avenue",
            "Ave." : "Avenue",
            "Rd" : "Road",
            "Rd.": "Road",
            "W.": "West",
            "W": "West",
            "E.": "East",
            "E": "East",
            "S.":"South",
            "S" : "South",
            "Grv":"Grove",
            "Pkwy":"Parkway",
            "Trl":"Trail"
            }
            
#Maps the city names to Toronto. Keeps the Buroughs as they are written
mapping2 = {"City of Toronto" : "Toronto",
            "Etobicoke, Toronto": "Etobicoke",
            "toronto": "Toronto" }

#checks the postal code 
def upostal (code):
    if postal.search(code):
        code1 = code[0:3].upper()
        code2 = code[3:].strip().upper()
        code = code1 + " " + code2
        return code
    else:
        return False
        
#updates both the street suffixes and the city names
def update_name(name):
    
    full_name = name.split(" ")
    counter = 0
    
    for n in full_name:
        
        for i in mapping:
           if n == i:
               full_name[counter] = mapping[i]
        counter += 1
    name =" ".join(full_name) 

    for i in mapping2:
        if name == i:
            name = mapping2[i]
            

    return name

    



    
#taking out KV data that is not in Toronto
def istoronto(element):
   for tag in element.iter("tag"):
       if tag.attrib['k'] == "addr:city":
           for c in cities:
               if c == tag.attrib['v']:
                   return True
   return False                 
                     
    

 
'''    
# makes a set of the users 
def count_users(element, counts):
    try:
        counts[element.attrib["user"]] = counts[element.attrib["user"]] + 1
    except KeyError:
        counts[element.attrib["user"]] = 1
                
    return counts

def ischild(element):
    if list(element) == []:
        return False
    else:
        return True

def tester(filename):
    for event, elem in ET.iterparse(filename):
        istoronto(elem)

#finding out how many tags are here

def count_tags(filename):
    counts = {}
    for event, elem in ET.iterparse(filename):
            
        try:
            counts[elem.tag] = counts[elem.tag] + 1
        except KeyError:
            counts[elem.tag] = 1
    print counts 
                
    return counts       
       
def k_attr(filename):
    ks = set()
    for event, elem in ET.iterparse(filename):
        
         if elem.tag == "node" or elem.tag == "way" :
        
             for tag in elem.iter("tag"):
                 
                 if tag.attrib['k'] == "addr:city":
                     print tag.attrib
                 ks.add(tag.attrib['k'])
                
    return ks

#Audits streetname for unpopular characters 
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
       
#Tests to see if it is a streetname
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types
'''        