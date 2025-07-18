# ruff: noqa: TC004, B018

from __future__ import annotations

import re
from typing import TYPE_CHECKING


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    import Gui


class UserMacro:
    """Rename the selected objects using a regex pattern."""

    @staticmethod
    def run(pattern: str, replace: str, dry_run: bool = True) -> None:
        """Run macro.

        Args:
            find: Regex pattern.
            replace: The string to replace the captured text.
        """

        re_pattern = re.compile(pattern)

        for obj in Gui.Selection.getSelection():
            try:
                obj.Label
            except AttributeError:
                # Not sure if this will ever trigger.
                print(f"Object '{obj}' has no 'Label' attribute.")
                continue

            new_label = re_pattern.sub(replace, obj.Label)

            if obj.Label != new_label:
                print(f"Renaming: {obj.Label} -> {new_label}")

                if dry_run is False:
                    obj.Label = new_label


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
UserMacro().run(
    pattern,
    replace,
    dry_run,
)
