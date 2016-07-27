# dota2-discord-bot

Discord bot that provides Dota2 related utilities.



Use [**this**](https://discordapp.com/oauth2/authorize?client_id=189656913246420992&scope=bot&permissions=268561414) link to invite the bot to your server.

##Adding matches

You can add your games to the bot's DB following these simple steps:

1. `!add_steamid <32bit steamid>` - links Steam ID to your Discord ID.
2. `!parse_my_game_history` - Parses your matches into DB. Takes about 10-15 min per 1000 games. 

**NOTE: Dota2 API gives a maximum of 500 last games for each hero you play. So if you have more than 500 games as same hero bot may not be able to get full stats.**

**NOTE2: Make sure you have "Expose Public Match Data" setting enabled in the Dota 2.**

**NOTE3: After successfully adding your Steam id bot will automatically parse your Dota 2 matches into DB every hour**
## List of commands:
Command prefix = `!`

1. Stats:
  - `wr`          - Your winrate playing as `hero_name`
  - `last`        - !last - your last match. Subcommands: `full`/`brief`
 
      `last full`:

 ![Image of full](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/example_game.png?raw=true)

        `last brief`: 
  ![Image of brief](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/lineup_example.png?raw=true) ![Image of brief2](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/itemlist_example.png?raw=true)
  - `stats`       - Your average stats in last `n` games
  - `p_last`      - Same as !last but for another player
  - `wr_with_hero`- Your winrate with `player` on specific `hero`
  - `wr_with`     - Your winrate with players (takes up to 4 arguments)
  - `avg`         - Your average stats playing as a `hero_name`
  - `hero_graph`  - Graph with your number of games played as a `hero_name` per month
 
  ![Image of hero_graph](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/graphs/hero.png?raw=true)
  - `game_stat <number>` - End-game screen with kda and items for all players for game №<number>, where `!game_stat 0` - your last game, `!game_stat -1` - your first game
     - `records`     - Your all-time records. Also takes <hero_name> argument for your hero-specific records.
2. Meta:
  - `uptime`      - Bot's current uptime
  - `join`        - Joins a server.
  - `about`       - Tells you information about the bot itself.
  - `help`        - Help message
  - `parse_my_game_history` - Parses your game history into db
  - `add_steamid ` - Makes connection discord id - steam id
3. PRO:
  - `pro_games`   - List of live or upcoming Dota2 pro games
  - `streams`     - Top 5 streams of `game` live on Twitch
4. Pics:
  - `item`        - Picture of `item_name`
  - `wow`         - Eddy Wally
  - `hero`        - `hero_name` 's icon
5. Game:
  - `guess`       - You need to guess the hero you or your friend played that game  
<center>![Image of game guess](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/example_game.png?raw=true)</center>
  - `quiz`        - Dota-themed quiz.
  - `leaderboard` - Highscores for `game_name` on this server.
6. Voice:
  - `voice`       - Plays voice line into your current voice channel. no spam pls.


#Running your instance of bot

## Config
To launch your own version of bot you need to create one configuration file: `token_and_api_key.py` with lines:

`api_key = "Dota2 api key here"` You can get one [here](https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey)/

`token = "your discord token"` You can get one [here](https://discordapp.com/developers/applications/me).

`client_id = discord client id`

`log_chat_id = chat id in which bot will post logs`

`font_path = path to fonts you want to use in !game_stat` - Main text font.

`font1_path` - Font of the numerals

##Requirements
1. Python 3.5+
2. discord.py
3. Pymongo
4. NumPy
5. OpenCV 3.0+

## Also you need running instance of MongoDB.





###Hero icons are extracted from the game Dota 2. The copyright for it is held by Valve Corporation, who created the software.
