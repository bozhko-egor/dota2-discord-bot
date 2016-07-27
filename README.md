## dota2-discord-bot
uses dota2 api to parse match history into db.

dota2-bot v. 0.99a
   
## List of commands:
command prefix = !

1. Stats:
  - `wr`          - Your winrate playing as `hero_name`
  - `last`        - !last - your last match. Subcommands: `full`/`brief`
 
      `last full`:

 ![Image of full](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/example_game.png?raw=true)

      `last brief`:
 ![Image of brief](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/lineup_example.png?raw=true)
 ![Image of brief2](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/examples/itemlist_example.png?raw=true)
  - `stats`       - Your average stats in last `n` games
  - `p_last`      - Same as !last but for another player
  - `wr_with_hero`- Your winrate with `player` on specific `hero`
  - `wr_with`     - Your winrate with players (takes up to 4 arguments)
  - `avg`         - Your average stats playing as a `hero_name`
  - `hero_graph`  - Graph with your number of games played as a `hero_name` per month
 
  ![Image of hero_graph](https://github.com/bozhko-egor/dota2-discord-bot/blob/master/images/graphs/hero.png?raw=true)
  - `game_stat <number>` - End-game screen with kda and items for all players for game №<number>, where 0 - your last game, -1 - your first game
     - `records`     - Your all-time records. Also takes <hero_name> argument for your hero-specific records.
2. Meta:
  - `uptime`      - Bot's current uptime
  - `join`        - Joins a server.
  - `about`       - Tells you information about the bot itself.
  - `help`        - help
  - `parse_my_game_history` - Parses your game history into db
  - `add_steamid ` - Makes connection discord id - steam id
3. PRO:
  - `pro_games`   - List of live or upcoming Dota2 pro games
  - `streams`     - Top 5 streams of `game` live on Twitch
4. Pics:
  - `item`        - Picture of `item_name`
  - `wow`         - Eddy Wally
  - `hero`        - `hero_name`'s icon
5. Game:
  - `guess`       - You need to guees hero you or your friend played that game  
  - `quiz`        - Dota-themed quiz.
  - `leaderboard` - highscores for `game_name` on this server.
6. Voice:
  - `voice`       - Plays voice line into your current voice channel. No spam pls.


Hero icons are extracted from the game Dota 2. The copyright for it is held by Valve Corporation, who created the software.

##Running

# Config
To launch your own version of bot you need to create one configuration file: `token_and_api_key.py` with lines:

`api_key = "Dota2 api key here"`

`token = "your discord token"`

`client_id = discord client id`

`log_chat_id= chat id in which bot will post logs`


`font_path = path to fonts you want to use in !game_stat - main text`

`font1_path = -  numerals`

#Requirements
1. discord.py
2. opencv 3.0
3. pymongo
4. numpy

# Also you need running instance of MongoDB.

#Adding matches

You can add your games to db following these simple steps:

1. `!add_steamid <32bit steamid>` - add connection steamid-your discord id
2.  `!parse_my_game_history` - parses your matches to db. Takes about 10-15 min per 1000 games. **NOTE: Dota2 api gives a maximum of 500 last games for each hero you play. So if you have more than 500 games as same hero bot may not be able to get full stats.**
