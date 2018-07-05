# -*- coding:utf-8 -*-
"""
生产者 Producer
"""

import pika
# 阻塞链接/链接参数/地址
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建链接信道(回话)
channel = connection.channel()

# queue_declare 声明队列，如果该消息队列不存在就创建
channel.queue_declare(queue='hello')  # 消息队列名称为hello

channel.basic_publish(exchange='',  # 指定交换机类型
                      routing_key='hello',  # 指定向那个消息队列发送
                      body='Hello world'  # 发送的内容
                      )

print "[x] Sent 'Hello World!!'"

# 关闭/断开链接
connection.close()