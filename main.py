#importing functions
from GUI import browse_files
# Importing the class from the file
# from chunking import PDF_parser_chunker
from vectorize import process_chunks
from slide_keywords import read_pptx, llm_keywords, get_keyword_vectors

#upload textbook excerpt and slides
textbook, slides = browse_files()
print("Textbook Path:", textbook)
print("Slides Path:", slides)

#chunk the extracted text from the textbook excerpt
chunks = [
    "This is the first chunk of text.",
    "Here is the second chunk of the text data.",
    "This is the third chunk of text we are processing."
]

# Calling the function to chunk, stored as a list in chunks
# chunks = PDF_parser_chunker(textbook).Chunker()

#get vector embeddings for chunks
formatted_embeddings=process_chunks(chunks)
for point in formatted_embeddings:
    print(f"ID: {point['id']}")
    print(f"Vector: {point['vector']}")
    print(f"Metadata (Text Chunk): {point['payload']['text']}")
    print("-" * 50)

#get vectorized keywords from uploaded slides
slide_text = read_pptx(slides) 
keywords = llm_keywords(slide_text)
print(keywords)
keyword_vectors = get_keyword_vectors(keywords)
print(len(keyword_vectors))