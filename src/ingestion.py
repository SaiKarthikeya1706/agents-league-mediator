import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentPipeline:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def _process(self, loader):
        documents = loader.load()
        return self.splitter.split_documents(documents)

    def process_pdf_file(self, path):
        return self._process(PyPDFLoader(path))

    def process_docx_file(self, path):
        return self._process(Docx2txtLoader(path))

    def process_txt_file(self, path):
        return self._process(TextLoader(path))
    
    # You can add Excel (.xlsx) support here using UnstructuredExcelLoader