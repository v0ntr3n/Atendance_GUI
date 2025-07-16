
import json
from datetime import datetime

import cv2
import numpy as np
from PyQt5 import QtCore

from config.config import CASCADE_PATH, LBPHFACE_PATH, RTSP_URL
from utils import db_utils
from utils.pre_process import pre_processing


class VideoThread(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)
    update_attendance_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._run_flag = True
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

        self.font = cv2.FONT_HERSHEY_SIMPLEX

        db_utils.init_db()
        self.LBPH_init()
        self.load_data()



    def load_data(self):
        self.labels = open("labels.txt").read().split("|")


    def LBPH_init(self):
        self.recognize = cv2.face.LBPHFaceRecognizer_create()
        self.recognize.read(LBPHFACE_PATH)

    def Refresh_Data(self):
        self.load_data
        self.LBPH_init()

    def run(self):
        cap = cv2.VideoCapture(RTSP_URL)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                # frame = cv2.flip(frame, 1)
                pre_img = pre_processing(frame)
                faces = self.face_cascade.detectMultiScale(
                    pre_img, scaleFactor=1.3, minNeighbors=5
                )
                for x, y, w, h in faces:
                    id, confidence = self.recognize.predict(pre_img[y : y + h, x : x + w])
                    # confidence = " {0}%".format(round(100 - confidence))

                    if confidence < 100:
                        id = self.labels[id]
                        info = db_utils.get_student(id)
                        name = info["name"]
                        class_name = info["class"]
                        color = (0, 255, 0)
                    else:
                        id = "unknown"
                        name = "unknown"
                        class_name = "---"
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, str(int(confidence)), (x + 80, y - 5), self.font, 1, (255, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"Class: {class_name}",
                        (x + 5, y + h + 45),
                        self.font,
                        0.7,
                        (0, 255, 255),
                        2,
                    )
                    cv2.putText(
                        frame, f"MSSV: {id}", (x + 5, y + h + 70), self.font, 0.7, (0, 255, 255), 2
                    )
                    cv2.putText(
                        frame, f"Name: {name}", (x + 5, y + h + 95), self.font, 0.7, (0, 255, 255), 2
                    )
                    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    cv2.putText(frame, current_time, (10, 90), self.font, 0.8, (0, 255, 255), 2)
                    if id != 'unknown':
                        self.update_attendance_signal.emit(id)
                
                self.change_pixmap_signal.emit(frame)
                
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

