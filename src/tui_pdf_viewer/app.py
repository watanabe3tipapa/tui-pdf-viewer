import sys
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container
from textual.binding import Binding
from tui_pdf_viewer.widgets.pdf_viewer import PDFViewer
from tui_pdf_viewer.utils.pdf_handler import PDFHandler

class PDFViewerApp(App):
    """A Textual app to view PDFs."""

    CSS = """
    PDFViewer {
        height: 1fr;
        border: solid green;
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("q", "quit", "Quit"),
        Binding("n", "next_page", "Next Page"),
        Binding("p", "prev_page", "Previous Page"),
    ]

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.pdf_handler = None
        self.current_page = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(PDFViewer(id="pdf_viewer"))
        yield Footer()

    def on_mount(self) -> None:
        try:
            self.pdf_handler = PDFHandler(self.file_path)
            self.load_page(0)
        except Exception as e:
            self.notify(f"Error loading PDF: {e}", severity="error")

    def load_page(self, page_num: int) -> None:
        if self.pdf_handler:
            total_pages = self.pdf_handler.get_page_count()
            if 0 <= page_num < total_pages:
                text = self.pdf_handler.get_page_text(page_num)
                self.query_one("#pdf_viewer", PDFViewer).text_content = text
                self.current_page = page_num
                self.sub_title = f"Page {page_num + 1} of {total_pages}"

    def action_next_page(self) -> None:
        self.load_page(self.current_page + 1)

    def action_prev_page(self) -> None:
        self.load_page(self.current_page - 1)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

def main():
    if len(sys.argv) < 2:
        print("Usage: tui-pdf-viewer <path_to_pdf>")
        sys.exit(1)
    
    app = PDFViewerApp(sys.argv[1])
    app.run()

if __name__ == "__main__":
    main()
