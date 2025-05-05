import numpy as np
from scipy.fftpack import dct, idct
from sklearn.cluster import KMeans

def compress_image(img, num_clusters, num_discard=0):
    # Apply DCT to the image (only once)
    dct_img = dct(img, norm='ortho', axis=0)  # Apply DCT along rows
    dct_img = dct(dct_img, norm='ortho', axis=1)  # Apply DCT along columns
    
    # Flatten the DCT image for clustering
    dct_flat = dct_img.reshape(-1, 1)  # Reshape to (N, 1) for K-means
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, n_init=10)
    kmeans.fit(dct_flat)

    # Get the cluster labels and centroids
    labels = kmeans.labels_  # Store cluster labels
    centroids = kmeans.cluster_centers_  # Store centroids

    # clusters after discarding
    num_clusters_after = num_clusters - num_discard

    # Discart the centroids with the lowest energy
    centroids = np.sort(centroids, axis=0)  # Sort centroids
    centroids = centroids[-num_clusters_after:]  # Keep only the top num_clusters centroids
    centroids = centroids.flatten()  # Flatten to 1D array
    # Map the labels to the corresponding centroids
    labels = np.array([np.argmin(np.abs(centroids - dct_flat[i])) for i in range(len(dct_flat))])
    labels = labels.reshape(dct_img.shape)  # Reshape back to original image shape
    
    # Return the labels, centroids, and original DCT shape
    return labels, centroids, dct_img.shape


def reconstruct_image(centroid_index, centroids, shape):
    # Reconstruct the quantized DCT coefficients
    reconstructed_dct = np.array([centroids[i] for i in centroid_index]).reshape(shape)
    
    # Apply inverse DCT (only once)
    reconstructed_img = idct(reconstructed_dct, norm='ortho', axis=0)  # Apply along rows
    reconstructed_img = idct(reconstructed_img, norm='ortho', axis=1)  # Apply along columns
    
    return reconstructed_img