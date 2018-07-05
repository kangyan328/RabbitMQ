# -*- coding:utf-8 -*-
"""
消费者 Consumer
"""
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 查看RabbitMQ中有哪些队列、有多少消息在队列中。
# sudo rabbitmqctl list_queues
channel.queue_declare('hello')  # 确认消息队列是否存在，不存在则创建

# 定义一个回调函数，该回调函数会将接收道德消息内容输出到屏幕上
def callback(ch, method, properties, body):
    print "[x] Received % r" % body

# 启动队列消费者，告诉rabbitMQ这个回调函数将会从名为'hello'的消息队列中接收消息
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print '[*] Waiting for message. To exit press CTRL+C'
channel.start_consuming()
