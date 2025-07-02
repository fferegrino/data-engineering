# Mediotiempo Data Extractor

A Python-based data extraction and loading tool designed to collect football (soccer) match data from Mediotiempo's API and store it in a PostgreSQL database.

This project is part of a larger data engineering pipeline for sports analytics.

## 🎯 Purpose

This extractor is specifically designed to:

- Fetch regular tournament match data from Mediotiempo's public API
- Handle incremental data extraction by tracking the last processed season, league, and round

## 🛠️ Technologies Used

### Core Technologies

- **Python 3.11+** - Primary programming language
- **PostgreSQL** - Target database for data storage
- **psycopg2-binary** - PostgreSQL adapter for Python
- **requests** - HTTP library for API interactions

## 📦 Project Structure

```text
src/
├── mediotiempo_data/
│   ├── __init__.py          # Main application entry point
│   ├── database_interactions.py  # PostgreSQL connection and operations
│   └── torneo_regular_resolver.py # Tournament progression logic
├── tests/                   # Test suite
├── Dockerfile              # Container configuration
├── pyproject.toml          # Project metadata and dependencies
└── uv.lock                 # Locked dependency versions
```

## 🔧 Key Components

### 1. Main Application (`__init__.py`)

- Orchestrates the data extraction process
- Manages database connections and API requests
- Handles data transformation and insertion

### 2. Database Interactions (`database_interactions.py`)

- **`get_max_values()`** - Retrieves the last processed season, league, and round
- **`insert_data()`** - Bulk inserts match data into the landing table

### 3. Tournament Resolver (`torneo_regular_resolver.py`)

- Manages tournament progression logic
- Handles season transitions (Clausura → Apertura → next year)
- Supports leagues 385 (Clausura) and 199 (Apertura)

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Docker (optional, for containerized deployment)

### Environment Variables

The application requires the following environment variables:

```bash
DB_HOST=your_postgres_host
DB_PORT=your_postgres_port
DB_DATABASE=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## 📊 Data Schema

The extractor populates the `landing_mediotiempo_torneo_regular` table with the following structure:

| Field | Description |
|-------|-------------|
| season_id | Tournament year |
| league_id | League identifier (385=Clausura, 199=Apertura) |
| round_id | Round number within the tournament |
| league_id_config | League ID from API configuration |
| league_name | League name |
| league_label | League display label |
| league_image | League logo URL |
| season_id_config | Season ID from API configuration |
| season_name | Season name |
| season_label | Season display label |
| season_round_id | Season round ID |
| season_round_name | Season round name |
| season_round_label | Season round display label |
| round_id_config | Round ID from API configuration |
| round_name | Round name |
| round_label | Round display label |
| match_id | Unique match identifier |
| match_date | Match date and time |
| home_team_id | Home team ID |
| home_team_name | Home team name |
| home_team_logo | Home team logo URL |
| home_team_logo_large | Home team large logo URL |
| away_team_id | Away team ID |
| away_team_name | Away team name |
| away_team_logo | Away team logo URL |
| away_team_logo_large | Away team large logo URL |
| match_status | Match status (e.g., "finished", "scheduled") |
| home_score | Home team score |
| home_shootout | Home team shootout score (if applicable) |
| away_score | Away team score |
| away_shootout | Away team shootout score (if applicable) |
| venue_id | Stadium ID |
| venue_stadium | Stadium name |
| venue_city | Stadium city |

## 🔄 Incremental Processing

The application implements smart incremental processing:

1. Queries the database to find the last processed season, league, and round
2. Starts extraction from the next logical point in the tournament progression
3. Continues until reaching the maximum season (2025) or no more data is available
4. Handles tournament transitions automatically (Clausura → Apertura → next year)

## 🧪 Testing

Run the test suite:

```bash
uv run pytest tests/
```
