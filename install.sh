#!/usr/bin/env zsh


# shellcheck disable=2296
NAME=$(basename "${(%):-%N}")

ROOT=$(pwd)


function install_macos {
    local target="$HOME/Library/Application Support/FreeCAD/Macro"

    # If the target directory exists, rename it.
    if [ -d "$target" ]; then
        mv "$target" "$target.bak"
    fi

    ln -sihv "$ROOT/src" "$target"
}


function install_linux {
    echo "Auto Linux installation is not currently supported."
    echo "Please submit a ticket to help establish this."
}


function install_windows {
    echo "Auto Windows installation is not currently supported."
    echo "Please submit a ticket to help establish this."
}


function print_help {
    echo -e "Install (symlink) FreeCAD macros.

\e[4mUsage:\e[0m ${NAME} [OPTIONS] <PLATFORM>

\e[4mPlatforms:\e[0m
  macos    Install for macOS
  linux    Install for Linux (currently unsupported)
  windows  Install for Window (currently unsupported)

\e[4mOptions:\e[0m
  -h, --help   Show help"
}


function main {

    if [[ "$1" == "--help" || "$1" == "-h" ]]; then
        print_help
        exit 0
    fi

    if [[ $# -ne 1 ]]; then
        echo "Error: missing required positional argument 'platform'"
        print_help
        exit 1
    fi

    case "$1" in
        "macos")
            install_macos
            ;;
        "linux")
            install_linux
            ;;
        "windows")
            install_windows
            ;;
        *)
            echo "Error: invalid platform '$1'"
            print_help
            exit 1
            ;;
    esac
}


main "$@"
