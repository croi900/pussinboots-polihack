import numpy as np
import cv2
import sys
import glob
import itertools as it
import os
first_frame = None
next_frame = None
delay_counter = 0
movement_persistent_counter = 0

def motion_detect(frame):

    FRAMES_TO_PERSIST = 10
    MIN_SIZE_FOR_MOVEMENT = 1000
    MOVEMENT_DETECTED_PERSISTENCE = 100

    transient_movement_flag = False

    global first_frame
    global next_frame
    global delay_counter
    global  movement_persistent_counter
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None: first_frame = gray

    delay_counter += 1


    if delay_counter > FRAMES_TO_PERSIST:
        delay_counter = 0
        first_frame = next_frame

    next_frame = gray

    frame_delta = cv2.absdiff(first_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    retvec = []

    for c in cnts:

        (x, y, w, h) = cv2.boundingRect(c)

        if cv2.contourArea(c) > MIN_SIZE_FOR_MOVEMENT:
            transient_movement_flag = True
            retvec.append((x, y, x + w, y + h))

    if transient_movement_flag == True:
        movement_persistent_flag = True
        movement_persistent_counter = MOVEMENT_DETECTED_PERSISTENCE


    if movement_persistent_counter > 0:
        movement_persistent_counter -= 1

    frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)

    return retvec

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def overlap_driven(l1, r1, l2, r2):
    if l1["x"] == r1["x"] or l1["y"] == r1["y"] or r2["x"] == l2["x"] or l2["y"] == r2["y"]:
        return False

    if l1["x"] > r2["x"] or l2["x"] > r1["x"]:
        return False

    if r1["y"] > l2["y"] or r2["y"] > l1["y"]:
        return False

    return True


def overlap(r1, r2):
    if (r1[0] >= r2[2]) or (r1[2] <= r2[0]) or (r1[3] <= r2[1]) or (r1[1] >= r2[3]):
        return False
    else:
        return True


def ingest(cam):
    # cam = cv2.VideoCapture(1)

    # cam = cv2.VideoCapture("http://192.168.137.205:4747/video")

    cascades = ["/home/croi/polipy/fbcs.xml", "/home/croi/polipy/harcascade_fullbody.xml"]#"haarcascade_lowerbody.xml", "haarcascade_upperbody.xml"]

    while True:
        detections = []
        ret, img = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        md_img = img.copy()
        # md_img = cv2.cvtColor(md_img, cv2.COLOR_BGR2GRAY)
        for file in cascades:
            if os.path.isfile(file):
                cascade = cv2.CascadeClassifier(file)

                width = int(img.shape[1] * 0.5)
                height = int(img.shape[0] * 0.5)

                img = cv2.resize(img, (width, height))
                if file.find("haar"):
                    rect = cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=6)
                else:
                    rect = cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=6)

                mvrects = motion_detect(md_img)

                for (x, y, w, h) in rect:
                    moving = False
                    mvtresh = 1
                    mvdets = 0
                    for movement in mvrects:
                        if overlap((x, y, x + w, y + h), movement):
                            mvdets += 1
                    if mvdets >= mvtresh:
                        moving = True

               

                    if moving:
                        detections.append(1)

            cv2.waitKey(1)
        #motion_detect(md_img)
        #cv2.imshow("img", img)
        # yield len([x for x in detections if x[1] > 1]) > 0
        yield len(detections)

def run_service(source, sid):
    source = cv2.VideoCapture(source)
    while True:
        sample_sum = 0
        samples = 0
        for sample in ingest(source):
            sample_sum += sample
            samples += 1
            if(samples >= 64): break
        if sample_sum/64 < 0.05:
            os.system(f"echo \"{sid}\" > ~/polipy/roomsqueue.txt")
            
            print(sid)

if __name__ == "__main__":
    # print("started detection service")
    run_service(0,1)
# import cv2
# import mediapipe as mp
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_pose = mp.solutions.pose

# # For webcam input:
# def ingest():
#     cap = cv2.VideoCapture(0)
#     with mp_pose.Pose(
#             min_detection_confidence=0.5,
#             min_tracking_confidence=0.5) as pose:
#         while cap.isOpened():
#             success, image = cap.read()
#             if not success:
#                 print("Ignoring empty camera frame.")
#                 continue

#             image.flags.writeable = False
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             results = pose.process(image)

#             print(results)
#     cap.release()
