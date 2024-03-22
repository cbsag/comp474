import json
import requests

class Query:
    def __init__(self):
        self.queries=json.loads(open("scripts/query.json","r").read())

        return
    
    def handleQuestion(self,question):
        if "List all courses offered by" in question and "within" in question:
            #q4
            university=question.split("List all courses offered by",1)[1].split("within the",1)[0].strip()
            subject=question.split("List all courses offered by",1)[1].split("within the",1)[1].strip()
            #print(university)
            #print("sub",subject)
            return self.queries["4"].format(university,subject)
        
        if "List all courses offered by " in question:
            #q1
            uni_name=question.split("List all courses offered by",1)[1].strip()
            #print(uni_name)
            return self.queries["1"].format(uni_name)
        if "In which courses is" in question:
            #q2
            topic=question.split("In which courses is",1)[1].split("discussed?",1)[0].strip()
            return self.queries["2"].format(topic)
            
        if "Which topics" in question and "are covered in" in question and "during" in question:
            #q3
            firstPart=question.split("Which topics are covered in ",1)[1]
            course=firstPart.split("during",1)[0].strip()
        
            lecture=firstPart.split("during",1)[1].strip().split("?",1)[0].strip()
            print(course,lecture)
            return self.queries["3"].format(course,lecture)
        
        
        
        if "How many credits is" in question:
            #q6
            course=question.split("How many credits is",1)[1].strip().split(" ",1)[0].strip()
            number=question.split("How many credits is "+course,1)[1].split("worth?",1)[0].strip()
            return self.queries["6"].format(number)
        if "For" in question:
            #q7
            course=question.split("For",1)[1].strip().split(" ")[0]
            number=question.split("For "+course,1)[1].split(", what additional resources",1)[0].strip()
            return self.queries["7"].format(number,course)
        
        if "Detail the content available for" in question:
            #q8
            lecnum=question.split("Detail the content available for",1)[1].split("in",1)[0].strip()
            course=question.split("Detail the content available for "+lecnum+" in",1)[1].strip().split(" ")[0]
            number=question.split("Detail the content available for "+lecnum+" in",1)[1].strip().split(" ")[1].replace(".","")
            return self.queries["8"].format(number,course,lecnum)
        
        if "What reading materials are recommended for studying" in question:
            #q9
            topic=question.split("What reading materials are recommended for studying",1)[1]
            topic=topic[0:topic.rfind("in")-3].strip()
            course=question.split("What reading materials are recommended for studying "+topic+" in",1)[1].split("?",1)[0].strip()
            
            return self.queries["9"].format(course,topic)
        
        if "What competencies does a student gain after completing" in question:
            #q10
            course=question.split("What competencies does a student gain after completing",1)[1].strip().split(" ")[0]
            number=question.split("What competencies does a student gain after completing",1)[1].strip().split(" ")[1][:-1]
            print(course,number)
            return self.queries["10"].format(number)
        if "What grades did" in question:
            #q11
            student=question.split("What grades did",1)[1].split("achieve in",1)[0].strip()
            firstName=student.split(" ")[0]
            lastName=" ".join(student.split(" ")[1:])
            course=question.split("What grades did "+student+" achieve in",1)[1].strip().split(" ")[0]
            number=question.split("What grades did "+student+" achieve in",1)[1].strip().split(" ")[1][:-1]
            return self.queries["11"].format(firstName,lastName,number)
        if "Which students have completed" in question:
            #q12
            course=question.split("Which students have completed",1)[1].strip().split(" ")[0]
            number=question.split("Which students have completed",1)[1].strip().split(" ")[1][:-1]
            return self.queries["12"].format(course,number)
        if "Print a transcript" in question:
            #q13
            student=question.split("Print a transcript for a",1)[1].split(", listing all the course taken with their grades.",1)[0].strip()
            firstName=student.split(" ")[0]
            lastName=" ".join(student.split(" ")[1:])
            return self.queries["13"].format(firstName,lastName)
        if "What" in question:
            #q5
            material=question.split("What",1)[1].split("are recommended for",1)[0].strip()
            topic=question.split("What",1)[1].split("are recommended for",1)[1].split("in",1)[0].strip()
            course=question.split("What",1)[1].split("are recommended for",1)[1].split("in",1)[1].strip().split(" ")[0]
            number=question.split("What",1)[1].split("are recommended for",1)[1].split("in",1)[1].strip().split(" ")[1].split("?")[0]
            return self.queries["5"].format(number,topic,material)

        
        
q=Query()
print(q.handleQuestion("Print a transcript for a Hari Guru Sai, listing all the course taken with their grades."))