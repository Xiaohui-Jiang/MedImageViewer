"""Test code"""
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRectF
from SegmentationGUI import ImageViewer, CustomGraphicsRectItem

def test_load_image(qtbot, monkeypatch):
    test_app = QApplication(sys.argv)
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    # Mocking user input for file dialog
    monkeypatch.setattr('PyQt5.QtWidgets.QFileDialog.getOpenFileName', lambda *args: ('test_image.png', ''))
    
    viewer.loadImage()
    assert viewer.current_image_name == 'test_image'
    assert not viewer.scene.items() == []
    
    test_app.quit()

def test_add_rectangle_category(qtbot, monkeypatch):
    test_app = QApplication(sys.argv)
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    rect_item = CustomGraphicsRectItem(QRectF(0, 0, 100, 100))
    viewer.scene.addItem(rect_item)
    
    # Mocking user input for category dialog
    monkeypatch.setattr('PyQt5.QtWidgets.QInputDialog.getItem', lambda *args: ('test_category', True))
    
    viewer.addRectangleCategory(rect_item)
    assert rect_item.category == 'test_category'
    assert viewer.categoryList.count() == 1
    
    test_app.quit()

def test_change_category(qtbot, monkeypatch):
    test_app = QApplication(sys.argv)
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    rect_item = CustomGraphicsRectItem(QRectF(0, 0, 100, 100))
    rect_item.category = 'old_category'
    viewer.scene.addItem(rect_item)
    
    list_item = viewer.categoryList.item(0)
    
    # Mocking user input for category dialog
    monkeypatch.setattr('PyQt5.QtWidgets.QInputDialog.getItem', lambda *args: ('new_category', True))
    
    viewer.changeCategory(list_item)
    assert rect_item.category == 'new_category'
    
    test_app.quit()

def test_delete_rectangle(qtbot):
    test_app = QApplication(sys.argv)
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    rect_item = CustomGraphicsRectItem(QRectF(0, 0, 100, 100))
    viewer.scene.addItem(rect_item)
    
    list_item = viewer.categoryList.item(0)
    viewer.deleteRectangle(list_item)
    assert rect_item not in viewer.scene.items()
    assert viewer.categoryList.count() == 0
    
    test_app.quit()

def test_save_rectangles(qtbot, tmpdir):
    test_app = QApplication(sys.argv)
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    rect_item1 = CustomGraphicsRectItem(QRectF(0, 0, 100, 100))
    rect_item1.category = 'category1'
    viewer.scene.addItem(rect_item1)
    
    rect_item2 = CustomGraphicsRectItem(QRectF(200, 200, 50, 50))
    rect_item2.category = 'category2'
    viewer.scene.addItem(rect_item2)
    
    viewer.current_image_name = 'test_image'
    
    # Changing the save path to a temporary directory
    viewer.save_path = str(tmpdir.join('test_image.npy'))
    viewer.saveRectangles()
    
    assert os.path.exists(viewer.save_path)
    
    test_app.quit()