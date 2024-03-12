import rdflib
from rdflib.namespace import RDFS,FOAF,RDF
import json
#loading Vocabularies

#Courses
g1=rdflib.Graph()
g1.parse("Vocabularies/courses.ttl",format="ttl")

#Lecture
g2=rdflib.Graph()

#Student
g2=rdflib.Graph()
g2.parse("Vocabularies/students.ttl",format="ttl")


#studentCourses
g3=rdflib.Graph()
g3.parse("Vocabularies/studentCourses.ttl",format="ttl")

#Merging Vocanulary graphs
g=g1+g2+g3

# f=open("sample.txt","w")
# f.write(g.serialize())
#Creating Name Spaces
vivo=rdflib.Namespace("http://vivoweb.org/ontology/core#")
ex=rdflib.Namespace("http://example.org/")

#import sample data
data=open("scripts/sampledata.json","r")
data=json.loads(data.read())

#populate courses
for i in data["courses"]:
    cname=rdflib.URIRef("http://example.org/"+i["cname"])
    g.add((cname,RDF.type,vivo.Course))
    #ßg.add((cname,RDF.label,i["label"]))
    g.add((cname,ex.course_name,rdflib.Literal(i["cname"])))
    g.add((cname,ex.course_subject,rdflib.Literal(i["subjectCode"])))
    g.add((cname,ex.course_number,rdflib.Literal(i["course_number"])))
    g.add((cname,ex.has_credits,rdflib.Literal(i["credits"])))
   
    
#populate students
for i in data["students"]:
    student=rdflib.URIRef("http://example.org/"+i["id"])
    name=rdflib.URIRef("http://example.org/"+i["fname"]+i["lname"])
    g.add((name,ex.firstName,rdflib.Literal(i["fname"])))
    g.add((name,ex.lastName,rdflib.Literal(i["lname"])))

    g.add((student,RDF.type,vivo.Student))
    g.add((student,ex.student_name,name))
    g.add((student,ex.student_id,rdflib.Literal(i["id"])))
    g.add((student,ex.email,rdflib.Literal(i["email"])))

    #comp courses
    studentCourses=rdflib.URIRef("http://example.org/"+i["id"]+"courses")
    g.add((student,RDF.type,ex.StudentCourses))

    for j in range(1,len(i["completed_courses"])+1):
        StudentCourse=rdflib.URIRef("http://example.org/"+i["id"]+"_"+i["completed_courses"][j-1]["code"])
        #cname=rdflib.URIRef("http://example.org/"+i["cname"])
        g.add((StudentCourse,RDF.type,ex.StudentCourse))
        g.add((StudentCourse,ex.grade,rdflib.Literal(i["completed_courses"][j-1]["grade"])))
        
        g.add((StudentCourse,ex.retakeCourse,rdflib.Literal("no")))

        for s,p,o in g.triples((None,ex.course_number,rdflib.Literal(i["completed_courses"][j-1]["code"]))):
            g.add((StudentCourse,ex.course,s))
        rdfuri=rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#_"+str(j))
        g.add((studentCourses,rdfuri,StudentCourse))
    g.add((student,ex.completed_courses,studentCourses))








f=open("sample.txt","w")
f.write(g.serialize())