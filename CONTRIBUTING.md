# Contributing to LitPrinter

Thank you for considering contributing to LitPrinter! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/litprinter.git
   cd litprinter
   ```

2. Create a virtual environment and install development dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## Running Tests

```
pytest
```

## Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking
- flake8 for linting

You can run all of these tools with:

```
black src tests
isort src tests
mypy src
flake8 src tests
```

## Submitting Changes

1. Push your changes to your fork
2. Submit a pull request to the main repository
3. Describe your changes in detail
4. Link any relevant issues

## Reporting Bugs

When reporting bugs, please include:
- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (Python version, OS, etc.)

## Feature Requests

Feature requests are welcome! Please provide:
- A clear description of the feature
- Why it would be useful
- Any implementation ideas you have

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Questions?

If you have any questions, feel free to open an issue or reach out to the maintainers.
