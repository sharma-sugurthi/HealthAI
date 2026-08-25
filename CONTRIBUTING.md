# Contributing to Susruta

We adhere to strict engineering standards to maintain the stability and security of the Susruta platform. Please review these guidelines before submitting a pull request.

## Development Workflow

1. Branch from `main` using the format `feature/your-feature`, `bugfix/issue-description`, or `refactor/component`.
2. Ensure your local environment is configured using `.venv` and `requirements-dev.txt`.
3. Write clean, self-documenting code.
4. Add unit and integration tests for all new functionality.

## Code Quality Standards

We enforce automated formatting and static analysis in our CI pipeline. Code that fails these checks will not be merged.

Prior to committing, run the following checks:

```bash
# Code Formatting (Black)
black --check .

# Import Sorting (isort)
isort --check-only .

# Linting (Flake8)
flake8 backend/ api/ tests/

# Type Checking (Mypy)
mypy backend/ api/
```

We recommend configuring `pre-commit` hooks to automate this workflow.

## Testing Strategy

We utilize `pytest` for all testing. Our test suite covers unit tests for domain models, repository behavior, and service logic, as well as integration tests for API endpoints.

To run the test suite:

```bash
source .venv/bin/activate
pytest tests/ -v
```

### Mocking and External Services

- Do not perform real network calls to AI providers in the test suite. Utilize dependency injection or standard mocking frameworks to simulate AI responses.
- Database tests utilize an in-memory SQLite database to ensure fast, isolated test execution without side effects.

## Architectural Guidelines

- **API Layer (`api/`)**: Routers should be thin. They handle HTTP concerns, request/response validation, and dependency injection. Business logic must be deferred to the service layer.
- **Service Layer (`backend/services/`)**: Contains the core domain logic. Services orchestrate data flow between repositories and external clients (like AI providers).
- **Data Access (`backend/repositories/`)**: All database operations must be encapsulated within repository classes. Do not execute raw queries from routers or services.

By strictly adhering to these boundaries, we ensure the system remains testable, decoupled, and maintainable as complexity grows.
