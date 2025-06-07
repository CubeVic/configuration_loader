# Installation

ConfigLoader can be installed using pip or Poetry.

## Using pip

```bash
pip install configloader
```

## Using Poetry

```bash
poetry add configloader
```

## Dependencies

ConfigLoader has the following dependencies:

- `pydantic`: For configuration validation
- `pyyaml`: For YAML file support
- `tomli`: For TOML file support (Python < 3.11)
- `tomllib`: For TOML file support (Python >= 3.11)

These dependencies will be automatically installed when you install ConfigLoader.

## Development Installation

If you want to install ConfigLoader for development:

1. Clone the repository:

```bash
git clone https://github.com/CubeVic/configuration_loader.git
cd configuration_loader
```

2. Install with pip in editable mode:

```bash
pip install -e .
```

3. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Requirements

- Python 3.8 or higher
- pip or Poetry for package management

## Optional Dependencies

Some features require additional dependencies:

- `pydantic[email]`: For email validation in Pydantic models
- `pydantic[ujson]`: For faster JSON parsing
- `pydantic[python-dotenv]`: For .env file support

You can install these optional dependencies using pip:

```bash
pip install "configloader[email,ujson,dotenv]"
```

Or with Poetry:

```bash
poetry add "configloader[email,ujson,dotenv]"
```
