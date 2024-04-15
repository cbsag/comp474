
import sys
sys.path.append('../../')
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from scripts.query import Query
from scripts.helper import handle_course
from scripts.queryhelp import queriesList
import re


class ActionTopics(Action):

    def name(self) :
        return "action_info_topics"

    def find_courses(self,topic,dispatcher:CollectingDispatcher):
        
        q=queriesList["2"].format(topic.lower())
        query=Query()
        res=query.sendQuery(q)
        message=""
        if len(res)>0:
            print(res)
            message+=""
            for index,item in enumerate(res):
                message+=str(index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["coursename"]["value"]+"\n"
            dispatcher.utter_message(
                template="utter_topic",
                topic=topic,
                courses=message
            )
        else:
            dispatcher.utter_message(
                f"No courses were found for the topic {topic}"
            )
            


        return 
    def find_course_event(self,dispatcher,course):
        return

    def find_lecture_topics(self,dispatcher,course,lecture):
        query=""
        res=None
        if str(lecture).isdigit() is not True:
            # Define a regular expression pattern to match numbers
            pattern = r'\b(\d+)\b'
            
            match = re.search(pattern, lecture)
            if match:
                lecture = str(int(match.group(1)))
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["3A"].format(cname.lower(),cnum,lecture)
            print(query)
        else:
            query=queriesList["3"].format(course.lower(),lecture)
        res=Query().sendQuery(query=query)
        if len(res)>0:
            print(res)
            message=""
            for index,item in enumerate(res):
                message+=str(index+1)+". "+item["topic"]["value"]+"\n"
            dispatcher.utter_message(
                template="utter_topics",
                topic=message,
                courses=course,
                lecture=lecture,
            )
        else:
            dispatcher.utter_message(
                f"No topics were found for the lecture {lecture} of course {course}"
            )

        return
    

    def competencies(self,dispatcher, course):
        query=""
        res=None
        
        if str(course.replace(" ","")).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["10"].format(cnum,cname.lower())
            print(query)
        else:
            query=queriesList["10A"].format(course.lower())

        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(
                f"The competencies for {course} is not available"

            )
            return
        message=""
        for index,i in enumerate(res):
            message+=str(index+1)+". "+ i["topicname"]["value"]+"\n"

        message=message[0:-1]
        dispatcher.utter_message(
            template="utter_compentencies",
            topics=message,
            course=course,
          
        )
        return
    def get_course_events(self,dispatcher,course,event,number):
        eve=event
        query=""
        res=None
        if str(number).isdigit() is not True:
            # Define a regular expression pattern to match numbers
            pattern = r'\b(\d+)\b'
            
            match = re.search(pattern, number)
            if match:
                number = str(int(match.group(1)))
        if "lab" in event.lower():
            event=" FILTER(lcase(str(?event)) = \'lab content\')"
        else:
            event=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["15"].format(cnum,cname.lower(),number,event)
            print(query)
        else:
            query=queriesList["15A"].format(course.lower(),number,event)
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(f"No event information found for {eve} {number} of {course} ")
            return
        message=""
        topic=[]
        index=0
        for i in res:
            if i["topics"]["value"] in topic:
                continue
            topic.append(i["topics"]["value"])
            if "dblink" not in i:
                message+=str(index+1)+". "+ i["topics"]["value"]+" - "+i["wikilink"]["value"]+"\n"
                index+=1
                continue
            if "wikilink" not in i:
                message+=str(index+1)+". "+ i["topics"]["value"]+" - "+i["dblink"]["value"]+"\n"
                index+=1
                continue
            message+=str(index+1)+". "+ i["topics"]["value"]+"-"+i["dblink"]["value"]+" "+i["wikilink"]["value"]+"\n"
            index+=1
        dispatcher.utter_message(
            template="utter_courseevent",
            event=eve,
            number=number,
            course=course,
            topics=message)



    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) :
        entities= tracker.latest_message.get('entities',[])
       
        ent={}
        for i in entities:
            ent[i["entity"]]=i["value"]
        print(ent)
        if len(entities)==1 and "topic" in ent:
            response=self.find_courses(entities[0]['value'],dispatcher)
            return
        if len(entities)==1 and "course"in ent :
            self.competencies(dispatcher,**ent)
            return
        if len(entities)==3:
            self.get_course_events(dispatcher,**ent)
            return
        if len(entities)==2:
            lecture=""
            course=""
            if entities[0]['entity']=='course':
                course=entities[0]['value']
                lecture=entities[1]['value']
            else:
                course=entities[1]['value']
                lecture=entities[0]['value']
            response=self.find_lecture_topics(dispatcher,course,lecture)
        dispatcher.utter_message(template="utter_fallback")
        return []