# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 20:27:31 2015

@author: Doug
"""

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
        counts = {}
        for event, elem in ET.iterparse(filename):
            
            try:
                counts[elem.tag] = counts[elem.tag] + 1
            except KeyError:
                counts[elem.tag] = 1
            
        print counts 
                
        return counts       
       
def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()