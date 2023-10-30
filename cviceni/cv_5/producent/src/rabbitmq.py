import pika
import logging
import logstash

logstash_logger = logging.getLogger()
logstash_logger.setLevel(logging.DEBUG)
logstash_logger.addHandler(logstash.TCPLogstashHandler("localhost", 5000, version=0))

conn_params = pika.ConnectionParameters(host='127.0.0.1')

def publish(msg: str):
    try:
        conn = pika.BlockingConnection(conn_params)
        channel = conn.channel()
        channel.basic_publish(
            exchange='',
            routing_key='wab_4',
            body=msg
        )
        conn.close()
        logging.info("Publish event '%s'", msg)
    except Exception as e:
        logging.error("Publish failed", e)