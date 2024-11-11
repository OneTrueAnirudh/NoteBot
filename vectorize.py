#9/11
from sentence_transformers import SentenceTransformer
from qdrant_utils import initialize_qdrant_client_cloud, upload_or_update_vectors


def initialize_model(model_name='all-mpnet-base-v2'):
    """Initialize the Sentence Transformer model."""
    model = SentenceTransformer(model_name)
    return model


def vectorize_chunks(model, chunks):
    """Vectorize the text chunks into embeddings."""
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings


def format_embeddings_for_qdrant(embeddings, chunks):
    """Format the embeddings to match Qdrant's required structure."""
    metadata = [{"id": i, "text": chunk} for i, chunk in enumerate(chunks)]
    points = [
        {
            "id": metadata[i]["id"],
            "vector": embedding.tolist(),
            "payload": {"text": metadata[i]["text"]}
        }
        for i, embedding in enumerate(embeddings)
    ]
    return points


def process_and_upload_chunks(chunks, collection_name="my_collection"):
    """Process the chunks, generate embeddings, and upload to Qdrant."""
    # Initialize model
    model = initialize_model()

    # Vectorize the chunks
    embeddings = vectorize_chunks(model, chunks)

    # Format embeddings for Qdrant
    formatted_points = format_embeddings_for_qdrant(embeddings, chunks)

    # Initialize Qdrant Cloud client
    client = initialize_qdrant_client_cloud()

    # Upload the vectors to Qdrant Cloud
    upload_or_update_vectors(client, collection_name, formatted_points)

    return formatted_points

