# Development guide

## Windows PowerShell commands

Activate virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Run API:

```powershell
uvicorn app.main:app --reload
```

Run tests:

```powershell
pytest
```

Run lint:

```powershell
ruff check .
```

Run format:

```powershell
ruff format .
```

## Makefile commands

If make is available:

```powershell
make run
make test
make lint
make format
make check
```