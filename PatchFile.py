import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QUrl
import hashlib
import shutil
import re


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(400, 30)

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

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 300)

        self.listbox_view = ListBoxWidget(self)

        self.line = QLineEdit(self)
        self.line.move(100, 50)
        self.line.resize(200, 32)

        self.btn = QPushButton('Patch', self)
        self.btn.setGeometry(100, 100, 200, 50)
        self.btn.clicked.connect(self.makePatch)

    def getSelectedItem(self):
        item = QListWidgetItem(self.listbox_view.currentItem())
        return item.text()

    def makePatch(self):
        file_name = self.getSelectedItem()
        versionInput = self.line.text()
        path = f"00000{versionInput}"
        try:
            os.mkdir(path)
        except OSError:
            pass

        with open("PatchInfoServer.cfg", "w") as versionCfg:
            versionCfg.write(f"Version {versionInput}")

        # Make Patch.txt file
        with open(file_name, "rb") as pak:
            findregex = re.findall(rb"(resource.*?|mapdata.*?)\x00\B", pak.read())
            decoded = [byte_out.decode("utf-8") for byte_out in findregex]
            output_decoded = map(lambda decoded: f"D {decoded}", decoded)
            output_txt = "\n".join(list(output_decoded))

        with open(f"00000{versionInput}/Patch00000{versionInput}.txt", "w") as patchTxt:
            patchTxt.write(output_txt)

        # Make Patch.md5
        with open(f"00000{versionInput}/Patch00000{versionInput}.pak.md5", "w") as patchMD5:
            patchMD5.write(f"{hashlib.md5(open(file_name, 'rb').read()).hexdigest()}\n")

        try:
            shutil.copy2(file_name, f"00000{versionInput}/Patch00000{versionInput}.pak")
        except shutil.SameFileError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())
