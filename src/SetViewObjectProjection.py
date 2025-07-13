# ruff: noqa: TC004, B018

from __future__ import annotations

from typing import TYPE_CHECKING


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCAD
    import Gui

document = FreeCAD.ActiveDocument


class UserMacro:
    TARGET_TYPE_ID = "TechDraw::DrawProjGroupItem"

    def run(self) -> None:
        objects = Gui.Selection.getSelection() or FreeCAD.activeDocument().Objects
        projections = [obj for obj in objects if obj.TypeId == self.TARGET_TYPE_ID]

        for projection in projections:
            try:
                view = projection.ViewObject
                view.ExtraWidth
                view.IsoWidth
                view.LineWidth
                view.HiddenWidth
            except AttributeError:
                print(f"Skipped {projection.Label}. Object does not have a ViewObject.")
                continue

            view.ExtraWidth = "0.508 mm"
            view.IsoWidth = "0.254 mm"
            view.LineWidth = "0.254 mm"
            view.HiddenWidth = "0.254 mm"


UserMacro().run()
