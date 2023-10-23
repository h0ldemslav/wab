import pika

conn_params = pika.ConnectionParameters(host="127.0.0.1")
conn = pika.BlockingConnection(conn_params)

# pripojim se a vezmu ted kanal

channel = conn.channel()
channel.queue_declare(queue="wab_4")
# routing key - nazev te nase fronty
# body je message
channel.basic_publish(exchange="", routing_key="wab_4", body="Hello 1")

conn.close()