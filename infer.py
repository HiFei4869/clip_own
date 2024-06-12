from PIL import Image
from clip_interrogator import Config, Interrogator

import os
from sklearn.decomposition import PCA

import numpy as np
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings("ignore")

#device = "cuda"

ci = Interrogator(Config(clip_model_name="ViT-L-14/openai"))

# Function to load and preprocess images from a folder
def load_and_preprocess_images_from_folder(folder_path):
    image_extensions = ('.jpg', '.jpeg')
    images = []
    image_names = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(image_path).convert('RGB')
                images.append(image)
                image_names.append(filename)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

    return images, image_names

# Function to generate embeddings using CLIP
def generate_embeddings(images):
    embeddings = []
    for image in images:
        image_embedding = ci.image_to_features(image)
        embeddings.append(image_embedding.cpu().numpy())
    
    embeddings = np.concatenate(embeddings, axis=0)  # Stack all embeddings
    return embeddings

def generate_captions(images):
    captions = []
    for image in images:
        caption = ci.generate_caption(image)
        captions.append(caption.cpu().numpy())
    
    captions = np.concatencate(captions, axis=0)
    return captions

# Function to apply PCA for dimensionality reduction
def reduce_dimensions(embeddings, n_components=100):
    pca = PCA(n_components=n_components)
    reduced_embeddings = pca.fit_transform(embeddings)
    return reduced_embeddings, pca

# Folder containing images
folder_path = './drawings_big'

# Load and preprocess the images
images, image_names = load_and_preprocess_images_from_folder(folder_path)

# Generate the embeddings for the images, and captions
embeddings = generate_embeddings(images) # (122, 768)

# Reduce dimensions to make clustering more efficient
reduced_embeddings, pca = reduce_dimensions(embeddings, n_components=100)

# Apply K-Means clustering
random_seed = 42
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=random_seed)
labels = kmeans.fit_predict(reduced_embeddings)
centroids = kmeans.cluster_centers_

unique_labels = np.unique(labels)

clusters = {label: [] for label in unique_labels}

for idx, label in enumerate(labels):
    clusters[label].append(idx)

# Output the clusters with indices
for label, indices in clusters.items():
    print(f"Cluster {label} points (indices): {indices}")
    
# Find the closest sample to each cluster center for future use (caption)
distances = kmeans.transform(reduced_embeddings)  # Shape: (n_samples, n_clusters)
closest_indices = np.argmin(distances, axis=0)
print(closest_indices)
closest_samples = embeddings[closest_indices]


centroids_original = pca.inverse_transform(centroids)
print("success now!")

for indice in closest_indices:
    image = images[indice]
    image_embedding = ci.image_to_features(image)
    caption = ci.generate_caption(image)
    print(ci.embedding_to_prompt(image_embedding, caption))

# i = 0
# for image_name in image_names:
#     print(i, image_name)
#     i = i+1

# Show the memberships of each cluster
for j in closest_indices:
    print(j, image_names[j])
