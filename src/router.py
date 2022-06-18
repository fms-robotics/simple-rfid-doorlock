# RESTful user management portal
# Copyright (c) 2019-2022, Ka-yiu Tam
# License: Apache-2.0 (see LICENSE for details)

import os
import json
from tinydb import TinyDB, Query
from bottle import Bottle, run, response, request

app = Bottle()

class CommonVariables:
    _config_path = "/../../../.config"
    _logs_path = "/../../../.logs"
    gpio_logs_path = (os.path.normpath(f"{__file__}{_logs_path}/gpio-logs.json"))
    users_data_path = (os.path.normpath(f"{__file__}{_config_path}/authorized_users.json"))

@app.get("/users")
def listusers():
    """list all users"""
    response.content_type = "application/json"
    return json.dumps(TinyDB(CommonVariables.users_data_path).all())

@app.post("/users")
def useradd():
    """Request like this
    curl -X POST -H 'Content-Type: application/json' http://0.0.0:8080/users -d '{"user_id":"s2170111","name": "CHAN TAI MAN","nfc":"200513441"}'"""
    db.insert(request.json)

@app.get("/logs")
def listlogs():
    response.content_type = "application/json"
    return json.dumps(TinyDB(CommonVariables.gpio_logs_path).all())

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080)