# Copyright 2019-2020 I. Tam (@tamik@duck.com)

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
import sqlite3
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO_RELAY_PIN = 15
user_database = sqlite3.connect('/home/pi/411lock/userdata.db', check_same_thread=False)
cur = user_database.cursor()


def main():
    GPIO.setup(GPIO_RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)

    while True:
        nfc_code = input()
        cur.execute(
            f"SELECT COUNT(*) FROM users WHERE nfc_code = '{nfc_code}'")
        if int(cur.fetchone()[0]) != 0:
            GPIO.output(GPIO_RELAY_PIN, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(GPIO_RELAY_PIN, GPIO.HIGH)

        cur.execute(
            f"INSERT INTO logs VALUES ('{datetime.now()}','{nfc_code}') ")
        user_database.commit()


if __name__ == '__main__':
    main()
