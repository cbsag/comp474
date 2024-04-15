
import sys
sys.path.append('../../')
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from scripts.query import Query
from scripts.helper import handle_course
from scripts.queryhelp import queriesList
import re


class ActionContent(Action):

    def name(self) :
        return "action_info_contents"

    def recommend_courses(self,dispatcher, materials,topic,course):
        query=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["5"].format(cnum.lower(),cname.lower(),topic.lower(),materials.lower())
            print(query)
        else:
            #print(queriesList["5A"])
            query=queriesList["5A"].format(course.lower(),topic.lower(),materials.lower())

        res=Query().sendQuery(query=query)
        message=""
        for index,item in enumerate(res):
            message+=item["x"]["value"]+","

        message=message[0:-1]
        dispatcher.utter_message(
            template="utter_content",
            materials=materials,
            topic=topic,
            course=course,
            lists=message,
            number=course

        )

        return

    def additional_res(self,dispatcher,course):
        query=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["7"].format(cnum.lower(),cname.lower())
            print(query)
        else:
            query=queriesList["7A"].format(course.lower())

        res=Query().sendQuery(query=query)
        message=""
        for index,item in enumerate(res):
            message+=item["url"]["value"]+","

        
        if len(res)==0:
            dispatcher.utter_message(f"There are no additional resources available for the {course}")
            return

        message=message[0:-1]
        dispatcher.utter_message(
            template="utter_add_res",
          
            course=course,
            res=message,
            

        )
    def content_type(self,dispatcher,lecture,course):
        query=""
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
            query=queriesList["8"].format(cnum.lower(),cname.lower(),lecture)
            print(query)
        else:
            query=queriesList["8A"].format(course.lower(),lecture)
        res=Query().sendQuery(query=query)
        print(res)
        if len(res)==0:
            dispatcher.utter_message(
                f"There are no content available for lecture {lecture} in {course}"

            )
            return
        message=""
        for i in res:
            message+=i["count"]["value"]+" "+i["material"]["value"]+", "

        message=message[0:-2]
        dispatcher.utter_message(
            template="utter_course_types",
            lecture=lecture,
            course=course,
            types=message
        )
        return
    def reading_materials(self,dispatcher,topic,course):
        query=""
        if str(course).isalnum() and str(course.replace(" ","")[4:]).isdigit():
            course=course.replace(" ","")
            cname=course[0:4]
            cnum=course[4:]
            query=queriesList["9"].format(cnum.lower(),cname.lower(),topic.lower())
            print(query)
        else:
            query=queriesList["9A"].format(course.lower(),topic.lower())
        res=Query().sendQuery(query=query)
        if len(res)==0:
            dispatcher.utter_message(
                f"There are no reading materials available for topic {topic} in {course}"

            )
            return
        message=""
        for index,i in enumerate(res):
            message+=str(index+1)+". "+ i["readingstuff"]["value"]+"\n"

        message=message[0:-1]
        dispatcher.utter_message(
            template="utter_reading_materials",
            topics=topic,
            course=course,
            materials=message
        )
        return


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain) :
        print("here2")
        entities= tracker.latest_message.get('entities',[])
        ent={}
        for i in entities:
            ent[i["entity"]]=i["value"]
        print(ent)
        if len(entities)==1:
            self.additional_res(dispatcher,**ent)
            return []
        if(len(entities))==2 and "lecture" in ent and "course" in ent :
            self.content_type(dispatcher,**ent)
            return []
        if(len(entities))==2 and "topic" in ent and "course" in ent:
            self.reading_materials(dispatcher,**ent)

        if len(entities)==3:
            self.recommend_courses(dispatcher, **ent)
            return []

        dispatcher.utter_message(template="utter_fallback")
        return []