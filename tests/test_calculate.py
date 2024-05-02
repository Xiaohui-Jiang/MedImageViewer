"""Test property_calculation."""

import numpy as np
from property_calculation import (
    compute_similarity,
    extract_image_features,
    plot_heatmap,
)


# Test extract_image_features function
def test_extract_image_features() -> None:
    """Test extract feature from image."""
    folder_path = "slices_from_GUI"
    feature_dict = extract_image_features(folder_path)

    # Check if feature_dict is a dictionary
    assert isinstance(feature_dict, dict)

    # Check if feature_dict contains the expected number of keys
    assert len(feature_dict) == 7
    # Check if values in feature_dict are lists of floats
    for feature_vector in feature_dict.values():
        assert isinstance(feature_vector, list)
        assert all(isinstance(f, float) for f in feature_vector)


# Test compute_similarity function
def test_compute_similarity() -> None:
    """Test similarity calculation."""
    # Generate a random feature dictionary
    random_feature_dict = {
        "image1.jpg": [0.1, 0.2, 0.3],
        "image2.jpg": [0.4, 0.5, 0.6],
        "image3.jpg": [0.7, 0.8, 0.9],
    }

    similarity_matrix = compute_similarity(random_feature_dict)

    # Check if similarity_matrix is a numpy array
    assert isinstance(similarity_matrix, np.ndarray)

    # Check if similarity_matrix has the correct shape
    assert similarity_matrix.shape == (3, 3)

    # Check if all values in similarity_matrix are between 0 and 1
    assert np.all(similarity_matrix >= 0) and np.all(similarity_matrix <= 1)


# Test plot_heatmap function
def test_plot_heatmap() -> None:
    """Test heatmap."""
    # Generate a random similarity matrix and list of filenames
    random_similarity_matrix = np.random.rand(3, 3)
    filenames = ["image1.jpg", "image2.jpg", "image3.jpg"]

    # Call plot_heatmap without raising any errors
    plot_heatmap(random_similarity_matrix, filenames, "tests")
