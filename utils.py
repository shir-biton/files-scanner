import os
import requests
import time

from config import UPLOAD_FOLDER, VIRUSTOTAL_BASE_URL, VIRUSTOTAL_API_KEY

def scan_file(file_name):
    """
    Gets local file name, sends to virustotal API and return the file's analysis
    :param file_name: Local file name (In ./files directory)
    :return: Virustotal json format analysis
    """
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    try:
        files = {"file": open(os.path.join(UPLOAD_FOLDER, file_name), "rb")}
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
