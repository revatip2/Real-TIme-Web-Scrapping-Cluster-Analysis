# Reddit Tech Keyword Clustering and Analysis

## Overview

This project involves the extraction, clustering, and analysis of Reddit tech posts based on their keywords. The core functionality includes scraping Reddit data, preprocessing it, embedding it using Doc2Vec, clustering posts based on similarity, and allowing users to search for the closest cluster for a given keyword. The project also includes periodic database updates and visualization of the clusters.

## Project Structure


## Technical Details

### Dependencies

The following Python libraries are required to run this project:

- `pandas` for data manipulation.
- `gensim` for Doc2Vec model to embed keywords.
- `sklearn` for clustering with KMeans.
- `matplotlib` for cluster visualization.
- `mysql-connector-python` for MySQL database connectivity.
- `rake-nltk` for keyword extraction.
- `nltk` for stopword handling and tokenization.
- `selenium` for web scraping Reddit data.
- `Counter` from `collections` to count keyword frequencies in clusters.

You can install the required dependencies by running:
`pip install -r requirements.txt`

### Modules

1. **`closest_cluster.py`**:
   - **Purpose**: This module finds the closest cluster to a given input keyword by calculating cosine similarity between the input keyword's Doc2Vec vector and the centroid vectors of the clusters.
   - **Main Functions**:
     - `get_top_words_in_cluster`: Extracts the most frequent words from a given cluster.
     - `closest_find`: Finds the closest cluster and top words based on an input keyword.

2. **`create_db.py`**:
   - **Purpose**: Initializes a MySQL database (`reddit_tech`) and a `posts` table to store Reddit post data, including content, username, subreddit, upvotes, comments, and keywords.
   - **Main Functions**:
     - Creates the `reddit_tech` database and the `posts` table.
     - Accepts user input for MySQL credentials.

3. **`embed_cluster.py`**:
   - **Purpose**: This module embeds the keywords of Reddit posts using the `Doc2Vec` model, clusters them using KMeans, and visualizes the clusters with the most frequent words.
   - **Main Functions**:
     - `get_doc2vec_vectors`: Embeds the keywords of posts using Doc2Vec.
     - `cluster_messages`: Performs clustering of posts based on their embeddings.
     - `visualize_clusters_with_top_words`: Visualizes the clusters and annotates them with the top words.
     - `main`: Executes the clustering and visualization, and saves the output to a CSV.

4. **`menu.py`**:
   - **Purpose**: Provides a command-line interface (CLI) for users to interact with the system, allowing them to find the closest cluster for a keyword and periodically update the database.
   - **Main Functions**:
     - `update_database_periodically`: Simulates periodic database updates.
     - `find_cluster`: Allows users to input a keyword and displays the closest cluster and top words.

5. **`preproc.py`**:
   - **Purpose**: Preprocesses Reddit posts by extracting useful information such as content, username, subreddit, URL, upvotes, comments, and keywords. It then stores this data in a MySQL database.
   - **Main Functions**:
     - `extract_data`: Extracts metadata (username, subreddit, URL, etc.) from Reddit posts.
     - `extract_keywords`: Uses RAKE to extract keywords from the content.
     - Prepares the dataset and inserts it into the `posts` table of the MySQL database.

6. **`scraper.py`**:
   - **Purpose**: Scrapes Reddit data from the "r/tech" subreddit using Selenium.
   - **Main Functions**:
     - Scrapes Reddit posts (title, content, upvotes, comments) and stores them in a CSV file (`reddit_tech_data.csv`).

### Data Flow

1. **Scraping**: The scraper (`scraper.py`) fetches data from Reddit’s "r/tech" subreddit.
2. **Preprocessing**: The preprocessor (`preproc.py`) extracts relevant information from each post (e.g., content, keywords) and stores it in the database.
3. **Embedding & Clustering**: The embedding and clustering module (`embed_cluster.py`) uses Doc2Vec to embed the keywords and KMeans for clustering. Clusters are saved and visualized.
4. **Interaction**: The `menu.py` provides an interactive interface for the user to find the closest cluster for a given keyword.
5. **Database Management**: The `create_db.py` handles MySQL database creation and structure, while `menu.py` updates the database periodically.

### Database Schema

The database `reddit_tech` contains the following table:

```sql
CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    username VARCHAR(512),
    url VARCHAR(512), 
    upvotes INT,
    comments INT,
    timestamp VARCHAR(255),
    subreddit VARCHAR(255),
    keywords VARCHAR(512)
);
```

### Example Usage

1. **Scraping Reddit Data**: Run the following command to scrape Reddit data and store it in a CSV file:

    ```bash
    python scraper.py
    ```

2. **Preprocessing Data**: After scraping, preprocess the data to extract useful features and store it in the database:

    ```bash
    python preproc.py
    ```

3. **Clustering and Visualizing**: Cluster the posts and visualize the results:

    ```bash
    python embed_cluster.py
    ```

4. **Interacting with Clusters**: Start the menu interface to find clusters:

    ```bash
    python menu.py <interval_in_minutes>
    ```

    - Choose option `1` to find the closest cluster for a keyword.
    - Choose option `2` to quit.
