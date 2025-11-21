import sys
import os
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import Container
from textual.binding import Binding
from tui_pdf_viewer.widgets.pdf_viewer import PDFViewer
from tui_pdf_viewer.widgets.goto_page_modal import GotoPageModal
from tui_pdf_viewer.widgets.help_screen import HelpScreen
from tui_pdf_viewer.widgets.open_file_modal import OpenFileModal
from tui_pdf_viewer.utils.pdf_handler import PDFHandler

class PDFViewerApp(App):
    """A Textual app to view PDFs."""

    CSS = """
    PDFViewer {
        height: 1fr;
        border: solid green;
        padding: 1;
        overflow-y: auto;
    }
    """

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle Dark Mode"),
        Binding("q", "quit", "Quit"),
        Binding("n", "next_page", "Next Page"),
        Binding("p", "prev_page", "Previous Page"),
        Binding("g", "goto_page", "Go to Page"),
        Binding("o", "open_file", "Open File"),
        Binding("?", "help", "Help"),
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
        self.load_pdf(self.file_path)

    def load_pdf(self, path: str) -> None:
        try:
            if self.pdf_handler:
                self.pdf_handler.close()
            
            self.file_path = path
            self.pdf_handler = PDFHandler(self.file_path)
            self.load_page(0)
            self.title = f"TUI PDF Viewer - {path}"
        except Exception as e:
            self.notify(f"Error loading PDF: {e}", severity="error")

    def load_page(self, page_num: int) -> None:
        if self.pdf_handler:
            total_pages = self.pdf_handler.get_page_count()
            if 0 <= page_num < total_pages:
                text = self.pdf_handler.get_page_text(page_num)
                viewer = self.query_one("#pdf_viewer", PDFViewer)
                viewer.text_content = text
                # Reset scroll position
                viewer.scroll_home(animate=False)
                self.current_page = page_num
                self.sub_title = f"Page {page_num + 1} of {total_pages}"

    def action_next_page(self) -> None:
        self.load_page(self.current_page + 1)

    def action_prev_page(self) -> None:
        self.load_page(self.current_page - 1)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_goto_page(self) -> None:
        def check_page(page_num: int | None) -> None:
            if page_num is not None:
                # User input is 1-based, convert to 0-based
                self.load_page(page_num - 1)
        
        self.push_screen(GotoPageModal(), check_page)

    def action_open_file(self) -> None:
        def check_file(file_path: str | None) -> None:
            if file_path:
                self.load_pdf(file_path)
        
        self.push_screen(OpenFileModal(initial_path=os.path.dirname(self.file_path) or "."), check_file)

    def action_help(self) -> None:
        self.push_screen(HelpScreen())

def main():
    if len(sys.argv) < 2:
        print("Usage: tui-pdf-viewer <path_to_pdf>")
        sys.exit(1)
    
    app = PDFViewerApp(sys.argv[1])
    app.run()

if __name__ == "__main__":
    main()
