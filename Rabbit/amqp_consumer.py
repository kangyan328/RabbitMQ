# -*- coding:utf-8 -*-

import pika
"""
消费者
处理接收到的消息的回调函数
method_frame携带了投递标记，
header_frame表示AMQP信息头的对象
body为消息实体
"""
def on_message(channel, method_frame, header_frame, body):
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    print(body)

parameters = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='web_develop',

                         exchange_type='direct',  # 直连交换机类型
                         passive=False,
                         durable=True,
                         auto_delete=False
                         )
# 声明队列，如果没有就创建
channel.queue_declare(queue='standard', auto_delete=True)

# 通过路由键将队列和交换机绑定
channel.queue_bind(queue='standard',  # 消息队列
                   exchange='web_develop',  # 交换机？？
                   routing_key='xxx_routing_key')

# 订阅队列
channel.basic_consume(on_message, 'standard')

try:
    channel.start_consuming()  # 开始消费
except KeyboardInterrupt:
    channel.stop_consuming()  # 停止消费

connection.close()
