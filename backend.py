# Necessary imports
import time
import requests
# import cv2
import mysql.connector

# Testing imports
# from PIL import Image
import sys


# Necessary variables
interval = 30
host = "https://auchan-qualif.easyvista.com/api/v1/50005/requests"


# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="water"
)

# Get data from database


def DBGet(stmt):
    mycursor = mydb.cursor()
    mycursor.execute(str(stmt))

    return mycursor.fetchall()

# Send data to a database


def DBPost(stmt, values):
    mycursor = mydb.cursor()
    mycursor.execute(stmt, values)
    mydb.commit()

# Image post-processing (Black-white, convert to binary)


# def PostProcess(img):
#     bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

#     API("ocr/", "unk", True, "latest",
#         cv2.threshold(img, 127, 255, cv2.THRESH_BINARY))

# Sends data to the API, and handles the raw response


def API(path, lang, do, mv, bin):
    response = requests.post(str(host) + str(path), data={"language": str(
        lang), "detectOrientation": bool(do), "model-version": str(mv), "body": str(bin)})

    LeakCheck(str([int(i) for i in ''.join(
        (ch if ch in '0123456789.-e' else ' ') for ch in response["text"]).split()]))


# Calculate delta, check for errors and leaks
def LeakCheck(data):
    db = DBGet("SELECT value, running FROM water ORDER BY time DESC LIMIT 1")

    if db:
        db = db[0]
        d = int(data) - int(db[0])

        running = db[1]
        err = False
        alarm = False

        if d < 0:
            err = True

        if d > 0:
            running += 1
            if running >= (86400/interval):
                alarm = True
        else:
            running = 0

        update = (int(data), running, err, alarm)

    else:
        update = (int(data), 0, False, False)

    DBPost("INSERT INTO water (value, running, alarm, error) VALUES (%s, %s, %s, %s)", update)


LeakCheck("12")


# Main loop, executes at set intervals
# while True:
#     time.sleep(interval)

#     PostProcess(Image.open(sys.argv[0]))
