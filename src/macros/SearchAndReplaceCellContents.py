# ruff: noqa: TC004

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from PySide import QtCore, QtGui


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCADGui


class UserMacro:
    """Replace the selected cells' contents using a regex pattern."""

    @staticmethod
    def run(pattern: str, replace: str, dry_run: bool = True) -> None:
        """Run macro.

        Args:
            find: Regex pattern.
            replace: The string to replace the captured text.
        """

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

        re_pattern = re.compile(pattern)

        for index in selection_model.selectedIndexes():
            contents = model.data(index, QtCore.Qt.DisplayRole)

            if not contents or not isinstance(contents, str):
                continue

            new_contents = re_pattern.sub(replace, contents)

            if dry_run is False:
                model.setData(index, new_contents, QtCore.Qt.EditRole)

            print(f"Renaming: {contents} -> {new_contents}")


pattern = r""
replace = r""
dry_run = False

# Remove a string from any part of the name.
#
# pattern = r"\(helper\)"
# replace = r""

# Remove a string from the end of the name.
#
# pattern = r"^(.*)_suffix$"
# replace = r"\1"

# Add a prexix/suffix to the name.
#
# pattern = r"^(.*)$"
# replace = r"prefix_\1_suffix"

# TODO: Build GUI.
UserMacro().run(pattern, replace, dry_run)
