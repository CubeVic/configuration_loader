"""Main CLI application module."""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        from configloader import __version__
        console.print(f"configloader version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """A flexible configuration loader with CLI support."""
    pass
