# Importing necessary libraries
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.high_level import extract_pages
from collections import defaultdict
import re
import tiktoken

# Class to hold metadata of each line
class DocumentLineItem:
    def __init__(self, position_x, position_y, content, font_height, total_characters):
        self.position_x = position_x
        self.position_y = position_y
        self.content = content
        self.font_height = font_height
        self.total_characters = total_characters

    def __repr__(self):
        return f"Font Height: {self.font_height}, Text: {self.content}"

# Main class to parse, chunk, and process PDFs
class PDF_parser_chunker:
    def __init__(self, file_path, token_limit=512, overlap=2):
        self.file_path = file_path
        self.line_items = []
        self.chunks = defaultdict(list)
        self.final = []
        self.token_limit = token_limit
        self.overlap = overlap
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def parse_pdf(self):
        """Function to parse pdf and extract relevant font metadata."""
        for page_layout in extract_pages(self.file_path, laparams=LAParams()):
            for element in page_layout:
                if isinstance(element, LTTextBox):
                    for line in element:
                        if isinstance(line, LTTextLine):
                            font_sizes = []
                            content = line.get_text().strip()
                            total_characters = len(content)
                            for char in line:
                                if isinstance(char, LTChar):
                                    font_sizes.append(char.size)
                            if font_sizes:
                                avg_font_size = round(sum(font_sizes) / len(font_sizes))
                                line_item = DocumentLineItem(line.x0, line.y0, content, avg_font_size, total_characters)
                                self.line_items.append(line_item)
                                
    def font_list(self):
        """Returns the list of font heights, arranged in ascending order."""
        font_heights = sorted(set(item.font_height for item in self.line_items), reverse=True)
        return font_heights

    def headers_by_font(self, unique_fonts):  
        """Returns the guessed size of the font used for the headings"""
        header_threshold = unique_fonts[:2]  
        return header_threshold

    def chunk_document(self, header_fonts):
        """Chunking of the document based on headers (does not heed the limit)"""
        current_header = None
        for item in self.line_items:
            if item.font_height in header_fonts:
                current_header = item.content
                self.chunks[current_header] = []  
            elif current_header: 
                self.chunks[current_header].append(item.content)

    def process_pdf(self):
        """Inital processing and creation of chunks from the pdf."""
        self.parse_pdf()
        unique_fonts = self.font_list()
        header_fonts = self.headers_by_font(unique_fonts)
        self.chunk_document(header_fonts)
        return self.chunks

    def count_tokens(self, text):
        """Count the number of tokens in a given text string."""
        tokens = self.encoding.encode(text)
        return len(tokens)

    def split_chunk(self, sentences):
        """Splits a list of sentences into chunks that don't exceed the limit."""
        final_chunks = []
        current_chunk = []
        for sentence in sentences:
            temp_chunk = current_chunk + [sentence]
            current_text = ' '.join(temp_chunk)
            num_tokens = self.count_tokens(current_text)
            if num_tokens <= self.token_limit:
                current_chunk = temp_chunk
            else:
                if current_chunk:
                    final_chunks.append(current_chunk[:])  
                current_chunk = current_chunk[-self.overlap:] if len(current_chunk) > self.overlap else current_chunk
                current_chunk.append(sentence)

        if current_chunk:
            final_chunks.append(current_chunk[:])

        return final_chunks

    def comp_sent(self, lines: list):
        """
        Takes a list of strings (lines), joins them into a single string,
        processes sentences by handling abbreviations, and returns a list containing
        complete sentences.
        """
        full_text = ' '.join(lines)
        raw_sentences = re.split(r'(?<=[.!?])\s+', full_text.strip())
        sentences = []
        for sentence in raw_sentences:
            sentence = sentence.strip()
            if not sentence:
                continue  
            if sentences and sentence.lstrip()[0].isupper() != True:
                last_sentence = sentences[-1]
                combined_sentence = last_sentence + ' ' + sentence
                if self.count_tokens(combined_sentence) <= self.token_limit:
                    sentences[-1] = combined_sentence 
                else:
                    sentences.append(sentence)  
            else:
                sentences.append(sentence)  
        return sentences

    def util_splitter(self, chunk: list)->list:
        """Utility function to split a chunk into pieces that don't exceed the token limit."""
        sentences = self.comp_sent(chunk)
        chunks = self.split_chunk(sentences)
        return chunks

    def final_chunks(self):
        """Final chunking function, returns list of chunks that are within token limit."""
        for i in self.chunks.items():
            if self.count_tokens(' '.join(i[1])) > self.token_limit:
                temp = self.util_splitter(i[1])
                for j in temp:
                    self.final.append(j)
                temp = []
            else:
                self.final.append(i[1])
        return self.final

    def Chunker(self):
        p = PDF_parser_chunker(self.file_path)
        ch = p.process_pdf()
        fin = p.final_chunks()
        return fin