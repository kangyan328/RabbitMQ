# -*- coding:utf-8 -*-

import pika
import sys

"""
生产者
# %2f 是被转义的‘/’ 这里使用了默认的虚拟主机和默认的用户及密码
# parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
# connection 就是所谓的消息代理
# connection = pika.BlockingConnection(parameters)
"""

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# 获取信道
channel = connection.channel()

# 声明交换机，指定交换类型为直接交换，最后两个参数表示想要持久化的交换机，
# 其中durable为True表示RabbitMQ在崩溃重启之后会重建队列和交换机
channel.exchange_declare(exchange='web_develop',  # 交换机(交换机名称)
                         exchange_type='direct',  # 直连交换机类型
                         passive=False,
                         durable=True,  # 持久化 ？？(消息代理重启后，队列依旧存在)
                         auto_delete=False  # 自动删除 ？？ (当最后一个消费者退订后即被删除)
                         )
if len(sys.argv) != 1:
    msg = sys.argv[1]  # 使用命令行参数作为消息体
else:
    msg = 'hah'

# 创建一个消息，delivery_mode为2表示让这个消息持久化，重启RabbitMQ页不会丢失。
# 使用持久化需要考虑为此付出的性能成本，如果开启次功能，强烈建议把消息存储在SSD上
props = pika.BasicProperties(content_type='text/plain',  # 内容类型
                             delivery_mode=2
                             )
# 接受确认消息（让它支持消息确认，支持的原理是确保basic_publish的返回值为True（mqp_producer_confirm.py））
# basic_publish 表示从发送路由键为xxx_routing_key，消息体为hah的消息给web_develop这个交换机
channel.confirm_delivery()
if channel.basic_publish('web_develop', 'xxx_routing_key',
                      msg, properties=props):
    print('Message publish was confirmed!!')
else:
    print('Message could not be confirmed!!!')

# 关闭链接
connection.close()
