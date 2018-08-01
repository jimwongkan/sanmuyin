import pymongo
from pymongo import *

client=None;
db_amazon=None;
productbaseinfo=None;
ip_add="192.168.20.7"
db_port=27017

def connectMongodb(host, port):
    count = 0
    global client
    while True:
        client = MongoClient(host, port, serverSelectionTimeoutMS=3)
        # client = MongoClient('mongodb://sanmuyin:0000@'+host+':'+str(port)+'/sanmuyin')
        # client.amazon.authenticate("sanmuyin", "0000", mechanism='SCRAM-SHA-1')
        try:
            client.amazon.command("ping")
        except ConnectionFailure:
            count = count + 1
        else:
            break
        if count == 3:
            return False
    return True

conn = connectMongodb(ip_add,db_port);
if(conn==True):
	print("connect mongodb success")
	db_amazon = client.amazon
	productbaseinfo = db_amazon.productbaseinfo
else:
	print("connect mongodb failure")


# conn = MongoClient("192.168.1.21",27017);
# print(conn)
# db = conn.sanmuyin#连接mydb数据库，没有则自动创建
# db.authenticate("sanmuyin","0000")
# amp = db.amazon_page#使用test_set集合，没有则自动创建
# amp.insert({"title":"this is a title","reviews":"232"})

