WITH teams AS (
    SELECT DISTINCT home_team_id AS team_id, home_team_name AS team_name 
    FROM {{ source('futbol_db', 'landing_mediotiempo_torneo_regular') }}
    UNION
    SELECT DISTINCT away_team_id AS team_id, away_team_name AS team_name 
    FROM {{ source('futbol_db', 'landing_mediotiempo_torneo_regular') }}
)
SELECT *
FROM teams
