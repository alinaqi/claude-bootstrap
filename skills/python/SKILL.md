---
name: python
description: Python development with ruff, mypy, pytest - TDD and type safety
---

# Python Skill

*Load with: base.md*

---

## Type Hints

- Use type hints on all function signatures
- Use `typing` module for complex types
- Run `mypy --strict` in CI

```python
def process_user(user_id: int, options: dict[str, Any] | None = None) -> User:
    ...
```

---

## Project Structure

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── core/           # Pure business logic
│       │   ├── __init__.py
│       │   ├── models.py   # Pydantic models / dataclasses
│       │   └── services.py # Pure functions
│       ├── infra/          # Side effects
│       │   ├── __init__.py
│       │   ├── api.py      # FastAPI routes
│       │   └── db.py       # Database operations
│       └── utils/          # Shared utilities
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── CLAUDE.md
```

---

## Tooling (Required)

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing --cov-fail-under=80"
```

---

## Testing with Pytest

```python
# tests/unit/test_services.py
import pytest
from package_name.core.services import calculate_total

class TestCalculateTotal:
    def test_returns_sum_of_items(self):
        # Arrange
        items = [{"price": 10}, {"price": 20}]
        
        # Act
        result = calculate_total(items)
        
        # Assert
        assert result == 30

    def test_returns_zero_for_empty_list(self):
        assert calculate_total([]) == 0

    def test_raises_on_invalid_item(self):
        with pytest.raises(ValueError):
            calculate_total([{"invalid": "item"}])
```

---

## GitHub Actions

```yaml
name: Python Quality Gate

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          
      - name: Lint (Ruff)
        run: ruff check .
        
      - name: Format Check (Ruff)
        run: ruff format --check .
        
      - name: Type Check (mypy)
        run: mypy src/
        
      - name: Test with Coverage
        run: pytest
```

---

## Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic]
        args: [--strict]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit -x --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

Install and setup:
```bash
pip install pre-commit
pre-commit install
```

---

## Patterns

### Pydantic for Data Validation
```python
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    email: str = Field(..., min_length=5)
    name: str = Field(..., max_length=100)
```

### Dependency Injection
```python
# Don't import dependencies directly in business logic
# Pass them in

# Bad
from .db import database
def get_user(user_id: int) -> User:
    return database.fetch(user_id)

# Good
def get_user(user_id: int, db: Database) -> User:
    return db.fetch(user_id)
```

### Result Pattern (No Exceptions in Core)
```python
from dataclasses import dataclass

@dataclass
class Result[T]:
    value: T | None
    error: str | None
    
    @property
    def is_ok(self) -> bool:
        return self.error is None
```

---

## Python Anti-Patterns

- ❌ `from module import *`
- ❌ Mutable default arguments
- ❌ Bare `except:` clauses
- ❌ Using `type: ignore` without explanation
- ❌ Global variables for state
- ❌ Classes when functions suffice
