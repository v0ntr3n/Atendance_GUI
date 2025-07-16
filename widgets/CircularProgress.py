
from PyQt5 import QtCore, QtGui, QtWidgets

from config.config import MAX_SAMPLES


class CircularProgressBar(QtWidgets.QWidget):
    """
    A circular progress bar with percentage in the center.
    """
    def __init__(self, parent=None, max_samples=MAX_SAMPLES, diameter=100):
        super().__init__(parent)
        self._min = 0
        self._max = max_samples
        self._value = 0
        self.setFixedSize(diameter, diameter)
        self._pen_width = 8
        self._font = QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold)

    def setRange(self, minimum, maximum):
        self._min = minimum
        self._max = maximum
        self.update()

    def setValue(self, val):
        self._value = max(self._min, min(val, self._max))
        self.update()

    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        margin = self._pen_width // 2

        rect = QtCore.QRect(margin, margin, width - margin*2, height - margin*2)
        start_angle = 90 * 16
        span_angle = -int(360 * (self._value - self._min) / (self._max - self._min)) * 16

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Draw background circle
        bg_pen = QtGui.QPen(QtGui.QColor('#D1D5DA'), self._pen_width)
        painter.setPen(bg_pen)
        painter.drawEllipse(rect)

        # Draw progress arc
        fg_pen = QtGui.QPen(QtGui.QColor('#4A90E2'), self._pen_width)
        painter.setPen(fg_pen)
        painter.drawArc(rect, start_angle, span_angle)

        # Draw text
        painter.setFont(self._font)
        painter.setPen(QtGui.QColor('#333333'))
        text = f"{int(self._value/self._max*100)}%"
        fm = painter.fontMetrics()
        text_w = fm.horizontalAdvance(text)
        text_h = fm.height()
        painter.drawText(
            (width - text_w)//2,
            (height + text_h//2)//2,
            text
        )