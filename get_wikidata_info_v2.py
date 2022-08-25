#-------------------------------------------------------------------------------
# Name:        get_wikidata
# Purpose: Two QGIS functions developed to find a person's gender using Wikidata information.
# get_ wikidata item_id: Find the unique wikidata id.
# get_wikidata_gender: search for the gender set in Wikidata
#
# Author:      Enrico Ferreguti, Rocco Pispico
#
# Created:     21/06/2022
# Licence:     PSFL - PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
#-------------------------------------------------------------------------------


from qgis.core import *
from qgis.gui import *
import requests
import json

# in q1 variable can set the main locale/national wikidata database
q1 = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&format=json&errorformat=plaintext&language=en&uselang=it"
q2 = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids=%s&props=claims'

# in this dictionary it is possible to set the genre wikidata keys and their desired description
decodict = {
    "Q6581097": "M",
    "Q6581072": "F",
    "Q1052281": "TF",
    "nd": "*"
}

def get_itemid(val):
    r1 = requests.get(q1 % val)
    j1 = r1.json()
    try:
        k1 = j1["search"][0]["id"]
        return k1
    except:
        return ""

@qgsfunction(args='auto', group='wikidata', referenced_columns=[])
def get_wikidata_itemid(value1, feature, parent):
    """
    Calculates the sum of the two parameters value1 and value2.
    <h2>Example usage:</h2>
    <ul>
      <li>my_sum(5, 8) -> 13</li>
      <li>my_sum("field1", "field2") -> 42</li>
    </ul>
    """
    return get_itemid(value1)


@qgsfunction(args='auto', group='wikidata', referenced_columns=[])
def get_wikidata_gender(value1, feature, parent):
    """
    Calculates the sum of the two parameters value1 and value2.
    <h2>Example usage:</h2>
    <ul>
      <li>my_sum(5, 8) -> 13</li>
      <li>my_sum("field1", "field2") -> 42</li>
    </ul>
    """
   
    if len(value1) > 1 and value1[0] == "Q" and value1[1] in "0123456789" and value1[2] in "0123456789":
        print("isvalue")
        k1 = value1
    else:
        k1 = get_itemid(value1)
        if not k1:
            return ""
   
    r2 = requests.get(q2 % k1)
    j2 = r2.json()
   
    try:
        gender = j2["entities"][k1]["claims"]["P21"][0]["mainsnak"]["datavalue"]["value"]["id"]
    except:
        gender = "nd"
    print (value1, k1, gender, decodifica[gender])
   
    return decodict[gender]
