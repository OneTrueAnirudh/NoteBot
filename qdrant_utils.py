#VERSION 1
# import qdrant_client
# from qdrant_client.http.models import PointStruct

# # Function to initialize Qdrant Cloud client
# def initialize_qdrant_client_cloud():
#     # Replace with your Qdrant Cloud URL and API key
#     qdrant_url = "https://f6967bda-4988-41b6-a761-42d86404b1b8.us-east4-0.gcp.cloud.qdrant.io:6333"
#     api_key = "XcBdfP3OyhoIwT4TnJdgbVqOAA7BO4XS7y4XnGj_sjNRJxBRTiRk1w"

#     # Initialize the client with cloud URL and API key
#     client = qdrant_client.QdrantClient(
#         url=qdrant_url,
#         api_key=api_key
#     )
#     return client

# # Function to upload points (vectors) to Qdrant Cloud
# def upload_vectors_to_qdrant_cloud(client, collection_name, points):
#     # Create a collection if it doesn't exist
#     client.recreate_collection(
#         collection_name=collection_name,
#         vector_size=len(points[0]["vector"]),  # Vector dimension
#         distance="Cosine"  # Distance metric (can also be Euclidean or Dot)
#     )
    
#     # Insert points into the collection
#     client.upload_collection(
#         collection_name=collection_name,
#         vectors=[point["vector"] for point in points],
#         payload=[point["payload"] for point in points],
#         ids=[point["id"] for point in points]
#     )

# # Sample usage:
# if __name__ == "__main__":
#     # Initialize Qdrant Cloud client
#     client = initialize_qdrant_client_cloud()

#     # Example points (vectors and metadata)
#     example_points = [
#         {
#             "id": 1,
#             "vector": [0.1, 0.2, 0.3],
#             "payload": {"text": "This is a sample text."}
#         },
#         {
#             "id": 2,
#             "vector": [0.4, 0.5, 0.6],
#             "payload": {"text": "Another example text."}
#         }
#     ]

#     # Upload vectors to Qdrant Cloud
#     upload_vectors_to_qdrant_cloud(client, collection_name="my_collection", points=example_points)

#VERSION 2
# import qdrant_client
# from qdrant_client.http.models import PointStruct

# # Function to initialize Qdrant Cloud client
# def initialize_qdrant_client_cloud():
#     # Replace with your Qdrant Cloud URL and API key
#     qdrant_url = "https://f6967bda-4988-41b6-a761-42d86404b1b8.us-east4-0.gcp.cloud.qdrant.io:6333"
#     api_key = "yl9WyhsWkjX04gPpwTvAamXpvI409GVjh1VY7LhlVd9oB7cPshbing"

#     # Initialize the client with cloud URL and API key
#     client = qdrant_client.QdrantClient(
#         url=qdrant_url,
#         api_key=api_key
#     )
#     return client

# # Function to upload points (vectors) to Qdrant Cloud
# def upload_vectors_to_qdrant_cloud(client, collection_name, points):
#     # Check if the collection exists
#     try:
#         client.get_collection(collection_name)
#         collection_exists = True
#     except Exception:
#         collection_exists = False

#     # Create a collection if it doesn't exist
#     if not collection_exists:
#         # Define the vector configuration
#         vectors_config = {
#             "size": len(points[0]["vector"]),  # Vector dimension
#             "distance": "Cosine"  # Distance metric (can also be Euclidean or Dot)
#         }

#         client.recreate_collection(
#             collection_name=collection_name,
#             vectors_config=vectors_config
#         )
    
#     # Insert points into the collection
#     client.upload_collection(
#         collection_name=collection_name,
#         vectors=[point["vector"] for point in points],
#         payload=[point["payload"] for point in points],
#         ids=[point["id"] for point in points]
#     )

    
#     # Insert points into the collection
#     client.upload_collection(
#         collection_name=collection_name,
#         vectors=[point["vector"] for point in points],
#         payload=[point["payload"] for point in points],
#         ids=[point["id"] for point in points]
#     )


# # Function to search for vectors in Qdrant Cloud
# def search_vectors(client, collection_name, vector, limit=5):
#     results = client.search(collection_name=collection_name, vector=vector, limit=limit)
#     return results
# # Sample usage:
# if __name__ == "__main__":
#     # Initialize Qdrant Cloud client
#     client = initialize_qdrant_client_cloud()

#     # Example points (vectors and metadata)
#     example_points = [
#         {
#             "id": 1,
#             "vector": [0.1, 0.2, 0.3],
#             "payload": {"text": "This is a sample text."}
#         },
#         {
#             "id": 2,
#             "vector": [0.4, 0.5, 0.6],
#             "payload": {"text": "Another example text."}
#         }
#     ]

#     # Upload vectors to Qdrant Cloud
#     upload_vectors_to_qdrant_cloud(client, collection_name="my_collection", points=example_points)

#     # Example to search for similar vectors
#     search_vector = [0.1, 0.2, 0.3]
#     search_results = search_vectors(client, collection_name="my_collection", vector=search_vector)
#     for result in search_results:
#         print(result)


#VERSION 3
import qdrant_client
from qdrant_client.http.models import PointStruct

# Function to initialize Qdrant Cloud client
def initialize_qdrant_client_cloud():
    # Replace with your Qdrant Cloud URL and API key
    qdrant_url = "https://f6967bda-4988-41b6-a761-42d86404b1b8.us-east4-0.gcp.cloud.qdrant.io:6333"
    api_key = "yl9WyhsWkjX04gPpwTvAamXpvI409GVjh1VY7LhlVd9oB7cPshbing"

    # Initialize the client with cloud URL and API key
    client = qdrant_client.QdrantClient(
        url=qdrant_url,
        api_key=api_key
    )
    return client

# Function to check if vectors already exist
def check_existing_vectors(client, collection_name, vector_ids):
    existing_ids = []
    for vector_id in vector_ids:
        try:
            # Check if the vector ID exists in the collection
            result = client.retrieve(collection_name=collection_name, ids=[vector_id])
            if result:
                existing_ids.append(vector_id)
        except Exception:
            continue  # If retrieval fails, assume vector does not exist
    return existing_ids

# Updated function to upload or update points (vectors) to Qdrant Cloud
def upload_or_update_vectors(client, collection_name, points):
    # Check if the collection exists
    try:
        client.get_collection(collection_name)
        collection_exists = True
    except Exception:
        collection_exists = False

    # Create a collection if it doesn't exist
    if not collection_exists:
        # Define the vector configuration
        vectors_config = {
            "size": len(points[0]["vector"]),  # Vector dimension
            "distance": "Cosine"  # Distance metric (can also be Euclidean or Dot)
        }
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=vectors_config
        )

    # Check for existing vectors
    existing_ids = check_existing_vectors(client, collection_name, [point["id"] for point in points])

    new_points = []
    updated_points = []

    # Separate new and existing points
    for point in points:
        if point["id"] in existing_ids:
            updated_points.append(point)  # Vectors with the same ID exist
        else:
            new_points.append(point)  # New vectors

    # Insert new points into the collection
    if new_points:
        client.upload_collection(
            collection_name=collection_name,
            vectors=[point["vector"] for point in new_points],
            payload=[point["payload"] for point in new_points],
            ids=[point["id"] for point in new_points]
        )
        print(f"Uploaded {len(new_points)} new points.")

    # Update existing points if needed
    if updated_points:
        client.upload_collection(
            collection_name=collection_name,
            vectors=[point["vector"] for point in updated_points],
            payload=[point["payload"] for point in updated_points],
            ids=[point["id"] for point in updated_points]
        )
        print(f"Updated {len(updated_points)} existing points.")

# Function to search for vectors in Qdrant Cloud
def search_vectors(client, collection_name, vector, limit=5):
    results = client.search(
        collection_name=collection_name,
        vector=vector,
        limit=limit
    )
    return results

# Sample usage:
if __name__ == "__main__":
    # Initialize Qdrant Cloud client
    client = initialize_qdrant_client_cloud()

    # Example points (vectors and metadata)
    example_points = [
        {
            "id": 1,
            "vector": [0.1, 0.2, 0.3],
            "payload": {"text": "This is a sample text."}
        },
        {
            "id": 2,
            "vector": [0.4, 0.5, 0.6],
            "payload": {"text": "Another example text."}
        }
    ]

    # Upload or update vectors in Qdrant Cloud
    upload_or_update_vectors(client, collection_name="my_collection", points=example_points)

    # Example to search for similar vectors
    search_vector = [0.1, 0.2, 0.3]
    search_results = search_vectors(client, collection_name="my_collection", vector=search_vector)
    
    for result in search_results:
        print(result)
