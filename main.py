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

#Version 4
#importing functions
# from GUI import browse_files
# from chunking import PDF_parser_chunker
# from vectorize import process_and_upload_chunks
# from slide_keywords import read_pptx, llm_keywords, get_keyword_vectors
# from qdrant_utils import upload_or_update_vectors


# # Upload textbook excerpt and slides
# textbook, slides = browse_files()
# print("Textbook Path:", textbook)
# print("Slides Path:", slides)

# # Calling the function to chunk the textbook, chunks are stored as strings in the list
# chunks = PDF_parser_chunker(textbook).Chunker()

# # Get vector embeddings for chunks and upload to Qdrant Cloud
# collection_name = "NoteBot"  # You can specify your collection name here
# formatted_embeddings = process_and_upload_chunks(chunks, collection_name)

# # # Print uploaded vectors
# # for point in formatted_embeddings:
# #     print(f"ID: {point['id']}")
# #     print(f"Vector: {point['vector']}")
# #     print(f"Metadata (Text Chunk): {point['payload']['text']}")
# #     print("-" * 50)

# for point in formatted_embeddings:
#     print(f"ID: {point['id']}")
#     print(f"Vector: {point['vector']}")
#     # Encode the payload text to handle special characters
#     print(f"Metadata (Text Chunk): {point['payload']['text'].encode('utf-8', 'replace').decode('utf-8')}")
#     print("-" * 50)


# # Get vectorized keywords from uploaded slides
# slide_text = read_pptx(slides)
# keywords = llm_keywords(slide_text)
# print("Keywords Extracted:", keywords)

# # Get vector embeddings for the extracted keywords
# keyword_vectors = get_keyword_vectors(keywords)
# print(f"Number of Keyword Vectors: {len(keyword_vectors)}")

# import sys
# sys.stdout.reconfigure(encoding='utf-8')

#9/11 ver 1
# from GUI import browse_files
# from chunking import PDF_parser_chunker
# from vectorize import process_and_upload_chunks
# from slide_keywords import read_pptx, llm_keywords, get_keyword_vectors
# from qdrant_utils import search_vectors, initialize_qdrant_client_cloud


# def main():
#     # Step 1: Upload textbook and slides via GUI
#     textbook, slides = browse_files()
#     print("Textbook Path:", textbook)
#     print("Slides Path:", slides)

#     # Step 2: Chunk the textbook (using PDF_parser_chunker)
#     chunks = PDF_parser_chunker(textbook).Chunker()

#     # Step 3: Get vector embeddings for the chunks and upload to Qdrant Cloud
#     collection_name = "NoteBot"  # You can specify your collection name here
#     formatted_embeddings = process_and_upload_chunks(chunks, collection_name)

#     # Print the uploaded vectors and their metadata (text chunk)
#     for point in formatted_embeddings:
#         print(f"ID: {point['id']}")
#         print(f"Vector: {point['vector']}")
#         # Encode the payload text to handle special characters
#         print(f"Metadata (Text Chunk): {point['payload']['text'].encode('utf-8', 'replace').decode('utf-8')}")
#         print("-" * 50)

#     # Step 4: Extract text from the slides and generate keywords
#     slide_text = read_pptx(slides)
#     keywords = llm_keywords(slide_text)
#     print("Keywords Extracted:", keywords)

#     # Step 5: Get vector embeddings for the extracted keywords
#     keyword_vectors = get_keyword_vectors(keywords)
#     print(f"Number of Keyword Vectors: {len(keyword_vectors)}")

#     # Step 6: Perform similarity search on Qdrant Cloud (using keyword vectors)
#     client = initialize_qdrant_client_cloud()
#     for keyword_vector in keyword_vectors:
#         search_results = search_vectors(client, collection_name, query_vector=keyword_vector, keyword=keyword, limit=3)

#         # # Step 7: Output the matching text from Qdrant for each keyword
#         # print("Search Results for Keyword Vector:")
#         # for result in search_results:
#         #     print(f"Matching Text: {result.payload['text']}")

#     import sys
#     sys.stdout.reconfigure(encoding='utf-8')


# if __name__ == "__main__":
#     main()


#9/11 ver 2
from GUI import browse_files
from chunking import PDF_parser_chunker
from vectorize import process_and_upload_chunks
from slide_keywords import read_pptx, llm_keywords, get_keyword_vectors
from qdrant_utils import search_vectors, initialize_qdrant_client_cloud


def main():
    # Step 1: Upload textbook and slides via GUI
    textbook, slides = browse_files()
    print("Textbook Path:", textbook)
    print("Slides Path:", slides)

    # Step 2: Chunk the textbook (using PDF_parser_chunker)
    chunks = PDF_parser_chunker(textbook).Chunker()

    # Step 3: Get vector embeddings for the chunks and upload to Qdrant Cloud
    collection_name = "NoteBot"  # You can specify your collection name here
    formatted_embeddings = process_and_upload_chunks(chunks, collection_name)

    # Print the uploaded vectors and their metadata (text chunk)
    for point in formatted_embeddings:
        print(f"ID: {point['id']}")
        print(f"Vector: {point['vector']}")
        # Encode the payload text to handle special characters
        print(f"Metadata (Text Chunk): {point['payload']['text'].encode('utf-8', 'replace').decode('utf-8')}")
        print("-" * 50)

    # Step 4: Extract text from the slides and generate keywords
    slide_text = read_pptx(slides)
    keywords = llm_keywords(slide_text)
    print("Keywords Extracted:", keywords)

    # Step 5: Get vector embeddings for the extracted keywords
    keyword_vectors = get_keyword_vectors(keywords)
    print(f"Number of Keyword Vectors: {len(keyword_vectors)}")

    # Step 6: Perform similarity search on Qdrant Cloud (using keyword vectors)
    client = initialize_qdrant_client_cloud()
    
    # Loop through both keywords and their corresponding keyword vectors
    for keyword, keyword_vector in zip(keywords, keyword_vectors):
        print("-" * 200)
        print(f"Search Results for Keyword: {keyword}")  # Print the current keyword
        search_results = search_vectors(client, collection_name, query_vector=keyword_vector, keyword=keyword, limit=3)

    import sys
    sys.stdout.reconfigure(encoding='utf-8')


if __name__ == "__main__":
    main()
