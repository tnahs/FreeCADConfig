# ruff: noqa: TC004

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide2 import QtWidgets


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCADGui


class UserMacro:
    @staticmethod
    def run() -> None:
        main_window = FreeCADGui.getMainWindow()

        python_console = main_window.findChild(QtWidgets.QDockWidget, "Python console")
        report_view = main_window.findChild(QtWidgets.QDockWidget, "Report view")

        if report_view.isVisible() or python_console.isVisible():
            report_view.hide()
            python_console.hide()
        else:
            report_view.show()
            python_console.show()


UserMacro().run()
