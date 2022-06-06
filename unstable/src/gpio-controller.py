""" RFID dectector for RPi"""
# Copyright 2022 I. Tam (@tamik@duck.com)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import os
import json
from tinydb import TinyDB, Query
import RPi.GPIO as GPIO

class CommonVariables:
    _config_path = "/../../../.config"
    _logs_path = "/../../../.logs"
    gpio_logs_path = (os.path.normpath(f"{__file__}{_logs_path}/gpio-logs.json"))
    users_data_path = (os.path.normpath(f"{__file__}{_config_path}/authorized_users.json"))
    gpio_relay_pin = json.load(
        open(os.path.normpath(f"{__file__}{_config_path}/gpio-server.config.json"), 'r',encoding='utf8')
    )["gpio_relay_pin"]
    idVendor = json.load(
        open(os.path.normpath(f"{__file__}{_config_path}/gpio-server.config.json"), 'r',encoding='utf8')
    )["idVendor"]
    idProduct = json.load(
        open(os.path.normpath(f"{__file__}{_config_path}/gpio-server.config.json"), 'r',encoding='utf8')
    )["idProduct"]


def sesameopen():
    GPIO.output(CommonVariables.gpio_relay_pin, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(CommonVariables.gpio_relay_pin, GPIO.HIGH)


def if_user_exists(rfid_token):
    if not TinyDB(CommonVariables.users_data_path).search(Query().rfid == rfid_token):
        return False
    return True


def get_user_legal_name(rfid_token):
    return TinyDB(CommonVariables.users_data_path).search(Query().rfid == rfid_token)[0]['name']

def get_user_eclass_id(rfid_token):
    return TinyDB(CommonVariables.users_data_path).search(Query().rfid == rfid_token)[0]['eclass_id']


def hardware_logging(rfid_token):
    TinyDB(CommonVariables.gpio_logs_path).insert(
        {
            "timestamp": time.time(),
            "name": get_user_legal_name(rfid_token),
            "studentid": get_user_eclass_id(rfid_token)
        }
    )


def start():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CommonVariables.gpio_relay_pin, GPIO.OUT, initial=GPIO.HIGH)
    while True:
        current_input = input()
        if if_user_exists(current_input):
            sesameopen()
            hardware_logging(current_input)
