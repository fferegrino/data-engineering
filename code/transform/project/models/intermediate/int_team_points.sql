WITH results_home_team AS (
  SELECT
    season_id,
    league_id,
    round_id,
    match_id,
    home_team_id AS team_id,
    date,
    CASE
      WHEN home_team_score = away_team_score THEN 1
      WHEN home_team_score > away_team_score THEN 3
      WHEN home_team_score < away_team_score THEN 0
      ELSE -1
    END AS points
  FROM {{ ref('stg_scores') }}
), results_away_team AS (
  SELECT 
    season_id,
    league_id,
    round_id,
    match_id,
    away_team_id AS team_id,
    date,
    CASE
      WHEN away_team_score = home_team_score THEN 1
      WHEN away_team_score > home_team_score THEN 3
      WHEN away_team_score < home_team_score THEN 0
      ELSE -1
    END AS points
  FROM {{ ref('stg_scores') }}
), all_points AS (
  SELECT
    season_id,
    league_id,
    round_id, match_id, team_id, date, points
  FROM results_home_team
  UNION
  SELECT
    season_id,
    league_id,
    round_id, match_id, team_id, date, points
  FROM results_away_team
)
SELECT 
    season_id,
    league_id,
    round_id,
    team_id,
    date,
    points
FROM all_points AS points_table
ORDER BY date DESC
