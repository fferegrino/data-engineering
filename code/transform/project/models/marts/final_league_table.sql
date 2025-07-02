WITH points_table AS (
  SELECT
    season_id,
    league_id,
    team_id,
    sum(points) AS points
  FROM {{ ref('int_team_points') }} AS points_table
  GROUP BY
    season_id,
    league_id,
    team_id
)
SELECT
  tournaments.season_id,
  tournaments.season_name,
  tournaments.league_id,
  tournaments.league_label,
  teams.team_id,
  teams.team_name,
  points
FROM points_table
  INNER JOIN {{ ref('stg_tournaments') }} AS tournaments
    ON tournaments.season_id = points_table.season_id AND
      tournaments.league_id = points_table.league_id
  INNER JOIN {{ ref('stg_teams') }} AS teams
    ON points_table.team_id = teams.team_id
ORDER BY
  points_table.season_id,
  points_table.league_id DESC,
  points DESC
