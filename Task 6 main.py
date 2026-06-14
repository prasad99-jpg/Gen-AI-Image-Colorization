# ============================================================
# COLORIZATION OF HISTORICAL PHOTOGRAPHS USING USER INPUT + GUI
# ============================================================

import sys
import cv2

from models.deoldify_model import colorize_image
from models.era_classifer import predict_era
from utils.palette import apply_historical_palette

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QMessageBox
)

from PyQt5.QtGui import (
    QPixmap,
    QImage,
    QFont
)

from PyQt5.QtCore import Qt


class HistoricalGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.image_path = None
        self.final_image = None

        self.initUI()

    # -------------------------------------------------------
    # GUI DESIGN
    # -------------------------------------------------------

    def initUI(self):

        self.setWindowTitle(
            "Historical Photograph Colorization"
        )

        self.setGeometry(
            100,
            50,
            1400,
            800
        )

        self.setStyleSheet("""
        QWidget{
            background-color:#1E1E1E;
        }

        QLabel{
            color:white;
            font-size:15px;
        }

        QPushButton{
            background-color:#3498db;
            color:white;
            border-radius:15px;
            padding:12px;
            font-size:15px;
            font-weight:bold;
        }

        QPushButton:hover{
            background-color:#2980b9;
        }
        """)

        # ---------------- TITLE ----------------

        title = QLabel(
            "Historical Photograph Colorization"
        )

        title.setFont(
            QFont(
                "Arial",
                20,
                QFont.Bold
            )
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        # ---------------- IMAGE LABELS ----------------

        self.original_label = QLabel(
            "Original Image"
        )

        self.original_label.setFixedSize(
            550,
            550
        )

        self.original_label.setAlignment(
            Qt.AlignCenter
        )

        self.original_label.setStyleSheet("""
        background-color:#2C2C2C;
        border:3px solid #3498db;
        border-radius:20px;
        """)

        self.output_label = QLabel(
            "Colorized Output"
        )

        self.output_label.setFixedSize(
            550,
            550
        )

        self.output_label.setAlignment(
            Qt.AlignCenter
        )

        self.output_label.setStyleSheet("""
        background-color:#2C2C2C;
        border:3px solid #2ecc71;
        border-radius:20px;
        """)

        image_layout = QHBoxLayout()

        image_layout.addWidget(
            self.original_label
        )

        image_layout.addWidget(
            self.output_label
        )

        # ---------------- ERA LABEL ----------------

        self.era_label = QLabel(
            "Detected Era : None"
        )

        self.era_label.setAlignment(
            Qt.AlignCenter
        )

        self.era_label.setFont(
            QFont(
                "Arial",
                14,
                QFont.Bold
            )
        )

        # ---------------- BUTTONS ----------------

        self.upload_btn = QPushButton(
            "Upload Image"
        )

        self.colorize_btn = QPushButton(
            "Colorize"
        )

        self.save_btn = QPushButton(
            "Save Output"
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.upload_btn
        )

        button_layout.addWidget(
            self.colorize_btn
        )

        button_layout.addWidget(
            self.save_btn
        )

        # ---------------- MAIN LAYOUT ----------------

        layout = QVBoxLayout()

        layout.addWidget(
            title
        )

        layout.addLayout(
            image_layout
        )

        layout.addWidget(
            self.era_label
        )

        layout.addLayout(
            button_layout
        )

        self.setLayout(
            layout
        )

        # button connections

        self.upload_btn.clicked.connect(
            self.load_image
        )

        self.colorize_btn.clicked.connect(
            self.run_colorization
        )

        self.save_btn.clicked.connect(
            self.save_image
        )

    # -------------------------------------------------------
    # DISPLAY IMAGE
    # -------------------------------------------------------

    def show_image(self, image, label):

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = rgb.shape

        bytes_per_line = ch * w

        qimage = QImage(
            rgb.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(
            qimage
        )

        pixmap = pixmap.scaled(
            label.width(),
            label.height(),
            Qt.KeepAspectRatio
        )

        label.setPixmap(
            pixmap
        )

    # -------------------------------------------------------
    # LOAD IMAGE
    # -------------------------------------------------------

    def load_image(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.jpg *.png *.jpeg)"
        )

        if path:

            self.image_path = path

            image = cv2.imread(
                path
            )

            self.show_image(
                image,
                self.original_label
            )

    # -------------------------------------------------------
    # COLORIZATION
    # -------------------------------------------------------

    def run_colorization(self):

        if self.image_path is None:

            QMessageBox.warning(
                self,
                "Warning",
                "Please upload an image first."
            )

            return

        # Step 1
        colorize_image(
            self.image_path
        )

        image = cv2.imread(
            "result.png"
        )

        # Step 2
        era = predict_era(
            image
        )

        self.era_label.setText(
            "Detected Era : " + era
        )

        # Step 3
        self.final_image = apply_historical_palette(
            image,
            era
        )

        self.show_image(
            self.final_image,
            self.output_label
        )

    # -------------------------------------------------------
    # SAVE OUTPUT
    # -------------------------------------------------------

    def save_image(self):

        if self.final_image is None:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "JPEG (*.jpg)"
        )

        if filename:

            cv2.imwrite(
                filename,
                self.final_image
            )

            QMessageBox.information(
                self,
                "Success",
                "Image saved successfully."
            )


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    window = HistoricalGUI()

    window.show()

    sys.exit(
        app.exec()
    )