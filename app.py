import os
import requests
import time

from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename

from config import *

### APP CONFIG ###
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/scan_file", methods=["POST"])
def upload_file():
    """
    Receives and uploads a file to ./files directory
    """
    if "file" not in request.files:
        return make_response(jsonify({"error": "No file received"}), 400)

    try:
        input_file = request.files["file"]
        file_name = secure_filename(input_file.filename)
        input_file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

        return make_response(scan_file(file_name))
    except Exception as e:
        return make_response(jsonify({"error": "Bad Request"}), 400)


def scan_file(file_name):
    """
    Gets local file name, sends to virustotal API and return the file's analysis
    :param file_name: Local file name (In ./files directory)
    :return: Virustotal json format analysis
    """
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    try:
        files = {"file": open(os.path.join(app.config["UPLOAD_FOLDER"], file_name), "rb")}
    except:
        return {"error": "Invalid file path"}

    try:
        res = requests.post(VIRUSTOTAL_BASE_URL + "/files", headers=headers, files=files)
        res_id = res.json()["data"]["id"]
        
        analysis_info = requests.get(VIRUSTOTAL_BASE_URL + f"/analyses/{res_id}", headers=headers)

        # Check whether analysis is completed before sending response
        while analysis_info.json()["data"]["attributes"]["status"] != "completed":
            time.sleep(2)
            analysis_info = requests.get(VIRUSTOTAL_BASE_URL + f"/analyses/{res_id}", headers=headers)

        return analysis_info.json()
    except:
        return {"error": "Unable to connect to virustotal service"}
