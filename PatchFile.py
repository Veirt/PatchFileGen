import hashlib
import os
import re
import shutil
import sys
import codecs
import json
import style

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton)


class PatchGenGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgb(39, 43, 54);")
        self.setWindowTitle("PatchFileGen")
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.setFixedSize(400, 300)

        try:
            with open("./config.json", "r+") as f:
                self.patchPath = json.load(f)['path']
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("config.json not found")
            msg.setText("Please make sure config.json is in the same directory.")
            msg.exec_()
            sys.exit()

        self.versionLabel = QLabel(self)
        try:
            with open(f"{self.patchPath}/PatchInfoServer.cfg") as versionCfg:
                version_cfg_now = versionCfg.readline()
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("PatchInfoServer.cfg not found")
            msg.setText("PatchInfoServer.cfg is not found in your patch directory.")
            msg.exec_()
            sys.exit()

        self.versionLabel.setText(version_cfg_now)
        label_font = QtGui.QFont()
        label_font.setFamily("Segoe UI Black")
        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.versionLabel.setFont(label_font)
        self.versionLabel.setStyleSheet(style.versionLabel_style)

        self.line = QLineEdit(self)
        self.line.setMaxLength(3)
        self.line.move(165, 50)
        self.line.resize(70, 32)
        self.line.setAlignment(QtCore.Qt.AlignCenter)
        self.line.setFont(font)
        self.line.setStyleSheet(style.line_style)
        self.line.textChanged.connect(self.on_text_changed)

        self.btn = QPushButton('Patch', self)
        self.btn.setFont(font)
        self.btn.setStyleSheet(style.button_style)

        self.btn.setDisabled(True)
        self.btn.setGeometry(100, 100, 200, 50)
        self.btn.clicked.connect(self.make_patch)
        self.btn.setShortcut("Return")
        self.setAcceptDrops(True)
        self.pak = ""

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    self.pak = str(url.toLocalFile())
                else:
                    self.pak = str(url.toString())
            self.on_text_changed()
        else:
            event.ignore()

    def generate_md5(self, file_name, version):
        with open(f"{self.patchPath}/00000{version}/Patch00000{version}.pak.md5", "w") as patchMD5:
            with open(file_name, 'rb') as md5:
                file_md5 = hashlib.md5(md5.read()).hexdigest()
            patchMD5.write(f"{file_md5}\n")

    def generate_txt(self, file_name, version):
        with codecs.open(file_name, "rb", encoding='utf-8', errors='ignore') as pak:
            find_regex = re.findall(r'(resource.*?|mapdata.*?)\W\B', pak.read())
            output_decoded = map(lambda decoded: f"D {decoded}", list(find_regex))
            output_txt = "\n".join(list(output_decoded))

        with open(f"{self.patchPath}/00000{version}/Patch00000{version}.txt", "w") as patchTxt:
            patchTxt.write(output_txt)

    def make_patch(self):
        file_name = self.pak
        try:
            version_input = "{version:03d}".format(version=int(self.line.text()))
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Invalid value")
            msg.setText("Please input a valid version")
            msg.exec_()
            sys.exit()

        path = f"{self.patchPath}/00000{version_input}"
        try:
            os.mkdir(path)
        except OSError:
            pass

        with open(f"{self.patchPath}/PatchInfoServer.cfg", "w") as versionCfg:
            versionCfg.write(f"Version {version_input}")

        self.generate_md5(file_name, version_input)
        self.generate_txt(file_name, version_input)

        try:
            shutil.copy2(file_name, f"{self.patchPath}/00000{version_input}/Patch00000{version_input}.pak")
        except shutil.SameFileError:
            pass
        sys.exit()

    @QtCore.pyqtSlot()
    def on_text_changed(self):
        self.btn.setEnabled(bool(self.line.text()) and bool(self.pak != ""))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    MainGUI = PatchGenGUI()
    MainGUI.show()

    sys.exit(app.exec_())
