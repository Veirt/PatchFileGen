import hashlib
import os
import re
import shutil
import sys
import codecs

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton)


class PatchGenGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PatchFileGen")
        self.setWindowIcon(QtGui.QIcon("./miku.ico"))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: rgb(39, 43, 54);")

        try:
            with open("./patch_path.txt", "r+") as f:
                self.patchPath = f.readline()
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("patch_path.txt not found")
            msg.setText("Please make sure patch_path.txt is in the same directory.")
            msg.exec_()
            sys.exit()

        self.versionLabel = QLabel(self)

        try:
            with open(f"{self.patchPath}/PatchInfoServer.cfg") as versionCfg:
                versionCfgNow = versionCfg.readline()
        except FileNotFoundError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("PatchInfoServer.cfg not found")
            msg.setText("PatchInfoServer.cfg is not found in your patch directory.")
            msg.exec_()
            sys.exit()

        self.versionLabel.setText(versionCfgNow)
        labelFont = QtGui.QFont()
        labelFont.setFamily("Segoe UI Black")
        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.versionLabel.setFont(labelFont)
        self.versionLabel.setStyleSheet("""
        QLabel {
            color: rgb(204, 205, 212);
        }
        """)

        self.line = QLineEdit(self)
        self.line.setMaxLength(3)
        self.line.move(165, 50)
        self.line.resize(70, 32)
        self.line.setAlignment(QtCore.Qt.AlignCenter)
        self.line.setFont(font)
        self.line.setStyleSheet("""
        QLineEdit {
            border: none;
            background-color: rgb(49, 54, 68);
            color: rgb(255, 255, 255);
        }
        """)
        self.line.textChanged.connect(self.on_text_changed)

        self.btn = QPushButton('Patch', self)
        self.btn.setFont(font)
        self.btn.setStyleSheet("""
        QPushButton {
            color: rgb(212, 212, 212);
            border: none;
            background-color: rgb(51, 59, 72);
            text-align: center;
        }
        
        QPushButton:hover {
            color: rgb(255,255,255);
            background-color: rgb(63, 73, 89);
        }
        
        QPushButton[Active=true] {
            color: rgb(255,255,255);
            border: none;
            background-color: rgb(27, 29, 35);
            text-align: left;
            padding-left: 45px;
        }
        
        QPushButton:hover {
            color: rgb(255,255,255);
            background-color: rgb(33, 37, 43);
        }
        
        QPushButton:pressed {
            background-color: rgb(230, 126, 125);
        }
        
            """)

        self.btn.setDisabled(True)
        self.btn.setGeometry(100, 100, 200, 50)
        self.btn.clicked.connect(self.makePatch)
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

    def makePatch(self):
        file_name = self.pak
        versionInput = self.line.text()
        if len(versionInput) == 1:
            versionInput = f"00{versionInput}"
        elif len(versionInput) == 2:
            versionInput = f"0{versionInput}"
        elif len(versionInput) == 3:
            versionInput = f"{versionInput}"
        else:
            sys.exit()

        path = f"{self.patchPath}/00000{versionInput}"
        try:
            os.mkdir(path)
        except OSError:
            pass

        with open(f"{self.patchPath}/PatchInfoServer.cfg", "w") as versionCfg:
            versionCfg.write(f"Version {versionInput}")

        # Make Patch.md5
        with open(f"{self.patchPath}/00000{versionInput}/Patch00000{versionInput}.pak.md5", "w") as patchMD5:
            patchMD5.write(f"{hashlib.md5(open(file_name, 'rb').read()).hexdigest()}\n")

        # Make Patch.txt file
        with codecs.open(file_name, "rb", encoding='utf-8', errors='ignore') as pak:
            findRegex = re.findall(r'(resource.*?|mapdata.*?)\W\B', pak.read())
            output_decoded = map(lambda decoded: f"D {decoded}", list(findRegex))
            output_txt = "\n".join(list(output_decoded))

        with open(f"{self.patchPath}/00000{versionInput}/Patch00000{versionInput}.txt", "w") as patchTxt:
            patchTxt.write(output_txt)

        try:
            shutil.copy2(file_name, f"{self.patchPath}/00000{versionInput}/Patch00000{versionInput}.pak")
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
