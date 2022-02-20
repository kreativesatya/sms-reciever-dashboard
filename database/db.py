import pymongo

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb+srv://root:root@cluster0.5lxod.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

def get_db():
    return client["SMS_RECIVER"]