"""Calculate feature vectors and similarity and plot heatmaps."""

import os
from typing import Any, Dict, List

import cv2
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def extract_image_features(folder_path: str) -> Dict[str, List[float]]:
    """Extracts features from images in a given folder.

    Args:
    folder_path (str): Path to the folder containing images.

    Returns:
    feature_dict (dict): Dictionary containing image names as keys
    and Z-score normalized feature matrices as values.
    """
    # Initialize dictionary to store feature matrices
    feature_dict = {}

    # Initialize lists to store features and filenames
    all_features = []
    filenames = []

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(
            (".jpg", ".jpeg", ".png")
        ):  # Check if file is an image
            # Store filename
            filenames.append(filename)

            # Read the image
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is None:
                continue  # Skip if image cannot be read

            # Convert image to RGB and HSV
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            # Calculate mean and variance of RGB
            rgb_mean = np.mean(image_rgb, axis=(0, 1))
            rgb_var = np.var(image_rgb, axis=(0, 1))

            # Calculate mean and variance of HSV
            hsv_mean = np.mean(image_hsv, axis=(0, 1))
            hsv_var = np.var(image_hsv, axis=(0, 1))

            # Calculate edge complexity using Canny edge detection
            edges = cv2.Canny(image, 100, 200)
            edge_complexity = np.mean(edges)

            # Calculate homogeneity using grayscale image
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ddepth = cv2.CV_64F  # type: ignore
            homogeneity = cv2.Laplacian(gray_image, ddepth).var()

            feature_vector = np.concatenate(
                [
                    rgb_mean,
                    rgb_var,
                    hsv_mean,
                    hsv_var,
                    [edge_complexity],
                    [homogeneity],
                ]
            )
            all_features.append(feature_vector)

    # Convert features to a numpy array for easier manipulation
    all_features_array = np.array(all_features)

    # Z-score normalization
    mean = np.mean(all_features_array, axis=0)
    std = np.std(all_features_array, axis=0)
    z_score_features = (all_features_array - mean) / std

    # Populate feature dictionary with normalized feature matrices
    for i, filename in enumerate(filenames):
        feature_dict[filename] = list(z_score_features[i])

    return feature_dict


def compute_similarity(feature_dict: Dict[str, List[float]]) -> Any:
    """Compute cosine similarity between feature vectors.

    Args:
    feature_dict (dict): Dictionary containing image names as keys
    and Z-score normalized feature vectors as values.

    Returns:
    similarity_matrix (ndarray): Matrix containing cosine similarity values.
    """
    # Extract feature vectors
    feature_vectors = np.array(list(feature_dict.values()))

    # Compute cosine similarity
    similarity_matrix = np.dot(feature_vectors, feature_vectors.T)
    norm = np.linalg.norm(feature_vectors, axis=1)
    similarity_matrix /= norm[:, np.newaxis]
    similarity_matrix /= norm[np.newaxis, :]

    return similarity_matrix


def plot_heatmap(similarity_matrix: np.ndarray, filenames: List[str]) -> None:
    """Plot heatmap of cosine similarity.

    Args:
    similarity_matrix (ndarray): Matrix containing cosine similarity values.
    filenames (list): List of image filenames.
    """
    sns.set_theme()
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        similarity_matrix,
        annot=False,
        xticklabels=filenames,
        yticklabels=filenames,
        cmap="YlGnBu",
    )
    plt.title("Cosine Similarity Heatmap")
    plt.xlabel("Images")
    plt.ylabel("Images")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.savefig("similarity_heatmap.png")


if __name__ == "__main__":
    folder_path = "slices_from_GUI"
    feature_dict = extract_image_features(folder_path)
    similarity_matrix = compute_similarity(feature_dict)
    plot_heatmap(similarity_matrix, list(feature_dict.keys()))
