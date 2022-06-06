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

import sqlite3
import json
from datetime import datetime
from flask import Flask
from flask import request

user_database = sqlite3.connect('userdata.db', check_same_thread=False)
cur = user_database.cursor()
app = Flask(__name__)

@app.route("/users/create", methods=['PUT', 'POST'])
def user_create():
    """Create user via PUT or POST method to 'user' table.

    Command Sample for exact usuage:
    curl -X POST -H 'Content-Type: application/json' http://127.0.0.1:8000/create_user -d '{"user_id":"s2170111","name": "CHAN TAI MAN","nfc":"200513441"}'
    """
    try:
        user_res = request.get_json()
        cur.execute(
            f"INSERT INTO users VALUES (?,?,'{datetime.now()}',?)",
            [
                user_res['user_id'],
                user_res['name'],
                user_res['nfc']
            ])
        user_database.commit()
        return "Success"
    except KeyError:
        return "Failed! Possibly caused by formatting."
    except Exception as e:
        return str(e) 

@app.route("/users/list", methods=['PUT', 'POST', 'GET'])
def user_listing():
    """List all users.
    Accessible via Browser; Returns as JSON.
    """
    try:
        cur.execute('SELECT * FROM users')
        users_records = cur.fetchall()
        user_lists = []
        for row in users_records:
            user_objects = {
                "User ID": f"{row[0]}",
                "Name": f"{row[1]}",
                "Registration Date": f"{row[2]}",
                "NFC code": f"{row[3]}"
            }
            user_lists.append(user_objects)
        return json.dumps(user_lists)
    except Exception as e:
        return str(e) 

@app.route("/users/logs", methods=['PUT', 'POST', 'GET'])
def entry_logs():
    """List all entry records.
    Accessible via Browser; Returns as JSON.

    cURL usage:
    curl -X POST http://localhost:5000/users/list
    """
    cur.execute('SELECT * FROM logs')
    log_records = cur.fetchall()
    log_listings = []
    try:
        for row in log_records:
            cur.execute(
                f"SELECT COUNT(*) FROM users WHERE nfc_code = '{row[1]}'")
            if int(cur.fetchone()[0]) != 0:
                cur.execute(
                    "SELECT user_legal_name FROM users WHERE nfc_code = ? ORDER BY ROWID ASC LIMIT 1",
                    [row[1]]
                    )
                log_listings.append(
                    {
                        "Name": f"{cur.fetchone()[0]}",
                        "Entry Time": f"{row[0]}",
                        "NFC Code": f"{row[1]}"}
                    )
            else:
                log_listings.append(
                    {
                        "Name": "Unknown",
                        "Entry Time": f"{row[0]}",
                        "NFC Code": f"{row[1]}"}
                    )
        return json.dumps(log_listings)
    except Exception as e:
        return str(e) 

@app.route("/users/purge/<r_type>/<r_str>", methods=['PUT', 'POST'])
def user_remove(r_type=None, r_str=None):
    """Remove user via PUT or POST method from 'user' table.

    Command Sample for exact usuage:
    curl -X [POST|PUT] http://localhost:5000/users/purge/<r_type>/<r_str>
    curl -X POST http://127.0.0.1:5000/users/purge/user/user_id/s2150123

    Keyword arguments:
    r_type -- row name (e.g. user_id // nfc_code // ... )
    r_str -- row data (e.g. s2170135 // 133264005 // ... )
    """
    try:
        cur.execute(
            f"DELETE FROM users WHERE {r_type} = '{r_str}'"
            )
        user_database.commit()
        return "Success"
    except Exception as e:
        return str(e) 

if __name__ == '__main__':
    app.run(host="0.0.0.0")
