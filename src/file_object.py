from pathlib import Path

class FileObject():
    def __init__(self, text: str, path: Path):
        self.text = text
        self.path = path

    def __repr__(self):
        return f"File Name: {self.path}\nContents:\n{self.text}"