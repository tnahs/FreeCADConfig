# FreeCADConfig

## Installation

Installation is done in two basic steps (1) install add-ons (2) install macros, preferences,
shorcuts. This is all done using the `install.py` script. Some of the commands used require that
FreeCAD's GUI is loaded so we'll have to paste the contents of the script in FreeCAD's Python
console.

1. Set the `PATH_CONFIG_ROOT` variable to the root directory of this repo.

```python
PATH_CONFIG_ROOT = "path/to/FreeCADConfig"
```

2. Start FreeCAD and open `Tools` > `Panels` > `Python console`.

3. Un-comment the following line and copy/paste the contents of the file. This will run a `git
clone` on all the add-ons defined in [`addons.toml`][addons] file.

```python
run_install_addons(PATH_CONFIG_ROOT, reinstall=False)
```

4. Restart FreeCAD

5. In `Preferences` > `General`, set the theme to `OpenDark`.

6. Restart FreeCAD

7. Un-comment the following line and copy/paste the contents of the file. This will
   install the macros, shortcuts and preferences defined in [`macros.toml`][macros],
   [`shortcuts.toml`][shortcuts] and [`preferences.toml`][preferences] files.

```python
run_install_configs(PATH_CONFIG_ROOT)
```

[addons]: ./src/config/addons.toml
[macros]: ./src/config/macros.toml
[shortcuts]: ./src/config/shortcuts.toml
[preferences]: ./src/config/preferences.toml
