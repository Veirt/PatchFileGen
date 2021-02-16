button_style = """
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

        """

line_style = """
        QLineEdit {
            border: none;
            background-color: rgb(49, 54, 68);
            color: rgb(255, 255, 255);
        }
        """

versionLabel_style = """
        QLabel {
            color: rgb(204, 205, 212);
        }
        """
