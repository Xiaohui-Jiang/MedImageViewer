"""Test the GUI."""

from typing import Any

from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication

from SegmentationGUI import MainWindow


def test_draw_rectangle(qtbot: Any) -> None:
    """Test that a rectangle can be drawn correctly."""
    test_app = QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)

    window.show()
    qtbot.mousePress(window.image_label, Qt.LeftButton, pos=QPoint(50, 50))
    qtbot.mouseMove(window.image_label, pos=QPoint(100, 100))
    qtbot.mouseRelease(window.image_label, Qt.LeftButton, pos=QPoint(100, 100))

    assert len(window.image_label.rectangles) == 1
    assert window.image_label.rectangles[0][0].topLeft() == QPoint(50, 50)
    assert window.image_label.rectangles[0][0].bottomRight() == QPoint(
        100, 100
    )


def test_label_increment(qtbot: Any) -> None:
    """Test that labels are incrementing correctly."""
    test_app = QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)

    window.show()
    for i in range(1, 4):
        start_point = QPoint(10 * i, 10 * i)
        end_point = QPoint(30 * i, 30 * i)
        qtbot.mousePress(window.image_label, Qt.LeftButton, pos=start_point)
        qtbot.mouseMove(window.image_label, pos=end_point)
        qtbot.mouseRelease(window.image_label, Qt.LeftButton, pos=end_point)

    assert len(window.image_label.rectangles) == 3
    assert window.image_label.rectangles[2][1] == "item3"


def test_save_images(qtbot: Any, tmp_path: Any) -> None:
    """Test saving images."""
    test_app = QApplication([])
    window = MainWindow()
    qtbot.addWidget(window)

    window.image_label.rectangles = [
        (QRect(10, 10, 50, 50), "item1"),
        (QRect(60, 60, 100, 100), "item2"),
    ]

    window.image = QPixmap(200, 200)
    painter = QPainter(window.image)
    painter.fillRect(0, 0, 200, 200, Qt.white)
    painter.end()

    window.image_label.pixmap = lambda: window.image

    output_dir = tmp_path / "output"
    output_dir.mkdir()
    os.chdir(output_dir)

    window.save_images()

    assert (output_dir / "bbox_1.png").exists()
    assert (output_dir / "bbox_2.png").exists()
