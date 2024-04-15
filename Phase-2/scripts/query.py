import json
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from scripts import responses
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

class Query:
    
    def sendQuery(self,query):
        query="""PREFIX Vocab: <http://example.org/vocabulary/>\nPREFIX rdf:	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nprefix rdfs:	<http://www.w3.org/2000/01/rdf-schema#>\n
           PREFIX vivo: <http://vivoweb.org/ontology/core#> 
           PREFIX foaf: <http://xmlns.com/foaf/0.1/> """+query
        sparql=SPARQLWrapper("http://localhost:3030/IntSysProjectPhase2/sparql")
        sparql.setQuery(query.encode())
        sparql.setReturnFormat(JSON)

        # Execute the query and print the results
        results = sparql.query().convert()
        #print(results)
        return results["results"]["bindings"]
        #return respFuncbinding[str(self.currQuestion)](results["results"]["bindings"])
        print("\n")
        # for result in results["results"]["bindings"]:
        #     print(result)
    def stats(self):
        print("Stats of DB:\n")
        sparql=SPARQLWrapper("http://localhost:3030/IntSysProjectPhase1/sparql")
        query="""SELECT (COUNT(*) AS ?totalTriples) WHERE {
            ?subject ?predicate ?object
            }"""
        sparql.setQuery(query.encode())
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print("total triples: ",results["results"]["bindings"][0]["totalTriples"]["value"],"\n")
        query="""PREFIX vivo: <http://vivoweb.org/ontology/core#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

            SELECT (count(?course) as ?coursecount) WHERE {
            ?course rdf:type vivo:Course.
            }"""
        sparql.setQuery(query.encode())
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        print("total course URIs: ",results["results"]["bindings"][0]["coursecount"]["value"],"\n")
        
# if __name__=="__main__":      
#     q=Query()
#     q.stats()
#     print("Hi, How can I help you today?")
#     while True:
#         inp=str(input())
#         if inp=="exit":
#             print("Have a nice day")
#             break
#         query=q.handleQuestion(inp)
        
#         q.sendQuery(query)
#         print("Please ask further question or type 'exit' to exit")