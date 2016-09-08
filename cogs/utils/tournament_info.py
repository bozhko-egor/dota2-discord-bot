from .parser import *


def get_schedule(*league_ids):
    games = get_upcoming_matches()
    live = []
    upcoming = []
    reply = ''
    for game in games:
        if int(game['timediff']) < 0:
            live.append(game)
        else:
            upcoming.append(game)

    if live:
        reply = "**Live games:** \n"
        for game in live:
            reply += "{0} - (Bo{3}: {4} - {5}) **{1}** vs **{2}** \n".format(
                game['league']['name'],
                game['team1']['team_name'],
                game['team2']['team_name'],
                game['series_type'],
                game['team1']['score'],
                game['team2']['score']
                )
    reply += "\n**Upcoming:** \n"
    for game in upcoming:
        h, m = divmod(int(game['timediff']), 3600)
        reply += "{0} - (Bo{3}) **{1}** vs **{2}** ({4}hr{5}min from now) \n".format(
            game['league']['name'],
            game['team1']['team_name'],
            game['team2']['team_name'],
            game['series_type'],
            h,
            int(m/60)
            )
    return reply
