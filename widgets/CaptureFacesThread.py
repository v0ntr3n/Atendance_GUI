import os

import cv2
import numpy as np
from PyQt5 import QtCore

from config.config import (
    CASCADE_PATH,
    IMAGES_PATH,
    LBPHFACE_PATH,
    MAX_SAMPLES,
    RTSP_URL,
)
from utils.pre_process import pre_processing


def TrainData():
    dict = {}
    labels = []
    for i in os.listdir(IMAGES_PATH):
        dict[i] = len(dict)
        labels.append(i)

    # Save labels
    with open("labels.txt", 'w+') as file:
        file.write('|'.join(labels))
    X_train = []
    y_train = []

    for users in os.listdir(IMAGES_PATH):
        users_path = os.path.join(IMAGES_PATH, users)
        lst_user = []

        for image in os.listdir(users_path):
            image_path = os.path.join(users_path, image)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            lst_user.append(img)
            y_train.append(dict[users])

        X_train.extend(lst_user)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(X_train, np.array(y_train))
    recognizer.write(LBPHFACE_PATH)

class CaptureFacesThread(QtCore.QThread):
    """
    QThread that grabs faces from a stream, saves them, and emits frames and progress.
    """

    frame_ready = QtCore.pyqtSignal(np.ndarray)  # np.ndarray frame
    progress_signal = QtCore.pyqtSignal(int)  # count of saved images
    finished = QtCore.pyqtSignal()

    def __init__(self, student_id=None, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self._stop = False

    def run(self):
        target_path = os.path.join(IMAGES_PATH, self.student_id)
        os.makedirs(target_path, exist_ok=True)
        cap = cv2.VideoCapture(RTSP_URL)
        count = 0

        while not self._stop and count < MAX_SAMPLES:
            ok, img = cap.read()
            if not ok:
                break
            img_pre = pre_processing(img)
            faces = self.face_cascade.detectMultiScale(img_pre, 1.3, 5)

            for x, y, w, h in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face = cv2.resize(img_pre[y : y + h, x : x + w], (100, 100))
                fname = f"{self.student_id}_{count + 1:03d}.jpg"
                cv2.imwrite(os.path.join(target_path, fname), face)
                count += 1
                self.progress_signal.emit(count)
                if count >= MAX_SAMPLES:
                    break

            self.frame_ready.emit(img)

        cap.release()
        TrainData()
        self.finished.emit()