import numpy as np
from sklearn.neighbors import BallTree


def group_coordinates(addresses,radius_km=5.0, max_size=6):

    EARTH_RADIUS = 6371.0088 
    coords = np.array([[a['latitude'], a['longitude']] for a in addresses])
    coords_rad = np.radians(coords)
    
    tree = BallTree(coords_rad, metric='haversine')
    radius_rad = radius_km / EARTH_RADIUS
    
    number_of_locations = len(addresses)
    unassigned_locations_indices = set(range(number_of_locations))
    clusters = []

    while unassigned_locations_indices:
        index = unassigned_locations_indices.pop()
        
        indices = tree.query_radius(coords_rad[index:index+1], r=radius_rad)[0]
        neighbors = [j for j in indices if j in unassigned_locations_indices]
        group_indices = [index] + neighbors[:max_size-1]
        
        for j in group_indices[1:]:
            unassigned_locations_indices.remove(j)
        
        clusters.append([addresses[j] for j in group_indices])

    return clusters
