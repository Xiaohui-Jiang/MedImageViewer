# MedImageViewer

## Overview

The MedImageViewer project comprises two essential components: `segmentationGUI.py` and `property_calculation.py`.

### Functionality 1: Segmentation GUI (`segmentationGUI.py`)

- **Description**: This script provides a graphical user interface (GUI) for image segmentation.
- **Usage**:
    1. Run the script.
    2. A window will automatically appear, prompting image selection. You can use the provided `sample_image.png`.
    3. Use the left mouse button to draw bounding boxes on the image.
    4. Click "save" to store segments into the `slices_from_GUI` folder.
    5. Close the window.

### Functionality 2: Property Calculation (`property_calculation.py`)

- **Description**: This script computes properties of segmented images.
- **Usage**:
    ```python
    from property_calculation import extract_image_features, compute_similarity, plot_heatmap
    
    folder_path = "slices_from_GUI"
    feature_dict = extract_image_features(folder_path)
    similarity_matrix = compute_similarity(feature_dict)
    plot_heatmap(similarity_matrix, list(feature_dict.keys()))
    ```

    1. Utilize the `extract_image_features` function to compute a feature vector for each image in the `slices` folder. Features include RGB mean, RGB variance, HSV mean, HSV variance, edge complexity, and homogeneity. Normalize features using Z-score.
    2. Employ the `compute_similarity` function to calculate pairwise feature vector similarity and generate a similarity matrix.
    3. Save the similarity matrix as a heatmap using the `plot_heatmap` function. A sample image is similarity_heatmap.png in this repository.

## Dependencies

Ensure the following dependencies are installed:

- numPy
- openCV-python
- matplotlib
- seaborn

## Installation

Clone the repository:

```bash
git clone https://github.com/Xiaohui-Jiang/MedImageViewer.git
```

## Usage

1. Navigate to the project directory.
2. Follow the usage instructions provided above for each functionality.

## Example

Below is an example of how to use both functionalities:

```python
"""Example Usage."""

from property_calculation import (
    compute_similarity,
    extract_image_features,
    plot_heatmap,
)
from segmentationGUI import main as segmentation_main

# Functionality 1: Segmentation GUI
segmentation_main()

# Functionality 2: Property Calculation
folder_path = "slices_from_GUI"
feature_dict = extract_image_features(folder_path)
similarity_matrix = compute_similarity(feature_dict)
plot_heatmap(similarity_matrix, list(feature_dict.keys()))
```

### Tests

The MedImageViewer project includes a comprehensive suite of tests to ensure both components operate as expected. We utilize pytest for our testing framework. Below are the specific functionalities tested in `test_GUI.py` and `test_calculate.py`:

#### `test_GUI.py` - GUI Functionality Tests
- **Purpose**: Ensure that the graphical user interface is robust and functions as intended.
- **Test Functions**:
    1. **GUI Launch**: Tests that the GUI application launches without any errors.
    2. **Image Loading**: Checks that the GUI can successfully load an image.
    3. **Annotation Functionality**: Verifies that the user can draw and modify bounding boxes on the image using the mouse.
    4. **Save Functionality**: Confirms that the annotated images are correctly saved to the designated folder.

#### `test_calculate.py` - Calculation Functionality Tests
- **Purpose**: Validate the accuracy and functionality of the image property calculations and similarity assessments.
- **Test Functions**:
    1. **Image Loading**: Ensures that the script can load images from a specified directory.
    2. **Feature Calculation**: Tests the computation of feature vectors for each image, checking for correct calculations of RGB and HSV means and variances, edge complexity, and homogeneity.
    3. **Similarity Calculation**: Verifies that the similarity matrix is accurately computed based on the feature vectors.
    4. **Heatmap Generation**: Tests the ability to generate and save a heatmap visualization of the similarity matrix, ensuring it correctly labels and represents the data.

Run:

```terminal
pytest.py
```

These tests cover the core functionalities of the MedImageViewer project, ensuring that each component not only works in isolation but also integrates smoothly in practical scenarios.

## Other notes

We try our best to meet the requirements of mypy for our project, but we found that some features in PyQt5, which exist, are considered non-existent by mypy. After researching online, it appears that mypy does not correctly handle some features in PyQt5. For these cases, we used # type: ignore # noqa to prevent errors. Additionally, we encountered issues with importing matplotlib and seaborn, receiving messages like 'module is installed, but missing library stubs or py.typed marker', even though there are no problems with their installation and usage.

The tests can pass smoothly locally, but for incorporating into github workflow, it seems that the GUI cannot be tested in the github workflow, so we delete the part of test in PR in workflow file.

## Contact Information

- Xiaohui Jiang (x.jiang@duke.edu)
- Tong Cheng (tong.cheng@duke.edu)

For any questions, feedback, or collaboration opportunities, please don't hesitate to reach out to us.

