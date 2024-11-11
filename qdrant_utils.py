#9/11 ver2
import qdrant_client
from qdrant_client.http import models
from qdrant_client.http.models import Distance, PointStruct


# Function to initialize Qdrant Cloud client
def initialize_qdrant_client_cloud():
    qdrant_url = "https://dca6df2b-77f2-4c50-83fa-02b4c5b2cbe7.us-east4-0.gcp.cloud.qdrant.io:6333"
    api_key = "HDF0hM81BZ8fbUuJJpOWISN4DCnj-ChktLE-YD5SH7MA5dMkjZp0yw"
    client = qdrant_client.QdrantClient(url=qdrant_url, api_key=api_key)
    return client


# Function to check if vectors already exist
def check_existing_vectors(client, collection_name, vector_ids):
    existing_ids = []
    for vector_id in vector_ids:
        try:
            result = client.retrieve(collection_name=collection_name, ids=[vector_id])
            if result:
                existing_ids.append(vector_id)
        except Exception:
            continue
    return existing_ids


# Function to upload or update vectors in Qdrant Cloud
def upload_or_update_vectors(client, collection_name, points):
    if not client.collection_exists(collection_name):
        vectors_config = {
            "size": len(points[0]["vector"]),
            "distance": Distance.COSINE
        }
        client.create_collection(collection_name=collection_name, vectors_config=vectors_config)

    existing_ids = check_existing_vectors(client, collection_name, [point["id"] for point in points])
    new_points = []
    updated_points = []

    for point in points:
        if point["id"] in existing_ids:
            updated_points.append(point)
        else:
            new_points.append(point)

    if new_points:
        client.upload_collection(
            collection_name=collection_name,
            vectors=[point["vector"] for point in new_points],
            payload=[point["payload"] for point in new_points],
            ids=[point["id"] for point in new_points]
        )
        print(f"Uploaded {len(new_points)} new points.")

    if updated_points:
        client.upload_collection(
            collection_name=collection_name,
            vectors=[point["vector"] for point in updated_points],
            payload=[point["payload"] for point in updated_points],
            ids=[point["id"] for point in updated_points]
        )
        print(f"Updated {len(updated_points)} existing points.")


# Function to search for vectors in Qdrant Cloud and return the most similar ones
def search_vectors(client, collection_name, query_vector, keyword, limit=3):
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit
    )

    # print(f"Search Results for Keyword: {keyword}")
    # print(f"Number of vectors returned: {num_results}")
    
    # # Iterate through search results and print the relevant metadata
    # for result in search_results:
    #     print(f"ID: {result.id}, Score: {result.score}")
    #     print(f"Metadata (Text Chunk): {result.payload['text']}")
    #     print("-" * 50)
    return search_results

def search_res_util(search_results):
    chunks = []
    for res in search_results:
        chunks.append(res.payload['text'])
    return chunks
