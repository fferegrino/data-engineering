import psycopg2


def get_max_values(db_credentials: dict):
    conn = psycopg2.connect(**db_credentials)
    cursor = conn.cursor()

    cursor.execute(
        f"""
    WITH max_season AS (
    SELECT MAX(season_id) AS season_id
    FROM landing_mediotiempo_torneo_regular
    ),
    min_league AS (
    SELECT MIN(league_id) AS league_id
    FROM landing_mediotiempo_torneo_regular
    WHERE season_id = (SELECT season_id FROM max_season)
    ),
    max_round AS (
    SELECT MAX(round_id) AS round_id
    FROM landing_mediotiempo_torneo_regular
    WHERE season_id = (SELECT season_id FROM max_season)
        AND league_id = (SELECT league_id FROM min_league)
    )
    SELECT 
    (SELECT season_id FROM max_season) AS season_id,
    (SELECT league_id FROM min_league) AS league_id,
    (SELECT round_id FROM max_round) AS round_id;
        """
    )

    row = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return row


def insert_data(db_credentials: dict, data: list):
    conn = psycopg2.connect(**db_credentials)
    cursor = conn.cursor()

    if len(data) == 0:
        return

    elements_to_insert = len(data[0])
    params_str = ", ".join(["%s"] * elements_to_insert)

    for entry in data:
        cursor.execute(
            f"""
        INSERT INTO landing_mediotiempo_torneo_regular
        VALUES ({params_str})
        """,
            entry,
        )

    conn.commit()
    cursor.close()
