# ruff: noqa: TC004

from __future__ import annotations

from typing import TYPE_CHECKING


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCAD
    import Gui


class UserMacro:
    TYPE_ID_SKETCH = "Sketcher::SketchObject"

    def run(self, label: str | None = None) -> None:
        document = FreeCAD.activeDocument()

        if label is None:
            try:
                source_sketch = Gui.Selection.getSelection()[0]
            except IndexError:
                print("Select a sketch or provide a label to query!")
                return
        else:
            try:
                source_sketch = document.getObjectsByLabel(label)[0]
            except IndexError:
                print(f"Sketch '{label}' does not exist!")
                return

        if source_sketch.TypeId != self.TYPE_ID_SKETCH:
            print(f"Object '{label}' is not a Sketch!")
            return

        sketches = [
            sketch
            for sketch in document.Objects
            if sketch.TypeId == self.TYPE_ID_SKETCH
        ]

        references = set()

        for sketch in sketches:
            # (SketchObject, [Edge1, EdgeN])
            for external_sketch, _referenced_edges in sketch.ExternalGeometry:
                if external_sketch.Label == source_sketch.Label:
                    references.add(sketch.Label)
                    break

        if not references:
            print(f"Found no sketch references to {source_sketch.Label}.")
            return

        print(f"Found {len(references)} sketch references to {source_sketch.Label}:")
        for reference in references:
            print(f"  {reference}")


UserMacro().run()
