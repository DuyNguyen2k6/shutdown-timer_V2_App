import sys
import os
import ctypes
import time
from datetime import datetime, timedelta
import winsound
from PyQt5 import QtCore, QtWidgets, QtGui

# Helper to locate resources when bundled with PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base_path, relative_path)

class ShutdownTimer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shutdown Timer")
        # Load and set window icon (for when running .py)
        icon_path = resource_path('app_icon.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))
        self.setFixedSize(320, 340)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.setStyleSheet(self._load_styles())

        self.remaining = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._timer_tick)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        # Optional: display logo inside UI
        logo_path = resource_path('app_icon.png')
        if os.path.exists(logo_path):
            logo_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
            pixmap = QtGui.QPixmap(logo_path).scaled(64,64, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            layout.addWidget(logo_label)

        # Mode selection
        self.radio_after = QtWidgets.QRadioButton("Hẹn sau (phút)")
        self.radio_at = QtWidgets.QRadioButton("Chọn giờ cụ thể")
        self.radio_after.setChecked(True)
        mode_box = QtWidgets.QHBoxLayout()
        mode_box.addWidget(self.radio_after)
        mode_box.addWidget(self.radio_at)
        layout.addLayout(mode_box)

        # After-minutes dropdown
        self.combo_after = QtWidgets.QComboBox()
        self.combo_after.setEditable(True)
        minutes = [str(i) for i in range(1, 1441)]
        self.combo_after.addItems(minutes)
        self.combo_after.setCurrentText("1")
        layout.addWidget(self.combo_after)

        # Specific time dropdowns
        time_box = QtWidgets.QHBoxLayout()
        self.combo_hour = QtWidgets.QComboBox()
        self.combo_hour.addItems([f"{i:02d}" for i in range(24)])
        self.combo_min = QtWidgets.QComboBox()
        self.combo_min.addItems([f"{i:02d}" for i in range(60)])
        time_box.addWidget(self.combo_hour)
        time_box.addWidget(self.combo_min)
        layout.addLayout(time_box)

        # Action selection
        self.combo_action = QtWidgets.QComboBox()
        self.combo_action.addItems(["Tắt máy","Khởi động lại","Ngủ"])
        layout.addWidget(self.combo_action)

        # Buttons
        btn_box = QtWidgets.QHBoxLayout()
        self.btn_start = QtWidgets.QPushButton("Bắt đầu")
        self.btn_cancel = QtWidgets.QPushButton("Huỷ hẹn giờ")
        btn_box.addWidget(self.btn_start)
        btn_box.addWidget(self.btn_cancel)
        layout.addLayout(btn_box)

        # Countdown display
        self.time_display = QtWidgets.QLabel("00:00:00", alignment=QtCore.Qt.AlignCenter)
        self.time_display.setObjectName("timer")
        layout.addWidget(self.time_display)

        # Status label
        self.status_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Connect signals
        self.radio_after.toggled.connect(self._update_mode)
        self.btn_start.clicked.connect(self._on_start)
        self.btn_cancel.clicked.connect(self._on_cancel)
        self._update_mode()

    def _load_styles(self):
        return '''
        QWidget { background: #fff; font-family: 'San Francisco','Helvetica Neue',Arial; }
        QRadioButton { font-size: 16px; }
        QComboBox { font-size:18px; border:1px solid #ddd; border-radius:8px; padding:4px; }
        QPushButton { background:#0a84ff; color:#fff; border:none; border-radius:12px; font-size:18px; padding:8px; }
        QPushButton:pressed { background:#0060df; }
        #timer { font-size:48px; color:#333; }
        '''

    def _play_click(self):
        wav = resource_path('click_soft.wav')
        winsound.PlaySound(wav, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)

    def _update_mode(self):
        is_after = self.radio_after.isChecked()
        self.combo_after.setVisible(is_after)
        self.combo_hour.setVisible(not is_after)
        self.combo_min.setVisible(not is_after)
        self.btn_start.setText("Bắt đầu" if is_after else "Hẹn giờ")

    def _on_start(self):
        self._play_click()
        if self.radio_after.isChecked():
            mins_text = self.combo_after.currentText()
            try:
                mins = int(mins_text)
            except ValueError:
                mins = 1
            self.remaining = mins * 60
            self.status_label.setText(f"Đếm ngược {mins} phút...")
        else:
            now = datetime.now()
            h = int(self.combo_hour.currentText())
            m = int(self.combo_min.currentText())
            target = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if target < now:
                target += timedelta(days=1)
            self.remaining = int((target - now).total_seconds())
            self.status_label.setText(f"Hẹn đến {target.strftime('%H:%M')} (còn {self.remaining//60} phút)")
        self.btn_start.setEnabled(False)
        self.update_display(self.remaining)
        self.timer.start(1000)

    def _timer_tick(self):
        self.remaining -= 1
        if self.remaining < 0:
            self.timer.stop()
            self._do_shutdown()
        else:
            self.update_display(self.remaining)

    def update_display(self, sec):
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        self.time_display.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def _do_shutdown(self):
        self.status_label.setText("Đang thực hiện...")
        action = self.combo_action.currentText()
        if action == "Tắt máy":
            os.system("shutdown /s /t 0")
        elif action == "Khởi động lại":
            os.system("shutdown /r /t 0")
        else:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        self.btn_start.setEnabled(True)

    def _on_cancel(self):
        self._play_click()
        if self.timer.isActive():
            self.timer.stop()
        try:
            ctypes.windll.kernel32.AbortSystemShutdownW(None)
        except Exception:
            pass
        self.status_label.setText("Đã huỷ hẹn giờ.")
        self.btn_start.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ShutdownTimer()
    win.show()
    sys.exit(app.exec_())

# Packaging instructions:
# 1. Convert your PNG/JPG icon to .ico format (e.g., using online tools).
# 2. Place app_icon.ico and click_soft.wav in the project directory.
# 3. Run PyInstaller:
#    pyinstaller --onefile --windowed --icon "app_icon.ico" \
#               --add-data "click_soft.wav;." \
#               --add-data "app_icon.ico;." \
#               shutdown_timer.py
