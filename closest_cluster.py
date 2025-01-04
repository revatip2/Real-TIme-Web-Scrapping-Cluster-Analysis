import pandas as pd
from gensim.models.doc2vec import Doc2Vec
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import ast
from embed_cluster import *

def get_top_words_in_cluster(cluster_df):
    all_keywords = ' '.join(cluster_df['keywords']).split(', ')
    top_words = [word for word, count in Counter(all_keywords).most_common(10)]
    return top_words

def closest_find(keyword):
    file_path = 'output_data.csv'
    num_clusters =10
    df = pd.read_csv(file_path)
    vectors = get_doc2vec_vectors(df)
    clusters = cluster_messages(vectors, num_clusters)
    df['cluster'] = clusters
    df['doc2vec_vector'] = vectors
    cluster_dict = {row['id']: {'cluster': row['cluster'], 'vector': row['doc2vec_vector']} for _, row in df.iterrows()}
    model = Doc2Vec.load('model.bin') 

    inferred_vector = model.infer_vector(keyword.split(', '))

    min_distance = float('inf')
    closest_cluster = None

    for id, data in cluster_dict.items():
        cluster_vector = list(data['vector'].values())[0]  # Extracting the vector from the dictionary
        distance = np.linalg.norm(np.array(inferred_vector) - np.array(cluster_vector))
        if distance < min_distance:
            min_distance = distance
            closest_cluster = data['cluster']
            closest_cluster_df = df[df['cluster'] == closest_cluster]
            top_words = get_top_words_in_cluster(closest_cluster_df)

    return keyword, closest_cluster, top_words

