from RPA.Word.Application import Application
from robot.api.deco import keyword


class WordHelper:
    """Helper class for creating Word documents via RPA Framework."""

    def __init__(self):
        self.app = None
        self.file_path = None

    @keyword("Create Doc")
    def create_doc(self, file_path):
        """Start Word and create a new document."""
        self.app = Application()
        self.app.open_application()
        self.app.create_new_document()
        self.file_path = file_path

    @keyword("Add Paragraph")
    def add_paragraph(self, text):
        """Add a paragraph of text to the document."""
        if not self.app:
            raise Exception("Word not started. Use 'Create Doc' first.")
        self.app.add_paragraph(text)

    @keyword("Add Picture")
    def add_picture(self, image_path, width=15.0, height=None):
        """Insert an image into the document."""
        if not self.app:
            raise Exception("Word not started. Use 'Create Doc' first.")
        self.app.add_picture(image_path, width=width, height=height)

    @keyword("Save And Close")
    def save_and_close(self):
        """Save and close the document."""
        if not self.app or not self.file_path:
            raise Exception("No open document or file path not set.")
        self.app.save_document(self.file_path)
        self.app.close_document()
        self.app.quit_application()
        self.app = None
        self.file_path = None
