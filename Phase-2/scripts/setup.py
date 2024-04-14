import rdflib
from rdflib.namespace import RDFS,FOAF,RDF
import json
import csv
import sys
import os
from dbsetup import DBsetup
from textProcess import TextProcessor
from fileProcess import processFile
textProcessor=TextProcessor()
DATA="http://example.org/Data/"
vivo=rdflib.Namespace("http://vivoweb.org/ontology/core#")
ex=rdflib.Namespace("http://example.org/Data/")
Vocab=rdflib.Namespace("http://example.org/vocabulary/")
#handle populating topic
def handleTopic(filename,cname,lname,graph):
    wiki,dbpedia=processFile(filename,textProcessor)
    
    topicList=[]
    for i in wiki:
        topicURI=rdflib.URIRef(DATA+str(i).replace(" ","_"))
        # if topicURI in topicList:
        #     g.add((topicURI,Vocab.belongs_to,cname))
        #     g.add((topicURI,Vocab.provenance,filename))
        #     g.add((topicURI,Vocab.wikidata_Link,rdflib.URIRef(wiki[i]))) 
        #     if lname is not None:
        #         g.add((topicURI,Vocab.taught_in,lname))
                
        #     continue
        #topicList.append(topicURI)
        graph.add((topicURI,RDF.type,Vocab.Topic))

        if lname is not None:
            g.add((topicURI,Vocab.taught_in,lname))
        
        g.add((topicURI,Vocab.belongs_to,cname))

        g.add((topicURI,Vocab.topic_name,rdflib.Literal(i)))
        g.add((topicURI,Vocab.provenance,filename))
        g.add((topicURI,Vocab.wikidata_Link,rdflib.URIRef(wiki[i])))  
    
    for i in dbpedia:
        topicURI=rdflib.URIRef(DATA+str(i).replace(" ","_"))
        # if topicURI in topicList:
        #     g.add((topicURI,Vocab.belongs_to,cname))
        #     g.add((topicURI,Vocab.provenance,filename))
        #     g.add((topicURI,Vocab.dbpedia_Link,rdflib.URIRef(dbpedia[i])))
        #     if lname is not None:
        #         g.add((topicURI,Vocab.taught_in,lname))
                
            
        #     continue
        #topicList.append(topicURI)
        graph.add((topicURI,RDF.type,Vocab.Topic))

        if lname is not None:
            g.add((topicURI,Vocab.taught_in,lname))
        
        g.add((topicURI,Vocab.belongs_to,cname))

        g.add((topicURI,Vocab.topic_name,rdflib.Literal(i)))
        g.add((topicURI,Vocab.provenance,filename))
        g.add((topicURI,Vocab.dbpedia_Link,rdflib.URIRef(dbpedia[i])))

        



        






#Create DB
db=DBsetup("http://localhost:3030")
db.create_db("IntSysProjectPhase2")

#Initialize Text Processer( this will setup spacy for medium english model)

# Get the base directory of the current Python script
base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)
phase_path = os.path.dirname(os.path.abspath(__file__+"/.."))
#loading Vocabularies

#Universities
g0=rdflib.Graph()
g0.parse(base_dir+"/../Vocabularies/university.ttl",format="ttl")

#Courses
g1=rdflib.Graph()
g1.parse(base_dir+"/../Vocabularies/courses.ttl",format="ttl")


#Student
g2=rdflib.Graph()
g2.parse(base_dir+"/../Vocabularies/students.ttl",format="ttl")


#studentCourses
g3=rdflib.Graph()
g3.parse(base_dir+"/../Vocabularies/studentCourses.ttl",format="ttl")

#lectures
g4=rdflib.Graph()
g4.parse(base_dir+"/../Vocabularies/lectures.ttl",format="ttl")

#topics
g5=rdflib.Graph()
g5.parse(base_dir+"/../Vocabularies/topics.ttl",format="ttl")

#Merging Vocanulary graphs
g=g0+g1+g2+g3+g4+g5

# f=open("sample.txt","w")
# f.write(g.serialize())
#Creating Name Spaces

#foaf=rdflib.Namespace("http://xmlns.com/foaf/0.1/")
#import sample data
# data=open("scripts/sampledata.json","r")
# data=json.loads(data.read())
#populate university

uniname=rdflib.URIRef("http://example.org/Data/"+"Concordia_University")
g.add((uniname,RDF.type,vivo.University))
g.add((uniname,Vocab.name,rdflib.Literal("Concordia University")))
g.add((uniname,Vocab.link,rdflib.URIRef("https://dbpedia.org/page/Concordia_University")))


courseLinks={"COMP6741":"https://aits.encs.concordia.ca/aits/public/top/courses/20214/05/COMP6741.html","COMP6231":"https://aits.encs.concordia.ca/aits/public/top/courses/20211/05/COMP6231.html"}
outlineLinks={"COMP6741":"lecture_content/COMP6744_471.pdf","COMP6231":"lecture_content/COMP6231.pdf"}
#populate courses
with open(base_dir+"/../Datasets/CU_SR_OPEN_DATA_CATALOG.csv","r",encoding="UTF-16",errors="ignore",newline='') as csvfile:
    courses=csv.reader(csvfile,quoting=csv.QUOTE_ALL)
    j=0
    for row in courses:
        if j == 0:
            j=1
            continue
        if row[5]!="LEC":
            continue
        cname=rdflib.URIRef("http://example.org/Data/"+row[1]+row[2])
        
        g.add((cname,RDF.type,vivo.Course))
        #g.add((cname,RDF.label,i["label"]))
        g.add((cname,Vocab.course_name,rdflib.Literal(row[3])))
        g.add((cname,Vocab.course_subject,rdflib.Literal(row[1])))
        g.add((cname,Vocab.course_number,rdflib.Literal(row[2])))
        g.add((cname,Vocab.has_credits,rdflib.Literal(row[4])))
        g.add((cname,Vocab.course_description,rdflib.Literal(row[7])))
        g.add((cname,Vocab.belongs_to,uniname))
        g.add((cname,Vocab.program_level,rdflib.Literal(row[-2])))
        if row[1]+row[2] in courseLinks:
            g.add((cname,RDFS.seeAlso,rdflib.URIRef(courseLinks[row[1]+row[2]])))
            

        if row[1]+row[2] in outlineLinks:
            g.add((cname,Vocab.course_outline,rdflib.URIRef(phase_path+"/"+outlineLinks[row[1]+row[2]])))
            handleTopic(rdflib.URIRef(phase_path+"/"+outlineLinks[row[1]+row[2]]),cname,None,g)

#populate LECTURE
with open(base_dir+"/../Datasets/LectureDetails.csv","r",errors="ignore",newline='') as csvfile:
    lectures=csv.reader(csvfile,quoting=csv.QUOTE_ALL)
    next(lectures,None)
    
    for row in lectures:
        lname=rdflib.URIRef("http://example.org/Data/"+row[1]+row[0]+"_"+row[2])
        cname=rdflib.URIRef("http://example.org/Data/"+row[1]+row[0])
        g.add((lname,rdflib.RDF.type,Vocab.Lecture))
        g.add((lname,Vocab.belongs_to,cname))
        g.add((lname,Vocab.lecture_number,rdflib.Literal(row[2])))
        g.add((lname,Vocab.lecture_name,rdflib.Literal(row[3])))
        if row[4]!="":
            worksheet=rdflib.URIRef(phase_path+"/"+row[4])
            g.add((worksheet,rdflib.RDF.type,Vocab.Worksheets))
            g.add((lname,Vocab.has_Content,worksheet))
            handleTopic(worksheet,cname,lname,g)
        if row[5]!="":
            readings=rdflib.URIRef(phase_path+"/"+row[5])
            g.add((worksheet,rdflib.RDF.type,Vocab.Readings))
            g.add((lname,Vocab.has_Content,readings))
            handleTopic(readings,cname,lname,g)
        if row[6]!="":
            others=rdflib.URIRef(phase_path+"/"+row[6])
            g.add((others,rdflib.RDF.type,Vocab.Other_Material))
            g.add((lname,Vocab.has_Content,others))
            handleTopic(others,cname,lname,g)
        if  row[7]!="":
            for i in row[7].split(","):
                slides=rdflib.URIRef(phase_path+"/"+i)
                g.add((slides,rdflib.RDF.type,Vocab.Slides))
                g.add((lname,Vocab.has_Content,slides))
                handleTopic(slides,cname,lname,g)
            

        if row[9]!="":
            for i in row[9].split(","):
                lab=rdflib.URIRef(phase_path+"/"+i)
                g.add((lab,rdflib.RDF.type,Vocab.Lab_Content))
                g.add((lname,Vocab.has_Content,lab))
                handleTopic(lab,cname,lname,g)
        
        g.add((lname,RDFS.seeAlso,rdflib.Literal(row[8])))

        
        
# #populate Topics
# with open(base_dir+"/../Datasets/Topic_Details.csv","r",errors="ignore",newline='') as csvfile:
#     topics=csv.reader(csvfile,quoting=csv.QUOTE_ALL)
#     next(topics,None)
#     for row in topics:
#         course=rdflib.URIRef("http://example.org/Data/"+row[2]+row[1])
        
#         tname=rdflib.URIRef("http://example.org/Data/"+row[3].replace(" ","_"))
#         for s,p,o in g.triples((None,Vocab.belongs_to,course)):
#             for ss,pp,oo in g.triples((s,Vocab.lecture_number,rdflib.Literal(row[0]))):
#                 g.add((tname,Vocab.taught_in,ss))
        
        
#         g.add((tname,RDF.type,Vocab.Topic))
#         #g.add((cname,RDF.label,i["label"]))
#         g.add((tname,Vocab.belongs_to,course))
#         g.add((tname,Vocab.topic_name,rdflib.Literal(row[3])))
#         g.add((tname,Vocab.provenance,rdflib.URIRef("file:////Users/hari/Intelligent_Systems_Project/Phase-1/"+row[4])))
#         if row[5]!="":
#             g.add((tname,Vocab.dbpedia_Link,rdflib.URIRef(row[5])))
#         if row[6]!="":
#             print(row[6])
#             g.add((tname,Vocab.wikidata_Link,rdflib.URIRef(row[6])))  
        

#populate Students
            
with open(base_dir+"/../Datasets/Students.csv","r",errors="ignore",newline='') as csvfile:
    students=csv.reader(csvfile,quoting=csv.QUOTE_ALL)
    next(students,None)
    for row in students:
        student=rdflib.URIRef("http://example.org/Data/"+row[0])
        g.add((student,RDF.type,vivo.Student))
        g.add((student,Vocab.student_id,rdflib.Literal(row[0])))
        g.add((student,FOAF.mbox,rdflib.Literal(row[2])))
        name=rdflib.URIRef("http://example.org/Data/"+"_".join(row[1].replace(" ","_").split(",")))
        g.add((name,RDF.type,Vocab.Name))
        g.add((name,FOAF.firstName,rdflib.Literal(row[1].split(",")[0])))
        g.add((name,FOAF.lastName,rdflib.Literal(row[1].split(",")[1])))
        g.add((student,Vocab.student_name,name))
        for s,p,o in g.triples((None,Vocab.name,rdflib.Literal(row[-1]))):
            g.add((student,Vocab.studies_at,s))
            break


#populate Students Courses
with open(base_dir+"/../Datasets/StudentsCourses.csv","r",errors="ignore",newline='') as csvfile:
    studentCourses=csv.reader(csvfile,quoting=csv.QUOTE_ALL)
    next(studentCourses,None)
    for row in studentCourses:
        student=rdflib.URIRef("http://example.org/Data/"+row[0])
        studentCourse=rdflib.URIRef("http://example.org/Data/"+row[0]+"_"+row[1]+row[2])
        course=rdflib.URIRef("http://example.org/Data/"+row[1]+row[2])
        retookCourse=False
        for s,p,o in g.triples((studentCourse,None,None)):
            if p==Vocab.retookCourse:
                g.set((s,p,rdflib.Literal(True)))
                retookCourse=True
        
        g.add((studentCourse,RDF.type,Vocab.StudentCourse))
        g.add((studentCourse,Vocab.grade,rdflib.Literal(row[-1])))
        g.add((studentCourse,Vocab.course,course))
        g.add((studentCourse,Vocab.retookCourse,rdflib.Literal(retookCourse)))
        g.add((student,Vocab.completed_courses,studentCourse))
        if retookCourse is False:
            for s,p,o in g.triples((None,Vocab.belongs_to,course)):
                if (s,RDF.type,Vocab.Topic) in g:
                    for ss,pp,oo in g.triples((s,Vocab.topic_name,None)):
                        g.add((student,Vocab.competencies,s))
        


        

    

        
f=open(base_dir+"/../GraphOutputTurtle.ttl","w")
f.write(g.serialize(format="ttl"))
f=open(base_dir+"/../GraphOutputNTrip.ttl","w")
f.write(g.serialize(format="nt"))

db.upload_ttl("GraphOutputNTrip.ttl")