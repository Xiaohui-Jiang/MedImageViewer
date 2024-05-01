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

    1. Utilize the `extract_image_features` function to compute a feature vector for each image in the `slices` folder. Features include RGB mean, RGB variance, HSV mean, HSV variance, edge complexity, and homogeneity.
    2. Normalize features using Z-score.
    3. Employ the `compute_similarity` function to calculate pairwise feature vector similarity and generate a similarity matrix.
    4. Visualize the similarity matrix as a heatmap using the `plot_heatmap` function, with image names as labels.

## Dependencies

Ensure the following dependencies are installed:

- NumPy
- OpenCV
- Matplotlib

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


## Contact Information

- Xiaohui Jiang (x.jiang@duke.edu)
- Tong Cheng (tong.cheng@duke.edu)

For any questions, feedback, or collaboration opportunities, please don't hesitate to reach out to us.

