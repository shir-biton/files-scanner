import os
import requests
import time

from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./files"

### VIRUSTOTAL CONSTS ###
VIRUSTOTAL_BASE_URL = "https://www.virustotal.com/api/v3"
VIRUSTOTAL_API_KEY = "7b796cd4b1043a7dabba77bd730374a9b3a1f31425b0c5fc54eaf5d89bc22fbf"


@app.route("/scan_file", methods=["POST"])
def upload_file():
    """
    Uploads a file to ./files directory
    """
    if "file" not in request.files:
            return make_response(jsonify({"error": "No file received"}), 400)

    input_file = request.files["file"]
    file_name = secure_filename(input_file.filename)
    input_file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

    return make_response(scan_file(file_name), 200)


def scan_file(file_name):
    """
    Gets local file name, sends to virustotal API and return the file's analysis
    :param file_name: Local file name (In ./files directory)
    :return: Virustotal json format analysis
    """
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    files = {"file": open(os.path.join(app.config["UPLOAD_FOLDER"], file_name), "rb")}

    res = requests.post(VIRUSTOTAL_BASE_URL + "/files", headers=headers, files=files)
    res_id = res.json()["data"]["id"]
    
    analysis_info = requests.get(VIRUSTOTAL_BASE_URL + f"/analyses/{res_id}", headers=headers)

    return analysis_info.json()


if __name__ == "__main__":
    app.run()