import os
from openpyxl import Workbook, load_workbook


class Excel:
    def __init__(self, path: str):
        """
        Initialize Excel handler.
        If the file exists, load it.
        Otherwise, create a new file and save it.
        """
        self.path = path

        if os.path.exists(path):
            self.wb = load_workbook(path)
        else:
            self.wb = Workbook()
            self.save()

    def save(self) -> None:
        """Save the workbook to the file."""
        self.wb.save(self.path)

    def sheet(self, name: str = None):
        """
        Get a worksheet by name.
        If name is None, return the active sheet.
        """
        if name:
            return self.wb[name]
        return self.wb.active

    def create_sheet(self, name: str) -> None:
        """Create a new worksheet with the given name."""
        self.wb.create_sheet(title=name)
        self.save()

    def list_sheets(self) -> list[str]:
        """Return the names of all sheets."""
        return self.wb.sheetnames
