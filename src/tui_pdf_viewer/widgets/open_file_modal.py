import os
from textual.screen import ModalScreen
from textual.widgets import Label, Button, DataTable
from textual.containers import Grid
from textual.app import ComposeResult
from textual.binding import Binding

class OpenFileModal(ModalScreen[str]):
    """Modal screen to select a file."""

    CSS = """
    OpenFileModal {
        align: center middle;
    }

    #dialog {
        grid-size: 1;
        grid-rows: auto 1fr auto;
        padding: 0 1;
        width: 80%;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
    }

    #path_label {
        padding: 1;
        background: $primary;
        color: $text;
        width: 100%;
    }

    DataTable {
        height: 1fr;
        border: solid $secondary;
    }

    #cancel_button {
        width: 100%;
    }
    """

    BINDINGS = [
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(self, initial_path: str = "."):
        super().__init__()
        self.current_path = os.path.abspath(initial_path)

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.current_path, id="path_label"),
            DataTable(id="file_table"),
            Button("Cancel", variant="error", id="cancel_button"),
            id="dialog",
        )

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Name", "Type")
        table.cursor_type = "row"
        self.refresh_file_list()

    def refresh_file_list(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        self.query_one("#path_label", Label).update(self.current_path)

        try:
            entries = os.scandir(self.current_path)
            # Sort: Directories first, then files
            sorted_entries = sorted(entries, key=lambda e: (not e.is_dir(), e.name.lower()))

            # Add ".." entry if not root
            parent = os.path.dirname(self.current_path)
            if parent != self.current_path:
                 table.add_row("..", "DIR", key="..")

            for entry in sorted_entries:
                if entry.name.startswith("."):
                    continue # Skip hidden files for simplicity
                
                type_str = "DIR" if entry.is_dir() else "FILE"
                table.add_row(entry.name, type_str, key=entry.name)
                
        except PermissionError:
            self.notify("Permission denied", severity="error")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        selected_key = event.row_key.value
        if selected_key == "..":
            self.current_path = os.path.dirname(self.current_path)
            self.refresh_file_list()
        else:
            new_path = os.path.join(self.current_path, selected_key)
            if os.path.isdir(new_path):
                self.current_path = new_path
                self.refresh_file_list()
            elif os.path.isfile(new_path):
                if new_path.lower().endswith(".pdf"):
                    self.dismiss(new_path)
                else:
                    self.notify("Please select a PDF file", severity="warning")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel_button":
            self.dismiss(None)
    
    def action_cancel(self) -> None:
        self.dismiss(None)
