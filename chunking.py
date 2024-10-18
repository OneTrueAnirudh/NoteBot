from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar
from pdfminer.high_level import extract_pages
from collections import defaultdict

# to hold metadata of each line
class DocumentLineItem:
    def __init__(self, position_x, position_y, content, font_height, total_characters):
        self.position_x = position_x
        self.position_y = position_y
        self.content = content
        self.font_height = font_height
        self.total_characters = total_characters

    def __repr__(self):
        return f"Font Height: {self.font_height}, Text: {self.content}"

# class that contains the methods to process the pdf + create chunks. method process_pdf() to be used when adding to main.
class PDF_parser_chunker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.line_items = []
        self.chunks = defaultdict(list)

    # Function to parse PDF and extract font metadata
    def parse_pdf(self):
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

    # Function to get unique font heights
    def font_list(self):
        font_heights = sorted(set(item.font_height for item in self.line_items), reverse=True)
        return font_heights

    # Function to classify headers based on font size
    def headers_by_font(self, unique_fonts): # Heuristic: the largest font sizes represent headers. Top 2 font sizes are likely headers
        header_threshold = unique_fonts[:2]  
        return header_threshold

    # Chunk the document based on identified headers
    def chunk_document(self, header_fonts):
        current_header = None
        
        for item in self.line_items:
            if item.font_height in header_fonts:
                current_header = item.content
                self.chunks[current_header] = []  
            elif current_header: 
                self.chunks[current_header].append(item.content)

    # Main function to process the PDF and chunk based on headers
    def process_pdf(self):
        # parse the pdf and get likely topic heights
        self.parse_pdf()
        unique_fonts = self.font_list()
        print("\nUnique Font Heights (sorted):", unique_fonts)
        
        # classify headers based on font size
        header_fonts = self.headers_by_font(unique_fonts)
        print("\nClassified Header Font Sizes:", header_fonts)

        # chunk the document
        self.chunk_document(header_fonts)

        # print the chunks
        for header, content in self.chunks.items():
            print(f"\n\nHeader: {header}\nContent: {' '.join(content[:3])}...")  # show first few lines of each chunk
        return self.chunks

# sample usage
processor = PDF_parser_chunker('phil_book.pdf')
chunks = processor.process_pdf()
