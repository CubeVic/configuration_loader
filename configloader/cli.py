import importlib
import json
import logging
from pathlib import Path
import sys
from typing import Optional
from pydantic import BaseModel
import toml
import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
import yaml

from configloader.core import ConfigLoader
from configloader.exceptions import ConfigFileError, ConfigParserError, ConfigSourceError, ConfigValidationError

app = typer.Typer(
    name="configloader",
    help="A CLI for loading and validating configuration files.",
    add_completion=True
)

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True)])


logger = logging.getLogger("configLoader")


def import_model(model_path: Path) -> Type[BaseModel]:
    """Import the model from the given path."""
    model_class = None
    try:
        model_path, class_name = model_path.rsplit(".", 1)
        module = importlib.import_module(model_path)
        model_class = getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to import model from {model_path}: {e}")
    return model_class

def format_config(config: BaseModel, format: str) -> str:
    """Format the configuration in the given format."""
    if format == "json":
        return json.dumps(config, indent=4)
    elif format == "yaml":
        return yaml.dump(config, indent=4, default_flow_style=False)
    elif format == "toml":
        return toml.dumps(config)
    else:
        raise ValueError(f"Invalid format: {format}")


def display_config(config: BaseModel, format: str) -> None:
    """Display the configuration in the given format."""
    formatted_config = format_config(config, format=format)

    table = Table(title="Configuration", show_header=True, header_style="bold")
    table.add_column("Format", style="cyan")
    table.add_column("Description", style="yellow")

    table.add_row(format.upper(), formatted_config)
    console.print(Panel(table, title="Configuration", border_style="blue"))


@app.command()
def load(
        config_file: Optional[Path] = typer.Option(None, "--config-file", "-c", help="Path to the configuration file to load", exists=True, file_okay=True, dir_okay=False,),
        config_name: str = typer.Option(),
        env_prefix: str = typer.Option(),
        format: str = typer.Option(),
        validate: bool = typer.Option(),
        model_path: Optional[Path] = typer.Option(),
        debug: bool = typer.Option(),) -> None:

    if debug:
        logger.setLevel(logging.DEBUG)

    try:
        config_model = None
        if validate and model_path:
            config_model = import_model(model_path=model_path)
            console.print(f"[green]Validating configuration against model: {model_path} [/green]")

            loader = ConfigLoader(
                config_file=config_file,
                config_name=config_name,
                env_prefix=env_prefix,
                config_model=config_model,
            )

            config = loader.load()

            display_config(config, format)

            if validate and config_model:
                console.print(f"[green]Configuration validated successfully[/green]")
                console.print(f"[green]Configuration: {config}[/green]")

    except (ConfigFileError, ConfigParserError, ConfigSourceError, ConfigValidationError) as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error occurred")
        sys.exit(1)