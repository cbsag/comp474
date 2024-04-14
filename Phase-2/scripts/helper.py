from scripts import queryhelp
from scripts.query import Query
def handle_course(entity):
    print("helper running")
    if len(entity)==1:
        query=queryhelp.queriesList["1"]
        
        query=query.format(str(entity[0]["value"]).lower())
        print(query)
        q=Query()
        result=q.sendQuery(query)
       
       

    return result