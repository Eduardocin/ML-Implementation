import numpy as np

# Define a class for K-means clustering
class KMeansClustering:
    
    def __init__(self, num_clusters=3):
        # Initialize the number of clusters (k) and centroids
        self.num_clusters = num_clusters
        self.centroids = None
        
    # Calculate the Euclidean distance between data points and centroids
    @staticmethod
    def euclidean_distance(data_point, centroids):
        return np.sqrt(np.sum((data_point - centroids) ** 2, axis=1))
    
    # Method to fit the model to the data
    def fit(self, data, max_iterations=200):
        # Initialize centroids randomly within the range of the data
        self.centroids = np.random.uniform(np.min(data, axis=0), np.max(data, axis=0),
                                            size=(self.num_clusters, data.shape[1]))
        
        # Save initial centroids for visualization
        initial_centroids = self.centroids.copy()
        intermediate_centroids = []
        intermediate_labels = []
        
        for iteration in range(max_iterations):
            cluster_assignments = []
            
            # Assign each data point to the nearest centroid
            for data_point in data:
                distances = KMeansClustering.euclidean_distance(self.centroids, data_point)
                closest_cluster = np.argmin(distances)
                cluster_assignments.append(closest_cluster)
                
            cluster_assignments = np.array(cluster_assignments)
            
            cluster_indices = []
            
            # Group data points by their assigned cluster
            for cluster_index in range(self.num_clusters):
                cluster_indices.append(np.argwhere(cluster_assignments == cluster_index))
                
            new_centroids = []
            
            # Recalculate the centroids of each cluster
            for cluster_index, indices in enumerate(cluster_indices):
                if len(indices) == 0:
                    new_centroids.append(self.centroids[cluster_index])
                else:
                    new_centroids.append(np.mean(data[indices], axis=0)[0])
            
            # Save intermediate centroids and labels for visualization
            if iteration == 0 or iteration == 4:
                intermediate_centroids.append(self.centroids.copy())
                intermediate_labels.append(cluster_assignments.copy())
            
            # Check for convergence (if centroids do not change significantly)
            if np.max(self.centroids - np.array(new_centroids)) < 0.001:
                break
            else:
                self.centroids = np.array(new_centroids)
        
        # Save final centroids and labels for visualization
        final_centroids = self.centroids.copy()
        final_labels = cluster_assignments.copy()
        
        return initial_centroids, intermediate_centroids, final_centroids, intermediate_labels, final_labels