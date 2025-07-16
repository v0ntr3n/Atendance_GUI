import sys

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from config.config import MAX_SAMPLES
from utils import db_utils

# from utils.pre_process import pre_processing
from widgets.CaptureFacesThread import CaptureFacesThread
from widgets.CircularProgress import CircularProgressBar
from widgets.StudentInfoDialog import StudentInfoDialog
from widgets.VideoCapture import VideoThread


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance App")
        self.setFixedSize(900, 520)

        # Shared face cascade
        self.attendance = set()

        # Central widget & layout
        central = QtWidgets.QWidget(self)
        self.setCentralWidget(central)
        main_layout = QtWidgets.QHBoxLayout(central)

        # Video frame with border and shadow
        video_frame = QtWidgets.QFrame()
        video_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        video_frame.setStyleSheet(
            "QFrame { border: 2px solid #4A90E2; border-radius: 10px; background: #F5F7FA; }"
        )
        v_layout = QtWidgets.QVBoxLayout(video_frame)
        self.image_label = QtWidgets.QLabel()
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet("border: none; border-radius: 8px;")
        v_layout.addWidget(self.image_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(video_frame)

        # Sidebar for attendance and controls
        sidebar = QtWidgets.QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            "QFrame { background: #FFFFFF; border-left: 2px solid #E1E8ED; }"
        )
        side_layout = QtWidgets.QVBoxLayout(sidebar)
        side_layout.setContentsMargins(10, 10, 10, 10)

        label = QtWidgets.QLabel("Attendance List")
        label.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
        side_layout.addWidget(label)

        self.attendance_list = QtWidgets.QListWidget()
        self.attendance_list.setStyleSheet(
            "QListWidget { border: 1px solid #D1D5DA; border-radius: 5px; padding: 5px; }"
        )
        side_layout.addWidget(self.attendance_list)

        # Buttons
        btn_style = (
            "QPushButton { padding: 8px; border-radius: 5px; font-size: 10pt; }"
            "QPushButton#start { background-color: #28A745; color: white; }"
            "QPushButton#stop { background-color: #DC3545; color: white; }"
            "QPushButton#add { background-color: #28A745; color: white; }"
        )
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.setObjectName("start")
        self.start_button.setStyleSheet(btn_style)
        self.start_button.clicked.connect(self.start_capture)

        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setObjectName("stop")
        self.stop_button.setStyleSheet(btn_style)
        self.stop_button.clicked.connect(self.stop_capture)
        self.stop_button.setEnabled(False)


        self.add_button = QtWidgets.QPushButton("Add Student")
        self.add_button.setObjectName("add")
        self.add_button.setStyleSheet(btn_style)
        self.add_button.clicked.connect(self.prompt_student_info)

        self.circular = CircularProgressBar(self.image_label, diameter=80)
        self.circular.setRange(0, MAX_SAMPLES)
        self.circular.hide()
        side_layout.addSpacing(10)
        side_layout.addWidget(self.start_button)
        side_layout.addWidget(self.stop_button)
        side_layout.addWidget(self.add_button)
        side_layout.addSpacing(20)
        side_layout.addWidget(self.circular)
        side_layout.addStretch()
        side_layout.setAlignment(self.circular, QtCore.Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(sidebar)

        # Thread setup
        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        self.video_thread.update_attendance_signal.connect(self.update_attendance)

        self.capture_thread = CaptureFacesThread()
        self.capture_thread.frame_ready.connect(self.update_image)
        self.capture_thread.progress_signal.connect(self.on_capture_progress)
        self.capture_thread.finished.connect(self.on_capture_finished)

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    @QtCore.pyqtSlot(str)
    def update_attendance(self, StudentID):
        if StudentID not in self.attendance:
            self.attendance.add(StudentID)
            self.attendance_list.addItem(StudentID)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888
        )
        return QtGui.QPixmap.fromImage(qt_format).scaled(
            640, 480, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
        )
    
    # Capture Face Data
    @QtCore.pyqtSlot(int)
    def on_capture_progress(self, count):
        # update a QProgressBar
        self.circular.setValue(count)
    
    @QtCore.pyqtSlot()
    def on_capture_finished(self):
        self.video_thread.Refresh_Data()
        QtWidgets.QMessageBox.information(self, "Done", f"Captured {MAX_SAMPLES} faces.")
        self.circular.hide()
    # --------------

    def start_capture(self):
        self.video_thread._run_flag = True
        self.video_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_capture(self):
        self.video_thread.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def closeEvent(self, event):
        self.video_thread.stop()
        event.accept()

    def prompt_student_info(self):
        dialog = StudentInfoDialog()
        
        result = dialog.get_data()
        if result:
            student_id, name, class_name = result
            db_utils.add_student(student_id, name, class_name)

            self.circular.show()
            self.capture_thread.student_id = student_id
            self.capture_thread.start()
        
        return None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
