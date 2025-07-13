# ruff: noqa: TC004

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import TYPE_CHECKING

from PySide import QtCore, QtGui


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCADGui


def cell_to_index(cell: str) -> tuple[int, int]:
    match = re.match(r"([A-Z]+)(\d+)", cell)
    if not match:
        raise ValueError(f"Invalid cell format: {cell}")
    col_str, row_str = match.groups()
    col = (
        sum(
            (ord(char) - ord("A") + 1) * (26**i)
            for i, char in enumerate(reversed(col_str))
        )
        - 1
    )
    row = int(row_str) - 1
    return row, col


class UserMacro:
    @staticmethod
    def run(cell_range: str, output_filepath: Path) -> None:
        """Export the selected cells to a CSV file."""

        main_window = FreeCADGui.getMainWindow()
        mdi_area = main_window.findChild(QtGui.QMdiArea)

        table_view = None

        for obj in mdi_area.subWindowList():
            if obj.widget().metaObject().className() == "SpreadsheetGui::SheetView":
                table_view = obj.widget().findChild(QtGui.QTableView)
                break

        if not table_view:
            print("No table view found.")
            return

        selection_model = table_view.selectionModel()

        if not selection_model:
            print("No selection model found.")
            return

        model = table_view.model()

        if not model:
            print("No model found.")
            return

        try:
            start_cell, end_cell = cell_range.split(":")
            start_row, start_column = cell_to_index(start_cell)
            end_row, end_column = cell_to_index(end_cell)
        except ValueError as e:
            print(f"Error parsing cell range: {e}")
            return

        data = []

        for row in range(start_row, end_row + 1):
            row_data = []

            for column in range(start_column, end_column + 1):
                index = model.index(row, column)
                row_data.append(model.data(index, QtCore.Qt.DisplayRole) or "")

            data.append(row_data)

        with output_filepath.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"Exported spreadsheet to {output_filepath}")


UserMacro().run(
    cell_range="",
    output_filepath=Path.cwd(),
)
