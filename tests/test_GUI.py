"""test for GUI."""

import os

import pytest
from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QMouseEvent, QPixmap
from PyQt5.QtWidgets import QApplication
from SegmentationGUI import DrawableLabel, MainWindow


@pytest.fixture
def app() -> QApplication:
    """Fixture to create a QApplication object."""
    return QApplication([])


@pytest.fixture
def main_window(app: QApplication) -> MainWindow:
    """Fixture to create and return the main window in test mode."""
    return MainWindow(test_mode=True)


@pytest.fixture
def drawable_label(app: QApplication) -> DrawableLabel:
    """Fixture to create a DrawableLabel."""
    label = DrawableLabel(None)
    label.resize(800, 600)
    pixmap = QPixmap(800, 600)
    pixmap.fill(Qt.white)  # type: ignore # noqa
    label.setPixmap(pixmap)
    return label


def test_main_window_initialization(main_window: MainWindow) -> None:
    """Test if the main window initializes with correct properties."""
    assert main_window.windowTitle() == "Image Analyzer"
    assert main_window.geometry().width() == 800
    assert main_window.geometry().height() == 600
    assert main_window.test_mode is True


def test_drawing_rectangle(drawable_label: DrawableLabel) -> None:
    """Test drawing a rectangle on the DrawableLabel."""
    # Simulate mouse press
    drawable_label.mousePressEvent(
        QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            QPoint(100, 100),
            Qt.LeftButton,  # type: ignore # noqa
            Qt.LeftButton,  # type: ignore # noqa
            Qt.NoModifier,  # type: ignore # noqa
        )
    )
    # Simulate mouse move
    drawable_label.mouseMoveEvent(
        QMouseEvent(
            QMouseEvent.Type.MouseMove,
            QPoint(200, 200),

            Qt.LeftButton,  # type: ignore # noqa
            Qt.LeftButton,  # type: ignore # noqa
            Qt.NoModifier,  # type: ignore # noqa
        )
    )
    # Simulate mouse release
    drawable_label.mouseReleaseEvent(
        QMouseEvent(
            QMouseEvent.Type.MouseButtonRelease,
            QPoint(200, 200),

            Qt.LeftButton,  # type: ignore # noqa
            Qt.LeftButton,  # type: ignore # noqa
            Qt.NoModifier,  # type: ignore # noqa
        )
    )

    # Check if a rectangle is added
    assert len(drawable_label.rectangles) == 1
    assert drawable_label.rectangles[0][0].topLeft() == QPoint(100, 100)
    assert drawable_label.rectangles[0][0].bottomRight() == QPoint(200, 200)


def test_save_images(main_window: MainWindow) -> None:
    """Test saving images of bounding boxes to a test-specific directory."""
    # Set up the image and rectangles manually
    main_window.image = QPixmap(200, 200)  # Assuming a 200x200 px image
    main_window.image.fill(

        Qt.white  # type: ignore # noqa
    )  # Fill the image with white for visibility
    main_window.image_label.rectangles = [
        (QRect(10, 10, 50, 50), "item1"),
        (QRect(60, 60, 100, 100), "item2"),
    ]

    # Trigger the saving logic
    main_window.save_images()

    directory = "tests/test_save"

    # Check that files are created in the correct directory
    assert os.path.exists(os.path.join(directory, "bbox_1.png"))
    assert os.path.exists(os.path.join(directory, "bbox_2.png"))
