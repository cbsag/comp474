import rdflib
from rdflib.namespace import RDFS,FOAF,RDF
import json
import csv
import sys
import requests
vivo=rdflib.Namespace("http://vivoweb.org/ontology/core#")
ex=rdflib.Namespace("http://example.org/")

g=rdflib.Graph()
uniname=rdflib.URIRef("http://example.org/"+"Concordia_University")
g.add((uniname,RDF.type,vivo.University))
g.add((uniname,ex.name,rdflib.Literal("Concordia University")))
g.add((uniname,ex.link,rdflib.URIRef("https://dbpedia.org/page/Concordia_University")))

req=requests.post("http://localhost:3030/project/data",data=g.serialize(),headers={"Content-Type":"text/turtle"})

print(req.status_code)
print(req.text)