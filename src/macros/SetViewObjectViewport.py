# ruff: noqa: TC004, B018

from __future__ import annotations

import contextlib
import math
from typing import TYPE_CHECKING, Any


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import FreeCAD
    import Gui

    # This is a FreeCAD type that seems inaccessible to Python.
    ViewObjectProxy = Any

    Color4f = tuple[
        float,  # R
        float,  # G
        float,  # B
        float,
    ]


class UserMacro:
    """Set the color and line weight for all or selected objects."""

    # Default FreeCAD color as floats.
    DEFAULT_DIFFUSE_COLOR: Color4f = (
        0.44705,  # 114
        0.47450,  # 121
        0.50196,  # 128
        0.0,
    )

    LINE_WIDTH = 1
    LINE_COLOR: Color4f = (
        25,
        25,
        25,
        0,
    )

    POINT_SIZE = 3
    POINT_COLOR = LINE_COLOR

    def run(
        self,
        diffuse_color: Color4f | None = None,
        retain_diffuse_color: bool = True,
        enable_auto_color: bool = True,
    ) -> None:
        """Run macro.

        Args:
            diffuse_color: Set all target objects to this color. A value of `None` will
                use FreeCAD's default diffuse color.
            retain_diffuse_color: Retain the object's diffuse color if it's different
                from FreeCAD's default. This allows us to retain the color for any
                objects that might have alredy had their color modified.

        """
        objects = Gui.Selection.getSelection() or FreeCAD.activeDocument().Objects

        for obj in objects:
            try:
                view = obj.ViewObject
                view.LineColor
                view.LineWidth
                view.PointColor
                view.PointSize
                view.ShapeAppearance
            except AttributeError:
                print(f"Skipped {obj.Label}. Object does not have a ViewObject.")
                continue

            if enable_auto_color is True:
                with contextlib.suppress(AttributeError):
                    view.AutoColor = True

            view.LineColor = self.LINE_COLOR
            view.LineWidth = self.LINE_WIDTH
            view.PointColor = self.POINT_COLOR
            view.PointSize = self.POINT_SIZE

            surface_material = self.new_surface_material(diffuse_color)

            if retain_diffuse_color:
                diffuse_color = self.get_diffuse_color(view)

                if not self.colors_match(diffuse_color, self.DEFAULT_DIFFUSE_COLOR):
                    surface_material = self.new_surface_material(diffuse_color)

            view.ShapeAppearance = surface_material

    def new_surface_material(
        self, diffuse_color: Color4f | None = None
    ) -> FreeCAD.Material:
        return FreeCAD.Material(
            DiffuseColor=diffuse_color or self.DEFAULT_DIFFUSE_COLOR,
            AmbientColor=(
                128,
                128,
                128,
            ),
            SpecularColor=(
                40,
                40,
                40,
            ),
            EmissiveColor=(
                10,
                10,
                10,
            ),
            Shininess=0.50,
            Transparency=0.0,
        )

    @staticmethod
    def get_diffuse_color(view: ViewObjectProxy) -> Color4f:
        """Returns the diffuse color of a ViewObject's material.

        This might raise an AttributeError or an IndexError.

        Returns:
            Color4f: The diffuse color.
        """

        return view.ShapeAppearance[0].DiffuseColor

    @staticmethod
    def colors_match(
        color1: Color4f, color2: Color4f, tolerance: float = 0.001
    ) -> bool:
        return all(
            math.isclose(component1, component2, abs_tol=tolerance)
            for component1, component2 in zip(color1, color2, strict=True)
        )


UserMacro().run(retain_diffuse_color=True)
