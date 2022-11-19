`export PYTHONPATH=/local/path/to/this/repo`

```
cd this/repo
export PYTHONPATH=$(pwd)
```

pre-commit:
- `black .`
- `flake8 .`

Docker build and run locally: `docker-compose -f docker-compose.build-local.yml up --build`

Run core without docker:
- deploy database
- `. ./env/bin/activate`
- `python core/application.py`