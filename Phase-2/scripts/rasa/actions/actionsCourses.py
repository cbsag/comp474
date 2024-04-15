# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
import sys
sys.path.append('../../')
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from scripts.query import Query

from scripts.helper import handle_course
from scripts.queryhelp import queriesList

courses = None
nextIndex=0
offset=10
class ActionCoursesAll(Action):

    def name(self) :
        return "action_course"

    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain) :
    #     uniname=tracker.get_slot('university')
    #     query1=query.Query()
    #     query1.currQuestion="1"
    #     q=query1.queries["1"].format(uniname,uniname)
    #     resp=query1.sendQuery(q)
    #     #print(resp)
    #     dispatcher.utter_message(text=resp[0: resp.find("101.")-1])
    #     return []
    def course_credits(self,dispatcher,course):
        query=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["6"].format(cnum,cname.lower())


        else:
            return
        
        res=Query().sendQuery(query)
        print(query)
        print(res)
        if res==0:
            dispatcher.utter_message(
            f"No such course {course} found"
            )
            return
        dispatcher.utter_message(
            template="utter_credit",
            course=course,
            credit=res[0]["credits"]["value"]
        )
        return 



    def uni_courses(self,dispatcher,uniname):
        global nextIndex
        global offset
        global courses
        courses=None
        query=queriesList["1"]
        
        query=query.format(str(uniname).lower())
        print(query)
        q=Query()
        courses=q.sendQuery(query)
        message=""
        num=len(courses)
        if len(courses) >10:
            op=courses[0:offset+nextIndex]
            nextIndex=offset+nextIndex

            
            for index,i in enumerate(op):
                item=op[index]
                message+=str(index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["courses"]["value"]+"\n"
        else:
            for index,i in enumerate(courses):
                item=op[index]
                message+=str(index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["courses"]["value"]+"\n"
        if len(courses) ==0:
            dispatcher.utter_message(f"No information found for university {uniname}")

        dispatcher.utter_message(
            template="utter_course",
            num=num,
            uni=uniname,
            first10="\n"+message
        )   
        return
    
    def sub_courses(self,dispatcher,university,subject):
        global nextIndex
        global offset
        global courses
        nextIndex=0
        query=queriesList["4"]
        
        query=query.format(str(university).lower(),subject.lower())
        q=Query()
        courses=q.sendQuery(query)
        print(query)
        message=""
        num=len(courses)
        
        if len(courses) >10:
            op=courses[0:offset+nextIndex]
            nextIndex=offset+nextIndex

            
            for index,i in enumerate(op):
                item=op[index]
                message+=str(index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["courses"]["value"]+"\n"
        else:
            for index,i in enumerate(courses):
                item=op[index]
                message+=str(index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["courses"]["value"]+"\n"
        dispatcher.utter_message(
            template="utter_course_subject",
            num=num,
            uni=university,
            subject=subject,
            first10="\n"+message
        )   
        return
    def course_desc(self,dispatcher,course):
        query=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["14A"].format(cnum,cname.lower())
        else:
            query=queriesList["14"].format(course.lower())
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(f"No description record found for course {course}")
            return
        elif res[0]["desc"]["value"].strip()=="":
            dispatcher.utter_message(f"No description record found for course {course}")
            return
        dispatcher.utter_message(
            template="utter_description",
            course=course,
            description=res[0]["desc"]["value"].strip()

        )

    def course_events(self,dispatcher,topic):
        query=queriesList["16"].format(topic.lower())
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(f"Course event information not available for {topic}")
            return
        message=""
        for index,i in enumerate(res):
            message+=str(index+1)+". count: "+i["count"]["value"]+" CNAME: "+i["cname"]["value"]+" EVENT: "+i["event"]["value"]+" LEC NO: "+i["lnum"]["value"]+"\n"

        dispatcher.utter_message(
            template="utter_coursetopics",
            topic=topic,
            topics=message
        )
        

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) :
        print("here3")
        global nextIndex
        global courses
        global offset
        
        entities= tracker.latest_message.get('entities',[])
        print(entities)
        ent={}
        for i in entities:
            ent[i["entity"]]=i["value"]
    
        latest_message = tracker.latest_message.get('text', '')
        if len(entities)==1 and entities[0]["entity"]=="university":
            self.uni_courses(dispatcher,entities[0]["value"])
        elif len(entities)==1 and entities[0]["entity"]=="course" and "credit" in latest_message.lower():
            courses=None
            self.course_credits(dispatcher,entities[0]["value"])
        elif len(entities)==1 and entities[0]["entity"]=="course" :
            self.course_desc(dispatcher,entities[0]["value"])
        elif len(entities)==1 and entities[0]["entity"]=="topic":
            self.course_events(dispatcher,entities[0]["value"])
        elif len(entities)==2:
            print("here2")
            self.sub_courses(dispatcher,**ent)
        dispatcher.utter_message(template="utter_fallback")

class ActionPrintOffset(Action):

    def name(self) :
        return "action_next_offsets"

    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain) :
    #     uniname=tracker.get_slot('university')
    #     query1=query.Query()
    #     query1.currQuestion="1"
    #     q=query1.queries["1"].format(uniname,uniname)
    #     resp=query1.sendQuery(q)
    #     #print(resp)
    #     dispatcher.utter_message(text=resp[0: resp.find("101.")-1])
    #     return []
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) :
        global nextIndex
        global courses
        global offset
        current_intent = tracker.latest_message['intent'].get('name')
        entities= tracker.latest_message.get('entities',[])
        result=[]
        off=offset
        indexVal=nextIndex
        print(len(courses),"courses",nextIndex)
        if len(entities)>0:
            newOff=nextIndex+int(entities[0]["value"])
            print(newOff,"off")
            if newOff >= len(courses):
                newOff=len(courses)
            print(nextIndex,"next")
            off=newOff-nextIndex
            result=courses[nextIndex:newOff]
            print(result)
            nextIndex=newOff
        else:
            print("nextIndex",nextIndex,offset)
            newOff=nextIndex+offset
            off=newOff-offset
            if newOff >= len(courses):
                newOff=len(result)
            result=courses[nextIndex:newOff]
            
            nextIndex=newOff

        message="\n"
        for index,i in enumerate(result):
            item=result[index]
            message+=str(indexVal+index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["courses"]["value"]+"\n"

        if len(result)==0:  
            dispatcher.utter_message(text="There are no more courses to display")
            return []
        
        dispatcher.utter_message(template="utter_next_offset",num=off,next=message)
        return []   