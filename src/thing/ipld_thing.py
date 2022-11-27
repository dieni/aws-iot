# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
from ipld import marshal, unmarshal, multihash
from datetime import datetime

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "ac40od4fxn5tc-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "TestThing"
PATH_TO_CERTIFICATE = "src/thing/certs/DevelopmentThing/93523796c35ae6f042318e1d6ca9a1f088c71a5a83d5479c17ede2d668911b9f-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "src/thing/certs/DevelopmentThing/93523796c35ae6f042318e1d6ca9a1f088c71a5a83d5479c17ede2d668911b9f-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "src/thing/certs/DevelopmentThing/AmazonRootCA1.pem"
TOPIC = "test"


ASSET = {
    "machine_id": "0x67c979A67dfBd14FF387D2c05e326Fe3B4851738",
    # "machine_id": "0xD72648e4EAF14c7f0039b99924d7733FA57c1148",
    "data": {
        "timestamp": str(datetime.now()),
        "value": "3.0144",
        "unit": "kWh",
    }
}

def multihashed(asset: dict):
    marshalled = marshal(asset)
    hashed_marshalled = multihash(marshalled)
    return hashed_marshalled

def puplish_asset(asset: dict):
    asset_hash = multihashed(asset)
    print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
    connect_future = mqtt_connection.connect()
    connect_future.result()
    asset['cid'] = asset_hash

    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(asset), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(asset) + "' to the topic: " + f"{TOPIC}")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()

mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            # client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )



puplish_asset(ASSET)