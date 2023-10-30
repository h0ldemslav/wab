import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/wba_4_11h")
print(f"Databases: {client.list_database_names()}")
db = client.get_database('wab_4_11h')
print(f"{db.name} collections: {db.list_collection_names()}")
collection = db.get_collection('rabbit')
print(f"Open {collection.name}")


import pika

conn_params = pika.ConnectionParameters(host='127.0.0.1')
conn = pika.BlockingConnection(conn_params)
channel = conn.channel()
channel.queue_declare(queue="wab_4",
                      durable=True)

def on_message_callback(channel, method, properties, body):
    print(f"""
channel:   {channel}
method:    {method}
properties:{properties}
body:      {body}""")
    collection.insert_one({
        'msg': body.decode("utf-8")
    })
    
channel.basic_consume(queue="wab_4",
                      auto_ack=True,
                      on_message_callback=on_message_callback)
channel.start_consuming()
