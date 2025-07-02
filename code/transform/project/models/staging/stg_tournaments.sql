SELECT DISTINCT season_id, league_id, season_name, league_name, league_label
FROM {{ source('futbol_db', 'landing_mediotiempo_torneo_regular') }}
