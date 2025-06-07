# Contributing to ConfigLoader

Thank you for your interest in contributing to ConfigLoader! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository:

```bash
git clone https://github.com/CubeVic/configuration_loader.git
cd configuration_loader
```

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install development dependencies:

```bash
pip install -e ".[dev]"
```

## Code Style

ConfigLoader follows these code style guidelines:

- Follow [PEP 8](https://peps.python.org/pep-0008/) for code style
- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Use type hints for all function arguments and return values
- Keep functions small and focused
- Write clear and descriptive variable names

## Running Tests

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=configloader
```

## Adding New Features

1. Create a new branch:

```bash
git checkout -b feature/your-feature-name
```

1. Make your changes
2. Add tests for your changes
3. Update documentation
4. Run tests and ensure they pass
5. Submit a pull request

## Writing Tests

- Write tests for all new features
- Include both positive and negative test cases
- Use descriptive test names
- Follow the `test_` prefix convention
- Use pytest fixtures when appropriate

Example test:

```python
def test_load_config_from_file():
    loader = ConfigLoader(config_file_name="test_config.yaml")
    config = loader.load_config()
    assert config["name"] == "test"
```

## Documentation

- Update documentation for all new features
- Include examples in docstrings
- Update the README if necessary
- Add new documentation files if needed

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add a clear description of your changes
4. Reference any related issues
5. Wait for review and address any feedback

## Code Review

All contributions require review before merging. Reviewers will check:

- Code style and quality
- Test coverage
- Documentation
- Performance impact
- Backward compatibility

## Reporting Issues

When reporting issues, please include:

- Python version
- ConfigLoader version
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs

## Development Tools

We use several tools to maintain code quality:

- `black` for code formatting
- `ruff` for linting
- `mypy` for type checking
- `pytest` for testing
- `pre-commit` for git hooks

## Release Process

1. Update version in `pyproject.toml`
2. Update changelog
3. Create a release tag
4. Build and publish to PyPI

## License

By contributing to ConfigLoader, you agree that your contributions will be licensed under the project's license.

## Questions?

Feel free to open an issue for any questions about contributing.
