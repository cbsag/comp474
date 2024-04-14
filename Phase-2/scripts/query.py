import json
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from scripts import responses
import os
respFuncbinding={"1":responses.firstQuestion,"2":responses.secondQuestion,"3":responses.thirdQuestion,"4":responses.fourthQuestion,"5":responses.fifthQuestion,"6":responses.sixthQuestion,
                 "7":responses.seventhQuestion,"8":responses.eightQuestion,"9":responses.ninethQuestion,"10":responses.tenthQuestion,"11":responses.eleventhQuestion,"12":responses.twelvethQuestion,"13":responses.thirteenthQuestion}
base_dir = os.path.dirname(os.path.abspath(__file__))

class Query:
    def __init__(self):
        self.queries=json.loads(open(base_dir+"/query.json","r").read())
        self.currQuestion=0
        return
    
    def handleQuestion(self,question):
        if "List all courses offered by" in question and "within" in question:
            #q4
            
            university=question.split("List all courses offered by",1)[1].split("within the",1)[0].strip()
            subject=question.split("List all courses offered by",1)[1].split("within the",1)[1].strip()[:-1]
            #print(university)
            print("sub",subject)
            self.currQuestion=4
            return self.queries["4"].format(university,subject)
        
        if "List all courses offered by" in question:
            #q1
            
            uni_name=question.split("List all courses offered by",1)[1].strip()
            print(uni_name)
            self.currQuestion=1
            return self.queries["1"].format(uni_name,uni_name)
        if "In which courses is" in question:
            #q2
            
            topic=question.split("In which courses is",1)[1].split("discussed?",1)[0].strip()
            self.currQuestion=2
            return self.queries["2"].format(topic)
            
        if "Which topics" in question and "are covered in" in question and "during" in question:
            #q3
            firstPart=question.split("Which topics are covered in ",1)[1]
            course=firstPart.split("during",1)[0].strip()
        
            lecture=firstPart.split("during",1)[1].strip().split("?",1)[0].strip()
            print(course,lecture)
            self.currQuestion=3
            return self.queries["3"].format(course,lecture)
        
        
        
        if "How many credits is" in question:
            #q6
            course=question.split("How many credits is",1)[1].strip().split(" ",1)[0].strip()
            number=question.split("How many credits is "+course,1)[1].split("worth?",1)[0].strip()
            self.currQuestion=6
            return self.queries["6"].format(number,course)
        if "For" in question:
            #q7
            course=question.split("For",1)[1].strip().split(" ")[0]
            number=question.split("For "+course,1)[1].split(", what additional resources",1)[0].strip()
            self.currQuestion=7
            return self.queries["7"].format(number,course)
        
        if "Detail the content available for" in question:
            #q8
            lecnum=question.split("Detail the content available for",1)[1].split("in",1)[0].strip()
            course=question.split("Detail the content available for "+lecnum+" in",1)[1].strip().split(" ")[0]
            number=question.split("Detail the content available for "+lecnum+" in",1)[1].strip().split(" ")[1].replace(".","")
            self.currQuestion=8
            return self.queries["8"].format(number,course,lecnum)
        
        if "What reading materials are recommended for studying" in question:
            #q9
            topic=question.split("What reading materials are recommended for studying",1)[1]
            topic=topic[0:topic.rfind("in")-1].strip()
            print(topic)
            course=question.split("What reading materials are recommended for studying "+topic+" in",1)[1].split("?",1)[0].strip()
            self.currQuestion=9
            return self.queries["9"].format(course,topic)
        
        if "What competencies does a student gain after completing" in question:
            #q10
            course=question.split("What competencies does a student gain after completing",1)[1].strip().split(" ")[0]
            number=question.split("What competencies does a student gain after completing",1)[1].strip().split(" ")[1][:-1]
            print(course,number)
            self.currQuestion=10
            return self.queries["10"].format(number,course)
        if "What grades did" in question:
            #q11
            student=question.split("What grades did",1)[1].split("achieve in",1)[0].strip()
            firstName=student.split(" ")[0]
            lastName=" ".join(student.split(" ")[1:])
            course=question.split("What grades did "+student+" achieve in",1)[1].strip().split(" ")[0]
            number=question.split("What grades did "+student+" achieve in",1)[1].strip().split(" ")[1][:-1]
            self.currQuestion=11
            return self.queries["11"].format(firstName,lastName,course,number)
        if "Which students have completed" in question:
            #q12
            course=question.split("Which students have completed",1)[1].strip().split(" ")[0]
            number=question.split("Which students have completed",1)[1].strip().split(" ")[1][:-1]
            self.currQuestion=12
            return self.queries["12"].format(course,number)
        if "Print a transcript" in question:
            #q13
            student=question.split("Print a transcript for a",1)[1].split(", listing all the course taken with their grades.",1)[0].strip()
            firstName=student.split(" ")[0]
            lastName=" ".join(student.split(" ")[1:])
            self.currQuestion=13
            return self.queries["13"].format(firstName,lastName)
        if "What" in question:
            #q5
            material=question.split("What",1)[1].split("are recommended for",1)[0].strip()
            topic=question.split("What",1)[1].split("are recommended for",1)[1].strip()
            topic=topic[0:topic.rfind("in")-1].strip()
            course=question.split("What "+material+" are recommended for "+topic,1)[1].split("in",1)[1].strip().split(" ")[0]
            number=question.split("What "+material+" are recommended for "+topic,1)[1].split("in",1)[1].strip().split(" ")[1].split("?")[0]
            self.currQuestion=5
            #print("crs",course)
            return self.queries["5"].format(number,course,topic,material)
        
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
        
if __name__=="__main__":      
    q=Query()
    q.stats()
    print("Hi, How can I help you today?")
    while True:
        inp=str(input())
        if inp=="exit":
            print("Have a nice day")
            break
        query=q.handleQuestion(inp)
        
        q.sendQuery(query)
        print("Please ask further question or type 'exit' to exit")