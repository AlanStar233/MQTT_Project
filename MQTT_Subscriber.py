# -*- coding: utf-8 -*-
"""
@File    : MQTT_Subscriber.py
@Author  : AlanStar
@Contact : alan233@vip.qq.com
@License : MIT
Copyright (c) 2022-2023 AlanStar
"""
import random
import time

import paho.mqtt.client as mqtt
from StatusCode import StatusCode

"""
    全局配置
    
    :param MQTT_Broker_IP: Broker(发布者) 地址
    :param MQTT_Broker_Port: Broker 端口
    :param MQTT_Node_Name: 节点名前缀
    :param MQTT_Anonymous: 是否同时允许多个节点
    :param MQTT_Timeout: 连接延时
    
    :param Topic_Name: 接收主题名称
    :param Callback_Function: 回调函数
"""

MQTT_Broker_IP = '192.168.31.55'
MQTT_Broker_Port = 1883
MQTT_Node_Name = "AlanStar_"
MQTT_Anonymous = True
MQTT_Timeout = 60

Topic_Name = "testMsg"
Callback_Function = None

# 连接成功回调
class MQTT_Subscriber:
    """
        MQTT 消息通讯
    """
    def __init__(self, central_ip=MQTT_Broker_IP, port=MQTT_Broker_Port, topic_name=Topic_Name, callback_func=Callback_Function,
                 node_name=MQTT_Node_Name, anonymous=MQTT_Anonymous, timeout=MQTT_Timeout):
        self.client = None  # 编译器建议
        self.topic = topic_name
        self.callback = callback_func
        self.broker_ip = central_ip
        self.broker_port = port
        self.timeout = timeout
        self.connected = False
        self.node_name = node_name
        # 如果允许多个节点连接
        if anonymous:
            self.node_name = self.node_name + str(random.randint(100000, 999999))   # 根据 Node_Name + 随机生成数字来生成客户端ID
        self.Start()

    def Start(self):
        """
            启动 Publisher
            :return:
        """
        self.client = mqtt.Client(self.node_name)   # 创建客户端
        self.client.on_connect = self.on_connect    # 指定回调函数
        self.client.on_message = self.default_on_message    # 指定默认接收消息
        self.client.connect(self.broker_ip, self.broker_port, self.timeout) # 开始连接
        self.client.subscribe(self.topic)   # 订阅指定主题, 准备监听
        self.client.loop_start()    # 开启一个独立循环通讯线程

    # 回调函数 default_on_message
    @staticmethod
    def default_on_message(client, userdata, msg):
        print(StatusCode.message() + msg.payload.decode('utf-8'))   # 输出

    # 回调函数 on_connect, 连接到 Broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
        else:
            raise Exception(StatusCode.error() + "Failed to connect MQTT Server...")


if __name__ == "__main__":
    mSubscriber = MQTT_Subscriber()
    while not mSubscriber.connected:
        pass
    while True:
        time.sleep(1)
