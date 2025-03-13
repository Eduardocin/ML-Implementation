import numpy as np


class KMeansClustering:
    """
    K-Means clustering algorithm implementation.
    The algorithm assigns each data point to the cluster
    with the nearest centroid (using Euclidean distance).
    
    The iterative process follows these steps:
    1. Initialize K centroids randomly within the data space
    2. Assign each data point to the nearest centroid
    3. Recalculate centroids as the mean of points assigned to each cluster
    4. Repeat steps 2 and 3 until convergence or maximum iterations reached
    
    """
        
    def __init__(self, num_clusters=3):
        self.num_clusters = num_clusters
        self.centroids = None
        
    @staticmethod
    def euclidean_distance(data_point, centroids):
        return np.sqrt(np.sum((data_point - centroids) ** 2, axis=1))
    
    def fit(self, data, max_iterations=200):
        self.centroids = np.random.uniform(np.min(data, axis=0), np.max(data, axis=0),
                                            size=(self.num_clusters, data.shape[1]))
        
        initial_centroids = self.centroids.copy()
        intermediate_centroids = []
        intermediate_labels = []
        
        for iteration in range(max_iterations):
            cluster_assignments = []
            
            for data_point in data:
                distances = KMeansClustering.euclidean_distance(self.centroids, data_point)
                closest_cluster = np.argmin(distances)
                cluster_assignments.append(closest_cluster)
                
            cluster_assignments = np.array(cluster_assignments)
            
            cluster_indices = []
            
            for cluster_index in range(self.num_clusters):
                cluster_indices.append(np.argwhere(cluster_assignments == cluster_index))
                
            new_centroids = []
            
            for cluster_index, indices in enumerate(cluster_indices):
                if len(indices) == 0:
                    new_centroids.append(self.centroids[cluster_index])
                else:
                    new_centroids.append(np.mean(data[indices], axis=0)[0])
            
            if iteration == 0 or iteration == 4:
                intermediate_centroids.append(self.centroids.copy())
                intermediate_labels.append(cluster_assignments.copy())
            
            if np.max(self.centroids - np.array(new_centroids)) < 0.001:
                break
            else:
                self.centroids = np.array(new_centroids)
        
        final_centroids = self.centroids.copy()
        final_labels = cluster_assignments.copy()
        
        return initial_centroids, intermediate_centroids, final_centroids, intermediate_labels, final_labels