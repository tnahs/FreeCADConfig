# ruff: noqa: TC004

from __future__ import annotations

from typing import TYPE_CHECKING


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCAD


class UserMacro:
    @staticmethod
    def run() -> None:
        document = FreeCAD.ActiveDocument

        for obj in document.Objects:
            obj.touch()

        print("Recomputing objects...")
        document.recompute()
        print("Recomputing complete!")


UserMacro().run()
