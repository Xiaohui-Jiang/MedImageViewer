"""GUI for annotation."""

import os
import sys
from typing import List, Optional, Tuple

from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import (
    QFont,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
)


class DrawableLabel(QLabel):
    """A QLabel that allows users to draw and label rectangles on an image."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize the DrawableLabel with default attributes."""
        super().__init__(parent)
        self.start_point: QPoint = QPoint()
        self.end_point: QPoint = QPoint()
        self.drawing: bool = False
        self.current_rectangle: Tuple[QRect, str]
        self.rectangles: List[Tuple[QRect, str]] = []

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Start drawing a rectangle on mouse press."""

        if event.button() == Qt.LeftButton:  # type: ignore # noqa
            self.drawing = True
            self.start_point = event.pos()
            self.end_point = self.start_point
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """Update the rectangle dimensions on mouse move."""
        if event.buttons() & Qt.LeftButton and self.drawing:  # type: ignore # noqa
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Finish drawing the rectangle on mouse release."""

        if event.button() == Qt.LeftButton and self.drawing:  # type: ignore # noqa
            self.drawing = False
            self.end_point = (
                event.pos()
            )  # Update end_point to current mouse position
            self.rectangles.append(
                (
                    QRect(self.start_point, self.end_point),
                    f"item{len(self.rectangles) + 1}",
                )
            )
            self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Draw the rectangles and labels on the widget."""
        super().paintEvent(event)
        painter = QPainter(self)

        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))  # type: ignore # noqa
        painter.setFont(QFont("Arial", 10))

        # Draw existing rectangles
        for rect, name in self.rectangles:
            painter.drawRect(rect)

            painter.drawText(rect, Qt.AlignCenter, name)  # type: ignore # noqa

        # Draw current rectangle being drawn
        if self.drawing:
            self.current_rectangle = (
                QRect(self.start_point, self.end_point),
                f"item{len(self.rectangles) + 1}",
            )
            painter.drawRect(self.current_rectangle[0])
            painter.drawText(
                self.current_rectangle[0],

                Qt.AlignCenter,  # type: ignore # noqa
                self.current_rectangle[1],
            )


class MainWindow(QMainWindow):
    """Main window that contains all UI components including DrawableLabel."""

    def __init__(self, test_mode: bool = False) -> None:
        """Set up the main window and initialize the UI."""
        super().__init__()
        self.test_mode = test_mode
        self.initUI()

    def initUI(self) -> None:
        """Initialize user interface components."""
        self.setWindowTitle("Image Analyzer")
        self.setGeometry(100, 100, 800, 600)
        self.image_label = DrawableLabel(self)
        self.image_label.setGeometry(10, 10, 780, 500)
        self.image_label.setScaledContents(True)
        self.load_image()

        # Add save button
        save_button = QPushButton("Save", self)
        save_button.setGeometry(10, 520, 100, 30)
        save_button.clicked.connect(self.save_images)

    def load_image(self) -> None:
        """Load an image file through a dialog and display it."""
        if not self.test_mode:
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Open Image", "", "Image files (*.jpg *.png)"
            )
            if file_name:
                self.image = QPixmap(file_name)
                self.image_label.setPixmap(self.image)
            else:
                self.close()
        else:
            # Simulate an image load
            self.image = QPixmap(800, 600)  # Specify the dimensions as needed
            self.image.fill(

                Qt.white  # type: ignore # noqa
            )  # Fill the pixmap with white or any other placeholder
            self.image_label.setPixmap(self.image)

    def save_images(self) -> None:
        """Save images of all bounding boxes."""
        directory = "tests/test_save" if self.test_mode else "slices_from_GUI"
        os.makedirs(directory, exist_ok=True)
        if self.image:
            pixmap_size = self.image_label.pixmap().size()
            for idx, (rect, _) in enumerate(self.image_label.rectangles):
                # Get coordinates of top left and bottom right points
                top_left = rect.topLeft()
                bottom_right = rect.bottomRight()
                # Convert rect coordinates to match QPixmap coordinates
                rect_translated = QRect(
                    int(
                        top_left.x()
                        * pixmap_size.width()
                        / self.image_label.width()
                    ),
                    int(
                        top_left.y()
                        * pixmap_size.height()
                        / self.image_label.height()
                    ),
                    int(
                        (bottom_right.x() - top_left.x())
                        * pixmap_size.width()
                        / self.image_label.width()
                    ),
                    int(
                        (bottom_right.y() - top_left.y())
                        * pixmap_size.height()
                        / self.image_label.height()
                    ),
                )
                cropped = self.image.copy(rect_translated)
                cropped.save(f"{directory}/bbox_{idx + 1}.png")


def main() -> None:
    """Main."""
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
