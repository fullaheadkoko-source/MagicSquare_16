"""Official GUI entry point.

Run:
    python -m magicsquare
"""

def main() -> None:
    try:
        from magicsquare.screen.app import run
    except ModuleNotFoundError as exc:
        if exc.name != "PyQt6":
            raise
        raise SystemExit(
            'PyQt6 is not installed. Run: python -m pip install -e ".[gui]"'
        ) from exc
    run()


if __name__ == "__main__":
    main()

