# import pdfplumber
# import re

# class PDFProcessor:
#     """Handles text extraction and normalization from a PDF file."""

#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.text = ""

#     def extract_text(self):
#         """Extracts raw text from the PDF file."""
#         try:
#             with pdfplumber.open(self.file_path) as pdf:
#                 for page in pdf.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         self.text += page_text + "\n"
#             return self.text
#         except Exception as e:
#             print(f"Error reading {self.file_path}: {e}")
#             return ""

#     def normalize_text(self):
#         """Normalizes text by handling common synonyms and converting to lowercase."""
#         self.text = self.text.lower()
#         synonyms = {
#             "ml": "machine learning",
#             "ai": "artificial intelligence",
#             "js": "javascript",
#             "py": "python",
#             "nlp": "natural language processing",
#             "restful apis": "rest api",
#             "web services": "rest api",
#             "devops engineer": "devops",
#             "git": "version control",
#             "docker container": "docker",
#             "k8s": "kubernetes",
#             "dsa": "data structures and algorithms"
#         }
#         for key, value in synonyms.items():
#             pattern = r'\b' + re.escape(key) + r'\b'
#             self.text = re.sub(pattern, value, self.text)
#         return self.text


# # pdf_processor.py
# import pdfplumber
# import re

# class PDFProcessor:
#     """Handles text extraction and normalization from a PDF file."""

#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.text = ""

#     def extract_text(self):
#         """Extracts raw text from the PDF file."""
#         try:
#             with pdfplumber.open(self.file_path) as pdf:
#                 for page in pdf.pages:
#                     page_text = page.extract_text()
#                     if page_text:
#                         self.text += page_text + "\n"
#             return self.text
#         except Exception as e:
#             print(f"Error reading {self.file_path}: {e}")
#             return ""

#     def normalize_text(self):
#         """Normalizes text by handling common synonyms and converting to lowercase."""
#         self.text = self.text.lower()
#         synonyms = {
#             "ml": "machine learning",
#             "ai": "artificial intelligence",
#             "js": "javascript",
#             "py": "python",
#             "nlp": "natural language processing",
#             "restful apis": "rest api",
#             "web services": "rest api",
#             "devops engineer": "devops",
#             "git": "version control",
#             "docker container": "docker",
#             "k8s": "kubernetes",
#             "dsa": "data structures and algorithms"
#         }
#         for key, value in synonyms.items():
#             pattern = r'\b' + re.escape(key) + r'\b'
#             self.text = re.sub(pattern, value, self.text)
#         return self.text



# ats_analyzer/pdf_processor.py

import re
import pdfplumber
from sentence_transformers import SentenceTransformer, util


class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def extract_text(self):
        """
        Extract text from PDF using pdfplumber (better formatting than PyPDF2).
        """
        try:
            text = ""
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return ""

    def normalize_text(self, text=None):
        """
        Normalize text: lowercase + remove extra spaces.
        """
        if text is None:
            text = self.extract_text()
        return re.sub(r"\s+", " ", text).lower().strip()

    def chunk_text(self, text):
        """
        Split text into smaller chunks based on bullets, dashes, and line breaks.
        """
        chunks = re.split(r"[\n•\-•]+", text)
        return [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]

    def classify_sections(self, text):
        """
        Classify resume/job text into dynamic sections using embeddings.
        Returns: dict with section_name -> list of chunks
        """
        section_labels = [
            "skills", "experience", "education",
            "projects", "achievements", "keywords", "other"
        ]

        label_embeddings = self.model.encode(section_labels, convert_to_tensor=True)
        chunks = self.chunk_text(text)
        chunk_embeddings = self.model.encode(chunks, convert_to_tensor=True)

        section_map = {label: [] for label in section_labels}

        for i, chunk in enumerate(chunks):
            similarities = util.cos_sim(chunk_embeddings[i], label_embeddings)
            best_label_idx = similarities.argmax().item()
            best_label = section_labels[best_label_idx]
            section_map[best_label].append(chunk)

        return section_map
    
    def _clean_pdf_artifacts(self, text):
        """
        Remove PDF artifacts like (cid:xxx) and other common PDF extraction issues.
        """
        # Remove (cid:xxx) patterns
        text = re.sub(r'\(cid:\d+\)', '', text)
        
        # Replace bullet point artifacts with proper bullets
        text = re.sub(r'[•▪➢➤]', '•', text)
        
        # Remove multiple spaces and clean up formatting
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\.\s+\.', '.', text)  # Fix double periods
        
        return text.strip()
