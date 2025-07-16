from PyQt5 import QtCore, QtWidgets


class StudentInfoDialog(QtWidgets.QDialog):
    """
    A styled dialog to collect Student ID, Name, and Class.
    Returns (student_id, name, class_name) on OK, or None on Cancel/invalid.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("➤ New Student Registration")
        self.setFixedSize(360, 240)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        
        # — Stylesheet for card look —
        self.setStyleSheet("""
        QDialog {
          background: #F5F7FA;
        }
        QGroupBox {
          border: 2px solid #4A90E2;
          border-radius: 8px;
          margin-top: 10px;
          background: white;
        }
        QGroupBox:title {
          subcontrol-origin: margin;
          subcontrol-position: top center;
          padding: 0 8px;
          color: #4A90E2;
          font: bold 12pt "Segoe UI";
        }
        QLabel {
          font: 10pt "Segoe UI";
        }
        QLineEdit {
          border: 1px solid #D1D5DA;
          border-radius: 4px;
          padding: 4px;
          font: 10pt "Segoe UI";
        }
        QLineEdit:focus {
          border-color: #4A90E2;
        }
        QPushButton {
          padding: 6px 14px;
          border-radius: 4px;
          font: bold 10pt "Segoe UI";
        }
        QPushButton#ok {
          background-color: #28A745; color: white;
        }
        QPushButton#cancel {
          background-color: #DC3545; color: white;
        }
        """)

        # — Form fields in a group box —
        form_box = QtWidgets.QGroupBox("Student Info")
        form_layout = QtWidgets.QFormLayout(form_box)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.setFormAlignment(QtCore.Qt.AlignCenter)

        self.id_edit    = QtWidgets.QLineEdit()
        self.id_edit.setPlaceholderText("e.g. HE190791")
        self.name_edit  = QtWidgets.QLineEdit()
        self.name_edit.setPlaceholderText("Full Name")
        self.class_edit = QtWidgets.QLineEdit()
        self.class_edit.setPlaceholderText("e.g. CS2023")

        form_layout.addRow("Student ID:", self.id_edit)
        form_layout.addRow("Name:",       self.name_edit)
        form_layout.addRow("Class:",      self.class_edit)

        # — OK / Cancel buttons —
        btn_ok     = QtWidgets.QPushButton("OK")
        btn_ok.setObjectName("ok")
        btn_cancel = QtWidgets.QPushButton("Cancel")
        btn_cancel.setObjectName("cancel")

        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)

        # — Main layout —
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(form_box)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)
        main_layout.setContentsMargins(12, 12, 12, 12)

    def get_data(self):
        """Return (id, name, cls) or None if invalid/cancel."""
        if self.exec_() == QtWidgets.QDialog.Accepted:
            sid  = self.id_edit.text().strip()
            nm   = self.name_edit.text().strip()
            cls  = self.class_edit.text().strip()
            if sid and nm and cls:
                return sid, nm, cls
        return None
