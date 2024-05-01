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
