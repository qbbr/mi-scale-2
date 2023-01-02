from paho.mqtt import client as mqtt_client

from logger import log


class MqttPublisher:
    MQTT_CLIENT_ID = "python-qbbr-mi-scale-2"

    def __init__(self, host, port, user, passwd, topic):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.topic = topic
        self.client = None

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if 0 == rc:
                log.debug("connecting to MQTT broker successful")
            else:
                log.error("failed to connect, return code %d", rc)

        client = mqtt_client.Client(self.MQTT_CLIENT_ID, clean_session=False, userdata=None)
        client.username_pw_set(self.user, self.passwd)
        client.on_connect = on_connect
        client.connect(self.host, self.port)

        return client

    def publish(self, msg):
        if self.client is None:
            self.client = self.connect()
            self.client.loop_start()
        topic = self.topic
        result = self.client.publish(topic, msg)
        status = result[0]  # result: [0, 1]
        if 0 == status:
            log.info("sending '%s' to topic '%s' successful", msg, topic)
        else:
            log.error("failed to send message to topic '%s'", topic)

        if 0 == self.client.disconnect():
            log.debug("disconnected from MQTT broker successful")

        self.client.loop_stop()
        self.client = None
