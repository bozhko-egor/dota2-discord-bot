import cv2
from PIL import ImageFont, ImageDraw
from PIL import Image
import datetime
from token_and_api_key import *
from .resources import db
from .hero_dictionary import *
from random import randint
from opendota_api.matches import Match


def length_check(name, font):
    global draw
    n = 0
    length, _ = draw.textsize(name, font=font)
    while length > 133:
        name = name[:-1]
        length, _ = draw.textsize(name, font=font)
        n += 1
    if n:
        name += "..."
        length, _ = draw.textsize(name, font=font)
    center = length//2

    return 128-center, name

def fill_template(hero, item, team, match):
    global template, draw
    x, y = hero
    x1, y1 = item
    for k in range(5):
        player = match['players'][k + team * 5]
        hero_name = hero_dic[player['hero_id']]

        hero = cv2.imread('images/heroes/{} icon.png'.format(hero_name.lower()), -1)
        roi = template[
            y + k * 36: y + 32 + k * 36,
            x: x + 32]
        for i in range(32):
            for j in range(32):
                if hero[i, j][3] == 255:
                    roi[i, j] = hero[i, j]
        template[y + k * 36: y + 32 + k * 36, x: x + 32] = roi

        item_list = []
        # проверка на пустые слоты
        for m in range(6):
            try:
                item_name = item_dic[player['item_{}'.format(m)]]

                item = cv2.imread('images/items/{} icon.png'.format(item_name.lower()), -1)
                item_list.append(item)
            except KeyError:
                continue
        for q, slot in enumerate(item_list):
            template[
                y1 + k * 36: y1 + 32 + k * 36,
                x1 + 45 * q: x1 + 44 + 45 * q
                ] = slot


def write_param(x, y, param, font):
    global draw
    length, _ = draw.textsize(param, font=font)
    start_point = x - length if x in [269, 190] else x
    draw.text((start_point, y), param, font=font, fill='black')

def post_game(match_id):
    global draw, template
    match = Match(match_id).info()
    font = ImageFont.truetype(font_path, 19)
    font1 = ImageFont.truetype(font1_path, 19)

    if bool(match['radiant_win']):
        template = cv2.imread('images/templates/radiant.png', -1)
    else:
        template = cv2.imread('images/templates/dire.png', -1)

    fill_template((14, 142), (309, 142), 0, match)
    fill_template((14, 375), (309, 375), 1, match)
    cv2.imwrite('images/lineup/postgame.png', template)

    im = Image.open('images/lineup/postgame.png')
    draw = ImageDraw.Draw(im)

    for i in range(10):
        y_param = 150 if i < 5 else 203
        player = match['players'][i]
        try:
            name = player['personaname']
        except KeyError:
            name = "Unknown"
        start_point, name = length_check(name, font)
        draw.text((start_point, y_param + i * 36), name, font=font, fill='white')
        kda = [
            player['kills'],
            player['deaths'],
            player['assists']
            ]
        kda = [str(x) for x in kda]
        for j, stat in enumerate(kda):
            length, _ = draw.textsize(str(stat), font=font1)
            start_point = 225 - length//2 + j*31
            draw.text((start_point, y_param + i * 36), stat, font=font1, fill='white')

        match_id = 'Match id {}'.format(match['match_id'])
        game_mode = game_mode_dic[match['game_mode']]
        m, s = divmod(match['duration'], 60)
        s = s if len(str(s)) == 2 else "{}{}".format(0, s)  # make secons 0x format
        duration = "Duration {0}:{1}".format(m, s)
        date = datetime.datetime.fromtimestamp(
                int(match['start_time'])).strftime('%d-%m-%Y %H:%M:%S')

    write_param(269, 78, match_id, font)
    write_param(269, 51, game_mode, font)
    write_param(321, 78, duration, font)
    write_param(321, 51, date, font)

    im.save('images/lineup/postgame.png')


def post_game_guess(match):
    global draw, template

    font = ImageFont.truetype(font_path, 19)
    font1 = ImageFont.truetype(font1_path, 19)

    if bool(match['radiant_win']):
        template = cv2.imread('images/templates/game_radiant.png', -1)
    else:
        template = cv2.imread('images/templates/game_dire.png', -1)

    fill_template((14, 142), (152, 142), 0, match)
    fill_template((14, 375), (152, 375), 1, match)
    cv2.imwrite('images/lineup/game_postgame.png', template)

    im = Image.open('images/lineup/game_postgame.png')
    draw = ImageDraw.Draw(im)

    for i in range(10):
        player = match['players'][i]
        y_param = 150 if i < 5 else 203
        kda = [
            player['kills'],
            player['deaths'],
            player['assists']
            ]
        kda = [str(x) for x in kda]
        for j, stat in enumerate(kda):
            length, _ = draw.textsize(str(stat), font=font1)
            start_point = 68 - length//2 + j*31  # 68 - center of first kda number
            draw.text((start_point, y_param + i * 36), stat, font=font1, fill='white')

        match_id = 'Match {}'.format(match['match_id'])
        game_mode = game_mode_dic[match['game_mode']]
        m, s = divmod(match['duration'], 60)
        s = s if len(str(s)) == 2 else "{}{}".format(0, s)  # make secons 0x format
        duration = "Duration {0}:{1}".format(m, s)
        date = datetime.datetime.fromtimestamp(
                int(match['start_time'])).strftime('%d-%m-%Y %H:%M:%S')

    write_param(190, 78, match_id, font)
    write_param(190, 51, game_mode, font)
    write_param(242, 78, duration, font)
    write_param(242, 51, date, font)

    im.save('images/lineup/game_postgame.png')
