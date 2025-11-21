from textual.screen import ModalScreen
from textual.widgets import Markdown
from textual.containers import Container

class HelpScreen(ModalScreen):
    """Screen to display help information."""

    CSS = """
    HelpScreen {
        align: center middle;
    }

    #help_container {
        width: 60;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    """

    HELP_TEXT = """
# Help

**Navigation**
- `n`: Next Page
- `p`: Previous Page
- `g`: Go to Page
- `j`: Scroll Down
- `k`: Scroll Up

**General**
- `d`: Toggle Dark Mode
- `?`: Toggle Help
- `q`: Quit
    """

    def compose(self):
        yield Container(
            Markdown(self.HELP_TEXT),
            id="help_container"
        )

    def on_key(self, event):
        if event.key in ("escape", "?"):
            self.dismiss()
