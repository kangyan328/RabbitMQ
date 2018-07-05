# -*- coding:utf-8 -*-

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)  # 设置消息队列持久化
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    print '[x] Received %r ' % (body,)
    time.sleep(body.count('.'))
    print '[x] Done'

    # 消息重发
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_qos(prefetch_count=1)  # 同一时刻，一个工作者只处理一个消息
channel.basic_consume(callback,
                      queue='task_queue'
                      )
print 'hahhh'
channel.start_consuming()
