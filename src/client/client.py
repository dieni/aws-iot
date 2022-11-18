import time
import ssl

import paho.mqtt.client as mqtt

import logging
logging.basicConfig(level=logging.DEBUG)

PATH_TO_CERTIFICATE = "src/client/certs/DevelopmentInstance/e8d0b8d988a30043939a28a296485a832b15af4cf6fd849f4ea302cc1fc54793-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "src/client/certs/DevelopmentInstance/e8d0b8d988a30043939a28a296485a832b15af4cf6fd849f4ea302cc1fc54793-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "src/client/certs/DevelopmentInstance/AmazonRootCA1.pem"

HOST = "ac40od4fxn5tc-ats.iot.eu-central-1.amazonaws.com"
PORT = 8883

class Client():

    def __init__(self):
        self.mqttc = mqtt.Client()
        
    def set_connection(self):
        ''' Specify the connection profile '''
        self.host = HOST
        self.port = PORT
        self.mqttc.on_connect = self.__on_connect
        self.mqttc.on_message = self.__on_message
        self.mqttc.tls_set(PATH_TO_AMAZON_ROOT_CA_1, 
            certfile=PATH_TO_CERTIFICATE, 
            keyfile=PATH_TO_PRIVATE_KEY, 
            cert_reqs=ssl.CERT_REQUIRED, 
            tls_version=ssl.PROTOCOL_TLSv1_2, 
            ciphers=None)
        self.logger = logging.getLogger(repr(self))

    def start_listening(self, topics):
        ''' listens for incomming smart meter data '''

        self.topics = topics
        self.connected_flag = False
        while not self.connected_flag:
            try:
                self.mqttc.connect(host=self.host, port=self.port)
                self.mqttc.loop_forever()
            except Exception:
                self.logger.debug(f'{type(self).__name__} - Connecting to broker... retry in 5 seconds')
                time.sleep(5)

    # The callback for when the client receives a CONNACK response from the server.
    def __on_connect(self, mqttc, userdata, flags, rc):
        if rc == 0:
            self.logger.info(f'{type(self).__name__} - Connection to broker established')
            self.mqttc.subscribe(self.topics)
            self.connected_flag = True

        else:
            self.logger.error(f"{type(self).__name__} - Failed to connect to broker. Status Code:", rc)
            self.connected_flag = False

    # The callback for when a PUBLISH message is received from the server.
    def __on_message(self, mqttc, userdata, msg):
        self.logger.debug(f"{type(self).__name__} - TOPIC: " + msg.topic)

        try:
            self.process_raw_message(msg.payload)
        except Exception:
            self.logger.exception(f"{type(self).__name__} - Failed to process raw message!")

    def process_raw_message(self, msg):
        print(msg)


if __name__ == '__main__':
    client = Client()
    client.set_connection()
    client.start_listening(topics='test')