# ruff: noqa: TC004

from __future__ import annotations

from typing import TYPE_CHECKING


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCAD
    import FreeCADGui


document = FreeCAD.ActiveDocument
objs = FreeCADGui.Selection.getSelection()
obj = objs[0] if objs else None

doc = document
d = document
o = obj

if obj:
    print(obj.TypeId)
    for name in dir(obj):
        print(name)
