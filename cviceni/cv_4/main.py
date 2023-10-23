import pika

conn_params = pika.ConnectionParameters(host="127.0.0.1")
conn = pika.BlockingConnection(conn_params)

channel = conn.channel()
channel.queue_declare(queue="wab_4")

import pymongo

client = pymongo.MongoClient("mongodb://mongo:mongo@127.0.0.1/wab_4")
wab_4 = client.get_database("wab_4")

collection = wab_4.get_collection("rabbit") 
 
def callback(channel, method, properties, body):
    collection.insert_one({"msg": body})
    print(f"{channel}\n\n{method}\n\n{properties}\n\n{body}")

# callback zaregistrujeme jako posluchace

channel.basic_consume(queue="wab_4", auto_ack=True, on_message_callback=callback) # on message jakou metodu provolame kdyz mame tu spravu
channel.start_consuming()