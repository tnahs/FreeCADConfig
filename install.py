# ------------------------------------------------------------------------------
#
#    See README.md for installation instructions.
#
# ------------------------------------------------------------------------------

import shutil
import subprocess
import tomllib
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

import FreeCAD
import FreeCADGui
from FreeCADGui import Command
from PySide import QtWidgets


NAME = "FreeCADConfig"
NAME_TOOLBAR = f"Custom_{NAME}"

NAME_ADDONS_TOML = "addons.toml"
NAME_MACROS_TOML = "macros.toml"
NAME_PREFERENCES_TOML = "preferences.toml"
NAME_SHORTCUTS_TOML = "shortcuts.toml"

SUBPATH_SRC = Path() / "src"
SUBPATH_CONFIG = SUBPATH_SRC / "config"
SUBPATH_ICONS = SUBPATH_SRC / "icons"
SUBPATH_MACROS = SUBPATH_SRC / "macros"
SUBPATH_ADDONS_TOML = SUBPATH_CONFIG / NAME_ADDONS_TOML
SUBPATH_MACROS_TOML = SUBPATH_CONFIG / NAME_MACROS_TOML
SUBPATH_PREFERENCES_TOML = SUBPATH_CONFIG / NAME_PREFERENCES_TOML
SUBPATH_SHORTCUTS_TOML = SUBPATH_CONFIG / NAME_SHORTCUTS_TOML

ICON_MACRO_DEFAULT = "freecad.svg"

P_ROOT = Path("User parameter:")
P_SUBPATH_MACROPATH = Path() / "BaseApp" / "Preferences" / "Macro" / "MacroPath"
P_SUBPATH_MACROS = Path() / "BaseApp" / "Macro" / "Macros"
P_SUBPATH_SHORTCUTS = Path() / "BaseApp" / "Preferences" / "Shortcut"
P_SUBPATH_TOOLBAR = Path() / "BaseApp" / "Workbench" / "Global" / "Toolbar"


T = TypeVar("T")


class Config:
    @classmethod
    def fields(cls) -> set[str]:
        return set(cls.__annotations__.keys())


@dataclass
class Addon(Config):
    name: str
    url: str


@dataclass
class Macro(Config):
    file: str
    name: str
    tooltip: str
    icon: str | Path
    shortcut: str

    def as_command(self) -> dict:
        return {
            "macroFile": self.file,
            "menuText": self.name,
            "toolTip": self.tooltip,
            "pixmap": str(self.icon),
            "shortcut": self.shortcut,
        }


@dataclass
class Preference(Config):
    # The path or paths to set.
    path: str | list[str]
    value: Any


@dataclass
class Shortcut(Config):
    command: str
    shortcut: str


# Install Functions


def install_addons(path_config_root: Path | str, reinstall: bool = False) -> None:
    path_config_root = Path(path_config_root).expanduser()

    path_freecad_addons = Path(FreeCAD.getUserAppDataDir()) / "Mod"
    path_freecad_addons.mkdir(exist_ok=True, parents=True)

    addons_config = load_config(
        path_config_root / SUBPATH_ADDONS_TOML,
        model=Addon,
    )

    for addon in addons_config:
        print(f"Installing {addon.name}…")

        addon_directory = path_freecad_addons / addon.name

        if reinstall is True:
            shutil.rmtree(addon_directory)

        addon_directory.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "git",
                "clone",
                addon.url,
                ".",
            ],
            cwd=addon_directory,
            check=True,
        )


def install_macros(path_config_root: Path | str) -> None:
    path_config_root = Path(path_config_root).expanduser()
    path_macro_src = path_config_root / SUBPATH_MACROS

    macros_config = load_config(
        path_config_root / SUBPATH_MACROS_TOML,
        model=Macro,
    )

    # Cache the generator so we can use it twice.
    macros_config = list(macros_config)

    missing_src_files = [
        entry.file
        for entry in macros_config
        if not (path_macro_src / entry.file).exists()
    ]

    if missing_src_files:
        print("Aborted! Missing source macro files:")
        for file in missing_src_files:
            print(f" {file}")
        return

    # Set the path to the macors source.
    set_preference(P_SUBPATH_MACROPATH, str(path_macro_src))

    print(" Removing old toolbar…")
    toolbar_global = FreeCAD.ParamGet(str(P_ROOT / P_SUBPATH_TOOLBAR))
    toolbar_global.RemGroup(NAME_TOOLBAR)

    print(f" Building {NAME} toolbar…")
    toolbar_fcm = toolbar_global.GetGroup(NAME_TOOLBAR)
    toolbar_fcm.SetString("Name", NAME)
    toolbar_fcm.SetBool("Active", True)

    for macro in macros_config:
        print(f"\nRegistering '{macro.name}'…")

        command: str = Command.findCustomCommand(macro.file)

        if command:
            print(" Removing old version…")
            Command.removeCustomCommand(command)

        macro.icon = str(
            path_config_root / SUBPATH_ICONS / (macro.icon or ICON_MACRO_DEFAULT)
        )

        command = Command.createCustomCommand(**macro.as_command())

        group = FreeCAD.ParamGet(str(P_ROOT / P_SUBPATH_MACROS))
        group = group.GetGroup(command)
        group.SetString("Script", macro.file)
        group.SetString("Menu", macro.name)
        group.SetString("Pixmap", macro.icon)
        group.SetString("Accel", macro.shortcut)
        group.SetString("Tooltip", macro.tooltip)
        group.SetString("Statustip", "")
        group.SetString("WhatsThis", "")
        group.SetBool("System", False)

        print(" Setting shorcut…")
        set_shortcut(command, macro.shortcut)

        print(" Adding to toolbar…")
        toolbar_fcm.SetString(command, macro.name)

    FreeCADGui.activeWorkbench().reloadActive()


def install_preferences(path_config_root: Path | str) -> None:
    path_config_root = Path(path_config_root).expanduser()

    preferences_config = load_config(
        path_config_root / SUBPATH_PREFERENCES_TOML,
        model=Preference,
    )

    for preference in preferences_config:
        if isinstance(preference.path, list):
            set_preferences(
                preference.path,
                preference.value,
            )
            continue

        set_preference(
            preference.path,
            preference.value,
        )


def install_shortcuts(path_config_root: Path | str) -> None:
    path_config_root = Path(path_config_root).expanduser()

    shortcuts_config = load_config(
        path_config_root / SUBPATH_SHORTCUTS_TOML,
        model=Shortcut,
    )

    for shortcut in shortcuts_config:
        set_shortcut(
            shortcut.command,
            shortcut.shortcut,
        )


# Set Functions


def set_shortcut(command: str, shortcut: str) -> None:
    shortcuts = FreeCAD.ParamGet(str(P_ROOT / P_SUBPATH_SHORTCUTS))
    shortcuts.SetString(command, shortcut)


def set_preferences(subpaths: list[Path] | list[str], value: Any) -> None:
    for subpath in subpaths:
        set_preference(subpath, value)


def set_preference(subpath: Path | str, value: Any) -> None:
    subpath = Path(subpath)

    preference = FreeCAD.ParamGet(str(P_ROOT / subpath.parent))

    if type(value) is bool:
        preference.SetBool(subpath.name, value)
    if type(value) is int:
        if value > 100_000:
            preference.SetUnsigned(subpath.name, value)
        else:
            preference.SetInt(subpath.name, value)
    if type(value) is float:
        preference.SetFloat(subpath.name, value)
    if type(value) is str:
        preference.SetString(subpath.name, value)
    if type(value) is list:
        preference.SetString(subpath.name, f"{','.join(value)},")


# Utils


def load_toml(file: Path) -> dict:
    with file.open(mode="rb") as f:
        return tomllib.load(f)


def load_config(path: Path, model: type[T]) -> Iterator[T]:
    data = load_toml(path)

    # Cache the manifest items.
    items = next(iter(data.values()))

    # Run a rough validataion.
    for item in items:
        if set(item.keys()) != model.fields():  # pyright: ignore [reportAttributeAccessIssue]
            raise RuntimeError(
                f"Encountered invalid fields for {model.__name__}.\n{item}"
            )

    for item in items:
        yield model(**item)


# Installation -----------------------------------------------------------------


def validate_path_exists(path: Path | str, make: bool = False) -> Path:
    if not path:
        raise ValueError("No path defined.")

    path = Path(path).expanduser().resolve()

    if make is True:
        path.mkdir(exist_ok=True, parents=True)

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist {path}.")

    return path


def show_dialog(message: str) -> None:
    dialog = QtWidgets.QMessageBox()
    dialog.setIcon(QtWidgets.QMessageBox.Warning)
    dialog.setText(message)
    dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
    dialog.exec()


def run_install_addons(
    path_config_root: Path | str,
    reinstall: bool,
) -> None:
    path = validate_path_exists(path_config_root)

    install_addons(path, reinstall)

    show_dialog(message="Add-on instalation complete!\nPlease restart FreeCAD.")


def run_install_configs(path_config_root: Path | str) -> None:
    path = validate_path_exists(path_config_root)

    install_macros(path)
    install_shortcuts(path)
    install_preferences(path)

    show_dialog(message="Config instalation complete!\nPlease restart FreeCAD.")


# ------------------------------------------------------------------------------
#
#    See README.md for installation instructions.
#
# ------------------------------------------------------------------------------


PATH_CONFIG_ROOT = "~/Projects/100-active/FreeCADConfig"

# run_install_addons(PATH_CONFIG_ROOT, reinstall=False)
# run_install_configs(PATH_CONFIG_ROOT)
