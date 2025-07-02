import os

import requests

from mediotiempo_data.database_interactions import get_max_values, insert_data
from mediotiempo_data.torneo_regular_resolver import TorneoRegularResolver


def main():

    db_credentials = {
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
        "database": os.environ["DB_DATABASE"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
    }

    row = get_max_values(db_credentials)

    starting_season = row[0] or 2013
    starting_league = row[1] or 385
    starting_round = row[2] or 1

    resolver = TorneoRegularResolver(starting_season, starting_league, starting_round)

    url = "https://www.mediotiempo.com/api/stats"

    query_params = {
        "containerId": "800600",
        "seasonRound": "regular",
    }

    data = []
    for year, league, round in resolver:
        query_params["league"] = league
        query_params["season"] = year
        query_params["round"] = round
        print(f"Fetching data for {year} {league} {round}")

        response = requests.get(url, params=query_params)
        data_ = response.json()

        cess_data = data_["modules"][0]["cessData"]

        if "calendarTop" in cess_data:
            configuration = cess_data["configuration"]
            for match in cess_data["calendarTop"]:
                data.append(
                    (
                        year,
                        league,
                        round,
                        configuration["leagueId"],
                        configuration["leagueName"],
                        configuration["leagueLabel"],
                        configuration["leagueImage"],
                        configuration["seasonId"],
                        configuration["seasonName"],
                        configuration["seasonLabel"],
                        configuration["seasonRoundId"],
                        configuration["seasonRoundName"],
                        configuration["seasonRoundLabel"],
                        configuration["roundId"],
                        configuration["roundName"],
                        configuration["roundLabel"],
                        match["id"],
                        match["date"],
                        match["homeTeam"]["id"],
                        match["homeTeam"]["name"],
                        match["homeTeam"]["logo"],
                        match["homeTeam"]["logoLarge"],
                        match["awayTeam"]["id"],
                        match["awayTeam"]["name"],
                        match["awayTeam"]["logo"],
                        match["awayTeam"]["logoLarge"],
                        match["status"]["type"],
                        match["scores"]["homeTeam"],
                        match["scores"]["homeShootOut"],
                        match["scores"]["awayTeam"],
                        match["scores"]["awayShootOut"],
                        match["venue"]["id"],
                        match["venue"]["stadium"],
                        match["venue"]["city"],
                    )
                )
        else:
            print(f"No calendarTop for {year} {league} {round}")

    insert_data(db_credentials, data)
