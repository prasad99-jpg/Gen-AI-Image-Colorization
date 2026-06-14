# ============================================================
# TIME-BASED HISTORICAL IMAGE COLORIZATION USING USER INPUT + GUI
# ============================================================

import sys
import cv2

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QMessageBox
)

from PyQt5.QtGui import (
    QPixmap,
    QImage
)

from PyQt5.QtCore import Qt

from palette import apply_palette
from era_classifier import detect_era


class HistoricalColorizationGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Time-Based Historical Image Colorization"
        )

        self.setGeometry(
            150,
            50,
            1400,
            850
        )

        self.image = None
        self.output_image = None

        # =================================================
        # DARK THEME
        # =================================================

        self.setStyleSheet("""

            QWidget{
                background-color:#1E1E2F;
                color:white;
                font-size:15px;
            }

            QPushButton{
                background-color:#0078D7;
                color:white;
                border-radius:15px;
                padding:12px;
                font-size:15px;
                font-weight:bold;
            }

            QPushButton:hover{
                background-color:#00A2FF;
            }

            QComboBox{
                background:white;
                color:black;
                border-radius:10px;
                padding:8px;
                font-size:14px;
            }

        """)

        # =================================================
        # TITLE
        # =================================================

        self.title = QLabel(
            "Time-Based Historical Image Colorization"
        )

        self.title.setAlignment(Qt.AlignCenter)

        self.title.setStyleSheet("""
            font-size:30px;
            color:#00D9FF;
            font-weight:bold;
            padding:15px;
        """)

        # =================================================
        # IMAGE LABELS
        # =================================================

        self.original_label = QLabel(
            "Original Image"
        )

        self.result_label = QLabel(
            "Colorized Output"
        )

        self.original_label.setAlignment(
            Qt.AlignCenter
        )

        self.result_label.setAlignment(
            Qt.AlignCenter
        )

        self.original_label.setFixedSize(
            550,
            500
        )

        self.result_label.setFixedSize(
            550,
            500
        )

        self.original_label.setStyleSheet("""
            background:white;
            color:black;
            border:3px solid #00D9FF;
            border-radius:20px;
        """)

        self.result_label.setStyleSheet("""
            background:white;
            color:black;
            border:3px solid #00FF80;
            border-radius:20px;
        """)

        # =================================================
        # ERA SELECTION
        # =================================================

        self.era_box = QComboBox()

        self.era_box.addItems([
            "Auto",
            "1900s",
            "1920s",
            "WWII",
            "1950s"
        ])

        self.era_box.setFixedHeight(45)

        # =================================================
        # BUTTONS
        # =================================================

        self.upload_btn = QPushButton(
            "Upload Image"
        )

        self.colorize_btn = QPushButton(
            "Colorize"
        )

        self.save_btn = QPushButton(
            "Save Output"
        )

        self.upload_btn.setStyleSheet("""
            QPushButton{
                background:#3A86FF;
                border-radius:15px;
                padding:12px;
                font-size:15px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#5AA3FF;
            }
        """)

        self.colorize_btn.setStyleSheet("""
            QPushButton{
                background:#06D6A0;
                border-radius:15px;
                padding:12px;
                font-size:15px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#20F0B8;
            }
        """)

        self.save_btn.setStyleSheet("""
            QPushButton{
                background:#FF006E;
                border-radius:15px;
                padding:12px;
                font-size:15px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#FF3D93;
            }
        """)

        # =================================================
        # STATUS LABEL
        # =================================================

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setStyleSheet("""
            color:#FFD166;
            font-size:16px;
            padding:10px;
        """)

        # =================================================
        # CONNECTIONS
        # =================================================

        self.upload_btn.clicked.connect(
            self.load_image
        )

        self.colorize_btn.clicked.connect(
            self.colorize
        )

        self.save_btn.clicked.connect(
            self.save_image
        )

        # =================================================
        # LAYOUTS
        # =================================================

        image_layout = QHBoxLayout()

        image_layout.addWidget(
            self.original_label
        )

        image_layout.addWidget(
            self.result_label
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.era_box
        )

        button_layout.addWidget(
            self.upload_btn
        )

        button_layout.addWidget(
            self.colorize_btn
        )

        button_layout.addWidget(
            self.save_btn
        )

        main_layout = QVBoxLayout()

        main_layout.addWidget(
            self.title
        )

        main_layout.addLayout(
            image_layout
        )

        main_layout.addSpacing(
            20
        )

        main_layout.addLayout(
            button_layout
        )

        main_layout.addWidget(
            self.status_label
        )

        self.setLayout(
            main_layout
        )

    # =====================================================
    # LOAD IMAGE
    # =====================================================

    def load_image(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.jpg *.png *.jpeg)"
        )

        if file_path:

            self.image = cv2.imread(
                file_path
            )

            self.show_image(
                self.image,
                self.original_label
            )

            self.status_label.setText(
                "Image Loaded Successfully"
            )

    # =====================================================
    # COLORIZE
    # =====================================================

    def colorize(self):

        if self.image is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Please upload an image first."
            )

            return

        era = self.era_box.currentText()

        if era == "Auto":

            era = detect_era(
                self.image
            )

        self.output_image = apply_palette(
            self.image,
            era
        )

        self.show_image(
            self.output_image,
            self.result_label
        )

        self.status_label.setText(
            f"Detected Era : {era}"
        )

    # =====================================================
    # SAVE OUTPUT
    # =====================================================

    def save_image(self):

        if self.output_image is None:

            QMessageBox.warning(
                self,
                "Warning",
                "No output image available."
            )

            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg)"
        )

        if save_path:

            cv2.imwrite(
                save_path,
                self.output_image
            )

            self.status_label.setText(
                "Output Saved Successfully"
            )

    # =====================================================
    # SHOW IMAGE
    # =====================================================

    def show_image(
        self,
        image,
        label
    ):

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = rgb.shape

        bytes_per_line = ch * w

        q_img = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(
            q_img
        )

        label.setPixmap(
            pixmap.scaled(
                label.width(),
                label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )


app = QApplication(sys.argv)

window = HistoricalColorizationGUI()

window.show()

sys.exit(app.exec_())