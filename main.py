#importing functions
from GUI import browse_files
from vectorize import process_chunks

#uploading textbook excerpt and slides
textbook, slides = browse_files()
print("Textbook Path:", textbook)
print("Slides Path:", slides)

#chunk the extracted text from the textbook excerpt
chunks = [
    "This is the first chunk of text.",
    "Here is the second chunk of the text data.",
    "This is the third chunk of text we are processing."
]

#get vector embeddings for chunks
formatted_embeddings=process_chunks(chunks)
for point in formatted_embeddings:
    print(f"ID: {point['id']}")
    print(f"Vector: {point['vector']}")
    print(f"Metadata (Text Chunk): {point['payload']['text']}")
    print("-" * 50)
