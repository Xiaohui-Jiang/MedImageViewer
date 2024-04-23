import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene,
                             QPushButton, QFileDialog, QGraphicsRectItem, QInputDialog, QGraphicsTextItem,
                             QListWidgetItem, QMenu, QAction, QListWidget, QHBoxLayout, QGraphicsItem, QMessageBox)
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF
import numpy as np
import logging

class CustomGraphicsRectItem(QGraphicsRectItem):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.category = None
        self.text_item = QGraphicsTextItem("", self)
        self.is_category_set = False

    def setCategory(self, category):
        self.category = category
        self.is_category_set = True

    def setLabelText(self, text):
        self.text_item.setPlainText(text)
        font = self.text_item.font()

        # Adjust the font size to fit the text within the rectangle
        while self.text_item.boundingRect().width() > self.rect().width() and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            self.text_item.setFont(font)

        # Center the text within the rectangle
        self.text_item.setPos(self.rect().center() - self.text_item.boundingRect().center())

    def highlight(self, state=True):
        if state:
            self.setBrush(QColor(255, 255, 0, 100))
        else:
            self.setBrush(QColor(0, 0, 0, 0))

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.parent.origin = self.mapToScene(event.pos())
            self.parent.temp_rect_item = CustomGraphicsRectItem()
            self.scene().addItem(self.parent.temp_rect_item)

    def mouseMoveEvent(self, event):
        if self.parent.temp_rect_item:
            end = self.mapToScene(event.pos())
            rect = QRectF(self.parent.origin, end).normalized()
            self.parent.temp_rect_item.setRect(rect)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.RightButton:
            self.parent.addRectangleCategory(self.parent.temp_rect_item)
            self.parent.temp_rect_item = None

class CategoryListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewer = parent

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            contextMenu = QMenu(self)

            changeCategoryAction = QAction('Change Category', self)
            changeCategoryAction.triggered.connect(lambda: self.viewer.changeCategory(item))
            contextMenu.addAction(changeCategoryAction)

            deleteRectangleAction = QAction('Delete Annotation', self)
            deleteRectangleAction.triggered.connect(lambda: self.viewer.deleteRectangle(item))
            contextMenu.addAction(deleteRectangleAction)

            contextMenu.exec_(event.globalPos())

class ImageViewer(QWidget):
    CATEGORY_COLORS = [
        "#FF0000", "#00FF00", "#0000FF",
        "#FFFF00", "#FF00FF", "#00FFFF"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_color_map = {}
        self.zoom_factor = 1.0
        self.initUI()
        self.current_image_name = None
        self.temp_rect_item = None
        self.resize(1000, 800)

    def initUI(self):
        mainLayout = QHBoxLayout()

        # Left 3/4 layout (for image display and buttons)
        leftLayout = QVBoxLayout()

        # Image Display
        self.view = CustomGraphicsView(self)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        leftLayout.addWidget(self.view)

        # Note
        self.noteLabel = QLabel(
            "Please select the bounding box",
            self)
        leftLayout.addWidget(self.noteLabel)

        # Load Button
        self.loadButton = QPushButton('Load Image', self)
        self.loadButton.clicked.connect(self.loadImage)
        leftLayout.addWidget(self.loadButton)

        # Load Bounding Box
        self.loadBBoxBtn = QPushButton('Load Annotations', self)
        self.loadBBoxBtn.clicked.connect(self.loadBoundingBoxes)
        leftLayout.addWidget(self.loadBBoxBtn)

        # Save Button
        self.saveButton = QPushButton('Save Annotations', self)
        self.saveButton.clicked.connect(self.saveRectangles)
        leftLayout.addWidget(self.saveButton)

        mainLayout.addLayout(leftLayout, 3)

        # Right 1/4 layout (for category list)
        rightLayout = QVBoxLayout()

        # Category Display
        self.categoryList = QListWidget()
        rightLayout.addWidget(self.categoryList)

        mainLayout.addLayout(rightLayout, 1)

        self.setLayout(mainLayout)

        self.categoryList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.categoryList.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):
        # Fetch the item at the clicked position
        item = self.categoryList.itemAt(position)
        if not item:
            return

        # Create a context menu
        menu = QMenu(self)

        # Change category action
        change_category_action = QAction('Change Category', self)
        change_category_action.triggered.connect(lambda: self.changeCategory(item))
        menu.addAction(change_category_action)

        # Delete rectangle action
        delete_rect_action = QAction('Delete Rectangle', self)
        delete_rect_action.triggered.connect(lambda: self.deleteRectangle(item))
        menu.addAction(delete_rect_action)

        # Display the menu
        menu.exec_(self.categoryList.mapToGlobal(position))

    def loadImage(self):
        # Display prompt
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
            "Please select the image path you want to process. Note: The image should be placed within the project path you choose.")
        msg.setWindowTitle("Prompt")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            # Show the file selection dialog after user confirmation
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                      "Image Files (*.png;*.jpg;*.jpeg;*.tif;*.tiff);;All Files (*)",
                                                      options=options)
            if filePath:
                pixmap = QPixmap(filePath)
                logging.info(f'Attempting to load image from {filePath}')
                self.image_item = self.scene.addPixmap(pixmap)
                self.view.setSceneRect(self.image_item.boundingRect())

                # Fit the image to the height of the view while maintaining aspect ratio
                self.view.fitInView(self.image_item, Qt.KeepAspectRatio)

                # Store current image's name without extension
                self.current_image_name = filePath.split('/')[-1].rsplit('.', 1)[0]

    def loadBoundingBoxes(self):
        # Display prompt
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Select the npy file with your annotated categories. (If exists)")
        msg.setWindowTitle("Prompt")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue != QMessageBox.Ok:
            return  # Exit the function if user clicked Cancel

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Bounding Box", "", "Numpy Files (*.npy);;All Files (*)",
                                                  options=options)

        if filePath:
            logging.info(f'Attempting to load bounding boxes from {filePath}')
            data = np.load(filePath, allow_pickle=True).item()

            rects = data.get('rects', [])
            for rect_data in rects:
                left, top, right, bottom, category = rect_data
                rect = QRectF(left, top, right - left, bottom - top)
                rect_item = CustomGraphicsRectItem(rect)
                rect_item.setFlag(QGraphicsItem.ItemIsMovable)
                rect_item.setFlag(QGraphicsItem.ItemIsSelectable)
                rect_item.setCategory(category)
                rect_item.setBrush(QBrush())  # Empty brush to make it hollow
                rect_item.setPen(QPen(self.getCategoryColor(category)))  # Set the category-specific color

                self.scene.addItem(rect_item)
            self.updateCategoryList()

    def getCategoryColor(self, category):
        if category not in self.category_color_map:
            available_colors = set(self.CATEGORY_COLORS) - set(
                [color.name() if isinstance(color, QColor) else color for color in self.category_color_map.values()])
            if available_colors:
                color = next(iter(available_colors))
            else:
                color = QColor(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)).name()
            self.category_color_map[category] = color
        return QColor(self.category_color_map[category])

    def addRectangleCategory(self, rect_item):
        items = list(self.category_color_map.keys())
        category, ok = QInputDialog.getItem(self, "Select Category", "Choose or input a category:", items, 0, True)
        if ok and category:
            color = self.getCategoryColor(category)
            rect_item.setPen(QPen(color, 5))
            rect_item.category = category
            self.updateCategoryList()
        else:
            if not rect_item.is_category_set:  # Check the flag here
                self.scene.removeItem(rect_item)  # Remove the rectangle if category not set

    def updateCategoryList(self):
        category_count = {}
        item_order = {}

        # Initialize order for each category
        for item in self.scene.items():
            if isinstance(item, CustomGraphicsRectItem) and item.category:
                category_count[item.category] = category_count.get(item.category, 0) + 1

        # Reset category counts for assigning unique order
        for category in category_count.keys():
            item_order[category] = 1

        self.categoryList.clear()

        for item in self.scene.items():
            if isinstance(item, CustomGraphicsRectItem) and item.category:
                item.setLabelText(f"{item.category}-{item_order[item.category]}")
                list_item = QListWidgetItem(f"{item.category}-{item_order[item.category]}")
                list_item.setData(Qt.UserRole, item)
                self.categoryList.addItem(list_item)

                # Increment the order for the category
                item_order[item.category] += 1

        self.categoryList.itemClicked.connect(self.highlightRectangle)

    def highlightRectangle(self, item):
        rect_item = item.data(Qt.UserRole)
        for other_item in self.scene.items():
            if isinstance(other_item, CustomGraphicsRectItem):
                other_item.highlight(False)
        rect_item.highlight(True)

    def wheelEvent(self, event):
        # Zoom
        degrees = event.angleDelta().y() / 8
        steps = degrees / 15
        self.zoom_factor += steps * 0.1

        anchorPoint = self.view.mapToScene(self.view.viewport().rect().center())
        self.view.centerOn(anchorPoint)
        scaleFactor = 1 + 0.1 * steps
        self.view.scale(scaleFactor, scaleFactor)
        newPos = self.view.mapToScene(self.view.viewport().rect().center())
        delta = newPos - anchorPoint
        self.view.translate(delta.x(), delta.y())

    def saveRectangles(self):
        rects = []
        category_info = {}

        # Collect all rectangles and their categories and calculate diameters
        for item in self.scene.items():
            if isinstance(item, CustomGraphicsRectItem) and item.category:  # Add check for category here
                rect = item.rect()
                diameter = ((rect.width() ** 2) + (rect.height() ** 2)) ** 0.5
                rects.append([rect.left(), rect.top(), rect.right(), rect.bottom(), item.category])

                if item.category not in category_info:
                    category_info[item.category] = {'count': 0, 'total_diameter': 0}

                category_info[item.category]['count'] += 1
                category_info[item.category]['total_diameter'] += diameter

        # Calculate average diameters
        avg_diameters = {}
        for category, info in category_info.items():
            avg_diameters[category] = info['total_diameter'] / info['count']

        # Save both the rectangle and the average diameters to a .npy file
        if self.current_image_name:
            save_path = f"{self.current_image_name}.npy"
            logging.info(f'Saving bounding box data to {save_path}')
            np.save(save_path, {'rects': rects, 'avg_diameters': avg_diameters})

    def changeCategory(self, item):
        rect_item = item.data(Qt.UserRole)
        items = list(self.category_color_map.keys())
        category, ok = QInputDialog.getItem(self, "Select Category", "Choose or input a new category:", items, 0, True)
        if ok and category:
            logging.info(f'Changed category for bounding box to {category}')
            color = self.getCategoryColor(category)
            rect_item.setPen(QPen(color, 2))
            rect_item.category = category
            self.updateCategoryList()

    def deleteRectangle(self, item):
        rect_item = item.data(Qt.UserRole)
        self.scene.removeItem(rect_item)
        logging.info('Removed bounding box')
        del rect_item
        self.updateCategoryList()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())
