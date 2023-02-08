# -*- coding: utf-8 -*-
"""
@File    : MQTT_Publisher.py
@Author  : AlanStar
@Contact : alan233@vip.qq.com
@License : MIT
Copyright (c) 2022-2023 AlanStar
"""
import paho.mqtt.client as mqtt
from StatusCode import StatusCode
import random
import time

"""
    全局配置
    
    :param MQTT_Broker_IP: Broker(发布者) 地址
    :param MQTT_Broker_Port: Broker 端口
    :param MQTT_Node_Name: 节点名前缀
    :param MQTT_Anonymous: 是否同时允许多个节点
    :param MQTT_Timeout: 连接延时
    
    :param Publish_QoS: 指定消息等级
    :param Publish_Retain: 状态机消息
"""

MQTT_Broker_IP = '192.168.31.55'
MQTT_Broker_Port = 1883
MQTT_Node_Name = "AlanStar_"
MQTT_Anonymous = True
MQTT_Timeout = 60

Publish_QoS = 0
Publish_Retain = False

# 连接成功回调
class MQTT_Publisher:
    """
        MQTT 消息通讯
    """
    def __init__(self, central_ip=MQTT_Broker_IP, port=MQTT_Broker_Port, node_name=MQTT_Node_Name, anonymous=MQTT_Anonymous, timeout=MQTT_Timeout):
        self.client = None  # 编译器建议
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
        self.client.connect(self.broker_ip, self.broker_port, self.timeout) # 开始连接
        self.client.loop_start()    # 开启一个独立循环通讯线程

    # 发布 MQTT 消息
    def Publish(self, topic, payload, qos=Publish_QoS, retain=Publish_Retain):
        # 如果已连接
        if self.connected:
            print(StatusCode.message() + f"[{topic}] " + payload)
            return self.client.publish(topic, payload=payload, qos=qos, retain=retain)
        else:
            raise Exception(StatusCode.error() + "Failed to create connection! MQTT Server may Offline...")

    # 回调函数 on_connect, 连接到 Broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
        else:
            raise Exception(StatusCode.error() + "Failed to connect MQTT Server...")


if __name__ == "__main__":
    mPublisher = MQTT_Publisher()
    while not mPublisher.connected:
        pass
    while True:
        mPublisher.Publish("testMsg", "This is testMsg...")
        mPublisher.Publish("Hello", "Hello MQTT!")
        time.sleep(1)
