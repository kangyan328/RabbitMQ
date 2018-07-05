# -*- coding:utf-8 -*-

import pika
import sys
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 创建消息队列
channel.queue_declare(queue='task_queue', durable=True)  # 设置消息队列持久化

message = ''.join(sys.argv[1:]) or 'Hello World'
channel.basic_publish(exchange='',
                      routing_key='task_queue',  # 指定发送的消息队列
                      body=message,
                      properties=pika.BasicProperties(  # 基本性能
                          delivery_mode=2,  # 设置消息持久化
                      ))
print '[x] Sent %r' % (message,)


