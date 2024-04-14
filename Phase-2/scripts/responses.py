def firstQuestion(data):
    output="There are "+str(len(data))+" courses offered at "+data[0]["uniname"]["value"]+": \n"
    for index,item in enumerate(data):
        output+=str(index+1)+". "+item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["courses"]["value"]+'\n'
    return output

def secondQuestion(data):
    if len(data)==0:
        return "This topic is not covered in any of the courses."
    output="It is discussed in "
    for item in data[:-1]:
        output+=item["coursecode"]["value"]+item["coursenumber"]["value"]+" "+item["coursename"]["value"]+", "

    output+="and "+data[-1]["coursecode"]["value"]+data[-1]["coursenumber"]["value"]+" "+data[-1]["coursename"]["value"]
    output=output[:-1]+"."
    return output

def thirdQuestion(data):
    if len(data)==0:
        return "I couldn't find any topics related to the course covered in that lecture"
    
    output="The topics that are covered in Course "+data[0]["cname"]["value"]+" during Lecture "+data[0]["lecnum"]["value"]+" are "
    for item in data[:-1]:
            output+=item["topic"]["value"]+", "
        
    output+="and "+data[-1]["topic"]["value"]+"."
    return output

def fourthQuestion(data):
    if len(data)==0:
        return "I couldn't find any courses offered by the university for the subject"
    
    output="The courses offered by "+data[0]["uniname"]["value"]+" for subject "+data[0]["subject"]["value"]+" are\n"
    for index,item in enumerate(data):
            output+=str(index+1)+". "+item["cname"]["value"]+"\n"

   
    return output

def fifthQuestion(data):
    if len(data)==0:
        return "I couldn't find any material for the topic."
    output="The "+data[0]["label"]["value"]+" that are recommeded for "+data[0]["topic_name"]["value"]+" in Course "+data[0]["ccode"]["value"]+data[0]["cnum"]["value"]+" are "
    if len(data)==1:
        output+=data[-1]["x"]["value"]+"."
        return output
    for item in data[:-1]:
            output+=item["x"]["value"]+", "
        
    output+="and "+data[-1]["x"]["value"]+"."
    return output

def sixthQuestion(data):
    if len(data)==0:
        return "I couldn't find the credits for the course."
    output="The course has "+data[0]["credits"]["value"]+" credits."
    return output

def seventhQuestion(data):
    if len(data)==0:
        return "There are no additional resources available."
    
    output="For "+data[0]["cname"]["value"]+data[0]["cnum"]["value"]+" the additional resources are "
    if len(data)==1:
        output+=data[-1]["url"]["value"]
        return output
    for item in data[:-1]:
            output+=item["url"]["value"]+", "
        
    output+="and "+data[-1]["url"]["value"]
    return output

def eightQuestion(data):
    if len(data)==0:
        return "There are no content available for the course."
    
    output="There are "
    if len(data)==1:
        output+=data[-1]["count"]["value"]+" "+data[-1]["material"]["value"]
        return output
    for item in data[:-1]:
            output+=item["count"]["value"]+" "+item["material"]["value"]
        
    output+=" and "+data[-1]["count"]["value"]+" "+data[-1]["material"]["value"]+" available for lecture "+data[0]["lnum"]["value"]+" in course "+data[0]["cname"]["value"]+data[0]["cnum"]["value"]
    return output

def ninethQuestion(data):
    if len(data)==0:
        return "There are no reading materials for the topic in the course."
    
    output="The recommended materials are  "
    if len(data)==1:
        output+=data[-1]["readingstuff"]["value"]
        return output
    for item in data[:-1]:
            output+=item["readingstuff"]["value"]
        
    output+=" and "+data[-1]["readingstuff"]["value"]
    return output

def tenthQuestion(data):
    if len(data)==0:
        return "There are no information available for the course."
    
    output="The competencies students acquire are as follows:\n"
    for index,item in enumerate(data):
        output+=str(index+1)+". "+item["topicname"]["value"]+"\n"
    return output

def eleventhQuestion(data):
    if len(data)==0:
        return "There are no student information available."
    
    output="There grade of student "+data[0]["firstName"]["value"]+" in "+data[0]["cname"]["value"]+data[0]["cnum"]["value"]+" is "
    if len(data)==1:
        output+=data[-1]["grade"]["value"]+"."
        return output
    for item in data[:-1]:
            output+=item["grade"]["value"]
        
    output+=" and "+data[-1]["grade"]["value"]+". The student retook the course to acheive better grade."
    return output

def twelvethQuestion(data):
    if len(data)==0:
        return "There are no information available."
    
    output="The list of students who completed"+data[0]["coursecode"]["value"]+data[0]["number"]["value"]+" are as follows:\n"
    for index,item in enumerate(data):
        output+=str(index+1)+". "+item["student_id"]["value"]+"-"+item["firstname"]["value"]+" "+item["lastname"]["value"]+"\n"

    return output

def thirteenthQuestion(data):
    if len(data)==0:
        return "There are no transcript available."
    
    output="\t\t\t Transcript \t\t\t"
    output+="\n\tstudent name: "+data[0]["firstname"]["value"]+" "+data[0]["lastname"]["value"]+"\t\t student ID: "+data[0]["id"]["value"]
    output+="\nSNo.\tCOURSE CODE\tCOURSE NAME\t\t\tRETOOK COURSE\tGRADE\n\n"
    for index,item in enumerate(data):
        output+=str(index+1)+"\t"+item["coursecode"]["value"]+item["coursenumber"]["value"]+"\t"+item["coursename"]["value"]+"\t"+item["retook"]["value"]+"\t"+item["grade"]["value"]+"\n"

    return output