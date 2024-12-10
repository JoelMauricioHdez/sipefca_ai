# SIPEFCA Forecasting Service

## Getting Started

### Prerequisites
- Python 3.10
- Pip
- Poetry
- PostgreSQL
- Docker
- Docker Compose
- Git
- [GitHub CLI](https://cli.github.com/)
- [GitHub Actions](https://github.com/features/actions)

### Installation
1. Clone the repository
```bash
git clone https://github.com/joelhernandez/sipefca_ai.git
```
2. Install the dependencies
```bash
poetry install
```
3. Create a `.env` file in the root directory of the project with the following content:
```bash
HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_KEY=postgres
```