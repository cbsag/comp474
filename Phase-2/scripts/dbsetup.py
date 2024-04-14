import requests
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)
class DBsetup:
    def __init__(self,url):
        self.dburl=url

    def create_db(self,dbName):
        # Dataset configuration
        self.dbName=dbName
        config = {
            "dbType": "tdb",
            "dbName": dbName,
            "datasetDescription": "Dataset to store triples for first phase of the project"
        }
        endpoint = f'{self.dburl}/$/datasets'
        response = requests.post(endpoint, data=config)
        if response.status_code == 200:
            print("Dataset created successfully.")
        else:
            print("Failed to create dataset. Status code:", response.status_code)
            print(response.text)

        return 
    
    def upload_ttl(self,filename):
        g=open(base_dir+"/../"+filename,"r").read()
        sparql_update_query = f'''
            INSERT DATA {{
                {g}
            }}
            '''
        req=requests.post(f"{self.dburl}/{self.dbName}/update",data={"update":sparql_update_query},headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if req.status_code == 200:
            print("Data uploaded successfully.")
        else:
            print("Failed to uploade data. Status code:", req.status_code)
            print(req.text)    
      





if __name__=="__main__":
    dbsetup=DBsetup(url="http://localhost:3030")
    dbsetup.create_db(dbName="IntSysProj1")
    dbsetup.upload_ttl("GraphOutputNTrip.ttl")