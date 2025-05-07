# Contributing to Domain-SC

Thank you for your interest in contributing to Domain-SC! This document outlines the process and standards for contributing to the project.

## Code Standards

- Follow PEP 8 style guidelines
- Use type annotations for all functions and methods
- Write docstrings for all modules, classes, and functions
- Keep functions focused on a single responsibility
- Maximum line length is 100 characters

## Commit Standards

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Changes that do not affect code execution (formatting, etc.)
- `refactor:` - Code changes that neither fix bugs nor add features
- `perf:` - Performance improvements
- `test:` - Adding or correcting tests
- `chore:` - Changes to build process, tools, etc.

Example: `feat: add smart model selection to LLM service`

## Pull Request Process

1. Ensure your code follows the standards defined above
2. Update documentation to reflect any changes
3. Include tests that validate your changes
4. Wait for code review and address any feedback

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install development dependencies: `pip install -r requirements-dev.txt`
5. Install pre-commit hooks: `pre-commit install`

## Testing

- Run all tests: `pytest`
- Check test coverage: `pytest --cov=src`
- Aim for at least 80% test coverage for new code

## Documentation

- Update documentation for any new features or changes
- Run documentation build to ensure correct formatting: `mkdocs build`