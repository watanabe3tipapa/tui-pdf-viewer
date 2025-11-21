import fitz  # PyMuPDF

class PDFHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = fitz.open(file_path)

    def get_page_count(self) -> int:
        return len(self.doc)

    def get_page_text(self, page_num: int) -> str:
        if 0 <= page_num < len(self.doc):
            page = self.doc.load_page(page_num)
            return page.get_text("text")
        return ""

    def close(self):
        if self.doc:
            self.doc.close()
