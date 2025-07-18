# ruff: noqa: TC004, B018

from __future__ import annotations

import re
from typing import TYPE_CHECKING


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import Gui


# TODO: Implement.
class UserMacro:
    """Zero the transforms of an imported model."""

    @staticmethod
    def run() -> None:
        # >>> App.getDocument('FuseHolder_Littelfuse_03540002ZXGY').addObject('Part::Refine','Part__Feature016')
        # >>> App.getDocument('FuseHolder_Littelfuse_03540002ZXGY').ActiveObject.Source = FreeCAD.getDocument('FuseHolder_Littelfuse_03540002ZXGY').getObject('Part__Feature016')
        # >>> App.getDocument('FuseHolder_Littelfuse_03540002ZXGY').ActiveObject.Label = FreeCAD.getDocument('FuseHolder_Littelfuse_03540002ZXGY').getObject('Part__Feature016').Label
        # >>> App.getDocument('FuseHolder_Littelfuse_03540002ZXGY').getObject('Part__Feature016').Visibility = False
        # >>> __shape = Part.getShape(App.getDocument('FuseHolder_Littelfuse_03540002ZXGY').getObject('Part__Feature022'),'',needSubElement=False,refine=False)
        # >>> App.ActiveDocument.addObject('Part::Feature','Part__Feature022').Shape=__shape
        # >>> App.ActiveDocument.ActiveObject.Label=App.getDocument('FuseHolder_Littelfuse_03540002ZXGY').getObject('Part__Feature022').Label
        pass


UserMacro().run()
