export PYTHONPATH=/local/path/to/this/repo

pre-commit:
- black .
- flake8 .