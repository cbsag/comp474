
import sys
sys.path.append('../../')
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from scripts.query import Query
from scripts.helper import handle_course
from scripts.queryhelp import queriesList
import re


class ActionStudent(Action):

    def name(self) :
        return "action_info_students"

    def getStudentGrades(self,dispatcher,student,course):
        query=""
        res=None
        studentName=False
        fname=""
        lname=""
        if str(student.replace(" ","")).isalpha():
            name=student.split(" ")
            fname=name[0]
            lname=" ".join(name[1:])
            studentName=True

        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            if studentName is True:
                query=queriesList["11"].format(cnum,cname.lower(),fname.lower(),lname.lower())
            else:
                query=queriesList["11A"].format(cnum,cname.lower(),student)
            print(query)
        else:
            if studentName is True:
                query=queriesList["11B"].format(course.lower(),fname.lower(),lname.lower())
            else:
                query=queriesList["11C"].format(course.lower(),student)
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(f"No record found for the student {student}")
            return
        if len(res)==1:
            dispatcher.utter_message(
                template="utter_studentgrade",
                student=student,
                grades=res[0]["grade"]["value"]+" grade",
                misc=""
            )
            return
        message=""
        for i in res:
            message+=i["grade"]["value"]+", "
        dispatcher.utter_message(
                template="utter_studentgrade",
                student=student,
                grades=message[0:-2]+" grades",
                misc="The student retook the course for better grades."
            )
        return
    


    def getStudentLists(self,dispatcher,course):
        query=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["12"].format(cnum,cname.lower())
            print(query)
        else:
            query=queriesList["12A"].format(course.lower())
        
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(f"No record found for the course {course}")
            return
        message=""
        for index,i in enumerate(res):
            message+=str(index+1)+". "+i["student_id"]["value"]+" - "+i["firstname"]["value"]+" "+i["lastname"]["value"]+"\n"
        dispatcher.utter_message(
            template="utter_lstofstudents",
            course=course,
            students=message
        )


        return
    
    def getTranscript(self,dispatcher,student):
        query=""
        studentName=False
        fname=""
        lname=""
        if str(student.replace(" ","")).isalpha():
            name=student.split(" ")
            fname=name[0]
            lname=" ".join(name[1:])
            studentName=True
        
        if studentName is True:
            query=queriesList["13"].format(fname.lower(),lname.lower())
        else:
            query=queriesList["13A"].format(student)
        print(query)
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(f"No record found for the student {student}")
            return
        message=""
        for index,item in enumerate(res):
            message+=str(index+1)+"\t"+item["coursecode"]["value"]+item["coursenumber"]["value"]+"\t"+item["coursename"]["value"]+"\t"+item["retook"]["value"]+"\t"+item["grade"]["value"]+"\n"
        dispatcher.utter_message(
            template="utter_transcript",
            student=student,
            table=message
        )


        return
    


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) :
        print("hereR")
        entities= tracker.latest_message.get('entities',[])
        ent={}
        print(ent)
        for i in entities:
            ent[i["entity"]]=i["value"]
        if len(entities) ==1 and "course" in ent:
            self.getStudentLists(dispatcher,ent["course"])
        if len(entities) ==1 and "student" in ent:
            self.getTranscript(dispatcher,ent["student"])
        if len(entities) == 2:
            self.getStudentGrades(dispatcher,**ent)
        dispatcher.utter_message(template="utter_fallback")
        return []