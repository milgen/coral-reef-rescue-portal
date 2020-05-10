import numpy as np
from sklearn.cluster import KMeans
import scipy.signal


def to_grid(indices, shape):
    grid = np.zeros(shape)
    for index in range(indices.shape[0]):
        i,j = indices[index]
        grid[i, j] = 1
    return grid


def median_flter(X, grid_shape, kernel_size):
    grid = to_grid(X, grid_shape)
    filtered = scipy.signal.medfilt(grid, kernel_size=kernel_size)
    result = np.argwhere(filtered)
    return result


def kmeans(X, number_of_clusters):
    kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    return kmeans.fit_predict(X)


def get_groups(X, y_km, nc):
    groups = {}
    for c in range(nc):
        groups[c] = X[y_km == c]
    return groups

def cluster(X, grid_shape, kernel_size, number_of_clusters):
    """
    Uses kmeans clustering with the given number of centroids.

     Parameters
    ----------
    X: 2 dim array of values

    Returns
    -------
    array
        Prediction of kmeans
    """
    indices = median_flter(X, grid_shape, kernel_size)
    y_pred = kmeans(indices, number_of_clusters)
    groups = get_groups(indices, y_pred, number_of_clusters)
    return groups




