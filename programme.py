from arango import ArangoClient
import json
import os
import time


# Initialize the client for ArangoDB. And some other info need to type in
client = ArangoClient(hosts="http://localhost:8529")
sys_db = client.db("_system", username="root", password="")
path='E:\DAMG7275\DataP3'

# Initial and See if any file change
dicts = {}
zd = {}
def file_state(dic,path):
    file = os.listdir(path)
    for files in file:
        file_path = path+files
        if os.path.isfile(file_path):
            dic[file_path] = os.path.getmtime(file_path)
    return

file_state(zd,path)

# Begin loop to update the file
while True:
    time.sleep(3)
    file_state(dicts, path)
    for i in dicts:
        if dicts[i] == zd[i]:
            pass
        else:
            zd[i] = os.path.getmtime(i)
            filepath, tmpfilename = os.path.split(i)
            shotname, extension = os.path.splitext(tmpfilename)
            print(shotname + " is updated, something new will be update into database")
            coll = sys_db.collection(str(shotname)) #Open file and import into database
            with open(i) as fd:
                data = json.load(fd)
            coll.import_bulk(documents=data, on_duplicate ='update')
