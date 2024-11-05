# #importing functions
# from GUI import browse_files
# from chunking import PDF_parser_chunker
# from vectorize import process_chunks
# from slide_keywords import read_pptx, llm_keywords, get_keyword_vectors

# #upload textbook excerpt and slides
# textbook, slides = browse_files()
# print("Textbook Path:", textbook)
# print("Slides Path:", slides)

# # Calling the function to chunk the textbook, chunks are stored as strings in the list
# chunks = PDF_parser_chunker(textbook).Chunker()

# #get vector embeddings for chunks
# formatted_embeddings=process_chunks(chunks)
# for point in formatted_embeddings:
#     print(f"ID: {point['id']}")
#     print(f"Vector: {point['vector']}")
#     print(f"Metadata (Text Chunk): {point['payload']['text']}")
#     print("-" * 50)

# #get vectorized keywords from uploaded slides
# slide_text = read_pptx(slides) 
# keywords = llm_keywords(slide_text)
# print(keywords)
# keyword_vectors = get_keyword_vectors(keywords)
# print(len(keyword_vectors))

#importing functions
from GUI import browse_files
from chunking import PDF_parser_chunker
from vectorize import process_and_upload_chunks
from slide_keywords import read_pptx, llm_keywords, get_keyword_vectors
from qdrant_utils import upload_or_update_vectors


# Upload textbook excerpt and slides
textbook, slides = browse_files()
print("Textbook Path:", textbook)
print("Slides Path:", slides)

# Calling the function to chunk the textbook, chunks are stored as strings in the list
chunks = PDF_parser_chunker(textbook).Chunker()

# Get vector embeddings for chunks and upload to Qdrant Cloud
collection_name = "NoteBot"  # You can specify your collection name here
formatted_embeddings = process_and_upload_chunks(chunks, collection_name)

# # Print uploaded vectors
# for point in formatted_embeddings:
#     print(f"ID: {point['id']}")
#     print(f"Vector: {point['vector']}")
#     print(f"Metadata (Text Chunk): {point['payload']['text']}")
#     print("-" * 50)

for point in formatted_embeddings:
    print(f"ID: {point['id']}")
    print(f"Vector: {point['vector']}")
    # Encode the payload text to handle special characters
    print(f"Metadata (Text Chunk): {point['payload']['text'].encode('utf-8', 'replace').decode('utf-8')}")
    print("-" * 50)


# Get vectorized keywords from uploaded slides
slide_text = read_pptx(slides)
keywords = llm_keywords(slide_text)
print("Keywords Extracted:", keywords)

# Get vector embeddings for the extracted keywords
keyword_vectors = get_keyword_vectors(keywords)
print(f"Number of Keyword Vectors: {len(keyword_vectors)}")

import sys
sys.stdout.reconfigure(encoding='utf-8')

