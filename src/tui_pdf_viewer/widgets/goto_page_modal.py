from textual.screen import ModalScreen
from textual.widgets import Label, Input, Button
from textual.containers import Grid
from textual.app import ComposeResult

class GotoPageModal(ModalScreen[int]):
    """Modal screen to jump to a specific page."""

    CSS = """
    GotoPageModal {
        align: center middle;
    }

    #dialog {
        grid-size: 2;
        grid-gutter: 1 2;
        grid-rows: 1fr 3;
        padding: 0 1;
        width: 60;
        height: 11;
        border: thick $background 80%;
        background: $surface;
    }

    #question {
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: center middle;
    }

    Button {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Enter page number:", id="question"),
            Input(placeholder="Page number", id="page_input", type="integer"),
            Button("Go", variant="primary", id="go_button"),
            Button("Cancel", variant="default", id="cancel_button"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "go_button":
            input_widget = self.query_one("#page_input", Input)
            if input_widget.value:
                try:
                    page_num = int(input_widget.value)
                    self.dismiss(page_num)
                except ValueError:
                    pass # Handle invalid input if needed
        elif event.button.id == "cancel_button":
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.value:
             try:
                page_num = int(event.input.value)
                self.dismiss(page_num)
             except ValueError:
                pass
