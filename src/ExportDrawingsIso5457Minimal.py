# ruff: noqa: TC004

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any


# All FreeCAD types should be placed here.
if TYPE_CHECKING:
    from collections.abc import Iterator

    import FreeCAD
    import FreeCADGui
    import Gui

    # This is a FreeCAD type that seems inaccessible to Python.
    DrawPageProxy = Any


class PageData:
    _revision: str | int = ""
    _page_count: int = 0
    _page_number: int = 0
    _date_format = "%Y-%m-%d"

    date = datetime.now(tz=UTC).today().date()

    def iter_default_fields(self) -> Iterator[tuple[str, Any]]:
        raise NotImplementedError

    def iter_mutable_fields(self) -> Iterator[tuple[str, Any]]:
        raise NotImplementedError

    def set_page_field_data(self, page: DrawPageProxy, page_number: int) -> None:
        self._page_number = page_number

        for key, value in self.iter_default_fields():
            page.Template.setEditFieldContent(key, str(value))

        for key, value in self.iter_mutable_fields():
            page.Template.setEditFieldContent(key, str(value))

    def clear_page_mutable_field_data(self, page: DrawPageProxy) -> None:
        for key, _ in self.iter_mutable_fields():
            page.Template.setEditFieldContent(key, "")

    def set_revision(self, value: str | int) -> None:
        self._revision = value

    def set_page_count(self, value: int) -> None:
        self._page_count = value

    def set_date_format(self, value: str) -> None:
        self._date_format = value


@dataclass
class PageDataIso5457(PageData):
    approval_person: str = ""
    creator: str = ""
    document_type: str = ""
    general_tolerances: str = ""
    identification_number: str = ""
    language_code: str = ""
    legal_owner_1: str = ""
    legal_owner_2: str = ""
    legal_owner_3: str = ""
    legal_owner_4: str = ""
    part_material: str = ""
    title: str = ""

    def iter_default_fields(self) -> Iterator[tuple[str, Any]]:
        yield from [
            # ruff: noqa: E241
            ("approval_person",       self.approval_person),
            ("creator",               self.creator),
            ("document_type",         self.document_type),
            ("general_tolerances",    self.general_tolerances),
            ("identification_number", self.identification_number),
            ("language_code",         self.language_code),
            ("legal_owner_1",         self.legal_owner_1),
            ("legal_owner_2",         self.legal_owner_2),
            ("legal_owner_3",         self.legal_owner_3),
            ("legal_owner_4",         self.legal_owner_4),
            ("part_material",         self.part_material),
            ("title",                 self.title),
        ]  # fmt: skip

    def iter_mutable_fields(self) -> Iterator[tuple[str, Any]]:
        yield from [
            # ruff: noqa: E241
            ("date_of_issue",         self.date_of_issue),
            ("revision_index",        self.revision),
            ("sheet_number",          self.page_number),
        ]  # fmt: skip

    @property
    def revision(self) -> str:
        return f"Rev{self._revision}"

    @property
    def page_number(self) -> str:
        return f"{self._page_number} / {self._page_count}"

    @property
    def date_of_issue(self) -> str:
        return self.date.strftime(self._date_format)


class UserMacro:
    TARGET_TYPE_ID = "TechDraw::DrawPage"

    def run(
        self,
        page_data: PageData,
        output_directory: Path,
        revision: str,
        date_format: str | None = None,
    ) -> None:
        objects = Gui.Selection.getSelection() or FreeCAD.activeDocument().Objects
        pages = [obj for obj in objects if obj.TypeId == self.TARGET_TYPE_ID]
        pages = sorted(pages, key=lambda p: p.Label)

        if not pages:
            print("Found no pages to export!")
            return

        print(f"Found {len(pages)} pages to export!")

        if date_format:
            page_data.set_date_format(date_format)
        page_data.set_revision(revision)
        page_data.set_page_count(len(pages))

        self.force_recompute_document()

        self.export_drawings(pages, page_data, output_directory)

        print("Export Complete!")

    def export_drawings(
        self,
        pages: list[DrawPageProxy],
        page_data: PageData,
        output_directory: Path,
    ) -> None:
        output_directory.mkdir(parents=True, exist_ok=True)

        for page_number, page in enumerate(pages, start=1):
            # FreeCAD has a bug where only the active Page is exported. Calling
            # `doubleClicked` activates the Page.
            page.ViewObject.doubleClicked()

            page_data.set_page_field_data(page, page_number)

            path = output_directory / f"{page.Label}.pdf"

            print(f"Exporting '{page.Label}' to {path}...")

            self.export_page(page, path)

            page_data.clear_page_mutable_field_data(page)

    @staticmethod
    def export_page(page: str, path: Path) -> None:
        path = str(path)  # pyright: ignore [reportAssignmentType]

        if hasattr(FreeCADGui, "exportOptions"):
            options = FreeCADGui.exportOptions(path)
            FreeCADGui.export([page], path, options)
        else:
            FreeCADGui.export([page], path)

    @staticmethod
    def force_recompute_document() -> None:
        document = FreeCAD.activeDocument()

        for obj in document.Objects:
            obj.touch()

        document.recompute()


# ---


path_document = Path(FreeCAD.activeDocument().FileName)

output_directory = path_document

macro = UserMacro().run(
    PageDataIso5457(
        approval_person="N/A",
        creator="N/A",
        general_tolerances="N/A",
        language_code="N/A",
        part_material="N/A",
        title="N/A",
    ),
    output_directory,
    revision="N/A",
)
