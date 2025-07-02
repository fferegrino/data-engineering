select
    year,
    season_id,
    league_id,
    round_id,
    date::timestamp as date,
    match_id,
    home_team_id,
    home_team_score,
    away_team_id,
    away_team_score
from {{ source('futbol_db', 'landing_mediotiempo_torneo_regular') }}
where status_type = 'finished'
