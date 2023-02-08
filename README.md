# MQTT_Project

## 一、文件构成

### 1.1 MQTT_Publisher.py

> **MQTT 发布者 class**



### 1.2 MQTT_Subscriber.py

> **MQTT 订阅者 class**



## 二、部署方式

### 2.1 EMQX Broker

​	可见教程：https://www.emqx.io/docs/zh/v5.0/

## 三、调试

### 3.1 调试过程

1. 启动 **EMQX**，获取其**IP地址**和**端口号**(默认 Broker Port **1883**)。
2. 启动 **MQTT_Publisher** ，在此之前可自定义发布的 Topic 和内容。
3. 启动 **MQTT_Subscriber** ，同上，可修改其订阅的主题，在 Subscriber 的终端上将实时回显其收到的对应主题的消息。
