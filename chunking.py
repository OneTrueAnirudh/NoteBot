# from langchain_experimental.text_splitter import SemanticChunker
# from sentence_transformers import SentenceTransformer

# # Initialize a local embedding model from Hugging Face (e.g., SentenceTransformer)
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# # Define a custom embedding function
# class CustomEmbeddings:
#     def embed_documents(self, texts):
#         return model.encode(texts)

#     def embed_query(self, text):
#         return model.encode([text])[0]

# # Use the custom embedding function in the SemanticChunker
# custom_embeddings = CustomEmbeddings()
# text_splitter = SemanticChunker(custom_embeddings)

# # Load your text
# with open("textbook.txt", encoding="utf-8") as f:
#     bojack_horseman = f.read()

# # Split text into chunks using semantic chunking
# docs = text_splitter.create_documents([bojack_horseman])

# # Output the first chunk of text
# for i in docs:
#     print(i.page_content, end="\n\n")

from llama_index.core import SimpleDirectoryReader
documents = SimpleDirectoryReader(input_files=["textbook.txt"]).load_data()
from llama_index.core.node_parser import SemanticDoubleMergingSplitterNodeParser, LanguageConfig
config = LanguageConfig(language="english", spacy_model="en_core_web_md")
splitter = SemanticDoubleMergingSplitterNodeParser(
    language_config=config,
    initial_threshold=0.5,
    appending_threshold=0.85,
    merging_threshold=0.85,
    max_chunk_size=5000,
)
nodes = splitter.get_nodes_from_documents(documents)
for node in nodes:
    print(node)