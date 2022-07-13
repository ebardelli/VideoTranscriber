import requests
import zipfile
import io

answer = input("Download Model (y/n)? ")

if answer.lower() in ["y","yes"]:
    URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip"
    response = requests.get(URL)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall("Models/")
elif answer.lower() in ["n","no"]:
    print("Skipping download. Moving on.")
else:
    print("Error. Please use y/n. Moving on.")

answer = input("Download Speaker Model (y/n)? ")

if answer.lower() in ["y","yes"]:
    URL = "https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip"
    response = requests.get(URL)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall("Models/")
elif answer.lower() in ["n","no"]:
    print("Skipping download. Moving on.")
else:
    print("Error. Please use y/n. Moving on.")

