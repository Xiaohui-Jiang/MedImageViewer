# MedImageViewer

MedImageViewer is a user-friendly GUI application designed for medical image processing and analysis. It aims to provide researchers and clinicians with a comprehensive suite of tools for image augmentation, annotation, measurement, tiling, edge detection, and similarity analysis. Our goal is to facilitate the efficient analysis of medical images, enhancing both research and clinical decision-making.

## Features
- **Annotation**: Manually annotate regions of interest in medical images.
- **Measure Annotations**: Calculate area, perimeter, and other metrics for annotated regions.
- **Find Similar Areas**: Identify and mark areas within or across images that share similar characteristics.

## Installation and Usage
### Prerequisites
- Python 3.x
- PyQt5
- OpenCV
- NumPy

### Installation
1. Clone the repository: git clone https://github.com/your-repo/MedImageViewer.git
2. Navigate to the project directory: cd MedImageViewer
3. Install the required dependencies: pip install -r requirements.txt

### Usage
1. Run the application:
python main.py
2. Load a medical image using the "Load Image" button.
3. Use the annotation tools to annotate regions of interest.
4. Perform measurements on the annotated regions using the "Measure Annotations" feature.
5. Identify similar areas within or across images using the "Find Similar Areas" feature.

Note: The operation of the application may differ between Windows and macOS systems:

- On macOS, use two-finger drag on the trackpad to select regions.
- On macOS touchscreens, zooming in and out of the test image may be challenging.

### Software Architecture
MedImageViewer is developed in Python, utilizing PyQt5 for the GUI components and OpenCV for image processing tasks. The application follows a modular architecture, making it easy to extend with additional functionalities.

The main components of the application include:

- GUI: Handles the user interface and user interactions.
- Image Processing: Performs image processing tasks such as annotation, measurement, and similarity analysis.
- Data Management: Manages the storage and retrieval of image data and annotations.

## Contributing
We welcome contributions from the community to enhance MedImageViewer. If you would like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Ensure your code adheres to the project's coding style and conventions.
3. Write unit tests to validate your changes.
4. Submit a pull request with a clear description of your changes and their purpose.

## Contact Information

- Xiaohui Jiang (x.jiang@duke.edu)
- Tong Cheng (tong.cheng@duke.edu)

For any questions, feedback, or collaboration opportunities, please don't hesitate to reach out to us.

