from textual.widgets import Static
from textual.reactive import reactive
from textual.binding import Binding

class PDFViewer(Static):
    """A widget to display PDF content."""
    
    text_content = reactive("")

    BINDINGS = [
        Binding("j", "scroll_down", "Scroll Down", show=False),
        Binding("k", "scroll_up", "Scroll Up", show=False),
    ]

    def watch_text_content(self, new_text: str) -> None:
        self.update(new_text)


