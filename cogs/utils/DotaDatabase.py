import pymongo
import time

class DotaDatabase:

    def __init__(self, db_name):
        self.db_name = db_name
        self.db = 'Not yet connected'

    def connect(self):
        conn = pymongo.MongoClient()
        self.db = conn[self.db_name]

    def get_acc_id(self, discord_id, server):
        acc_id = self.db['steamids'].find_one(
            {'{}.{}'.format(str(server), str(discord_id)): {'$exists': 1}})
        if not acc_id:
            return
        return acc_id[str(server)][str(discord_id)]

    def get_discord_id(self, steamid, server):
        cursor = list(self.db['steamids'].find({str(server): {'$exists': 1}}))
        for entry in cursor:
            for key, value in entry[str(server)].items():
                if value == steamid:
                    _id = key
        return _id

    def get_all_ids_on_server(self, server):
        # there should be a better way
        cursor = list(self.db['steamids'].find({str(server): {'$exists': 1}}))
        dic = {}
        for entry in cursor:
            dic.update(entry[str(server)])
        return list(dic.values())

    def update_name(self, steam_name, match_id, account_id):
        self.db['matches_all'].update_one(
                            {'$and':
                                [
                                    {'match_id': match_id},
                                    {"players.account_id": account_id}
                                ]
                            },
                            {"$set": {"players.$.personaname": steam_name}}
                        )

    def get_server_list(self):
        # there definetly should be a better way
        servers = list(self.db['steamids'].find())
        server_list = []
        for entry in servers:
            for key in entry.keys():
                if key != '_id' and key not in server_list:
                    server_list.append(key)
        return server_list
    #def get_leaderboard(self, db, game, server):

    def add_id(self, discord_id, server, account_id):
        acc_id = self.db['steamids'].find_one(
            {'{}.{}'.format(str(server), str(discord_id)): {'$exists': 1}})
        if not acc_id:
            self.db['steamids'].insert_one(
                {
                    str(server):
                        {str(discord_id): account_id}
                }
            )
        else:
            return "Already in db. Need to delete old entry first."

    def delete_id(self, discord_id, server):
        acc_id = self.db['steamids'].find_one(
            {'{}.{}'.format(str(server), str(discord_id)): {'$exists': 1}})
        if not acc_id:
            return "No entry to delete"
        else:
            self.db['steamids'].delete_one(acc_id)

    def get_all_ids(self):
        servers = list(self.db['steamids'].find())
        server_list = []
        for entry in servers:
            for key in entry.keys():
                if key != '_id' and key not in server_list:
                    server_list.append(key)
        user_list = []
        for server in server_list:
            cursor = list(self.db['steamids'].find({str(server): {'$exists': 1}}))
            dic = {}
            for entry in cursor:
                dic.update(entry[str(server)])
            users = list(dic.values())
            for user in users:
                if user not in user_list:
                    user_list.append(user)
        return user_list

    def add_leaderboard_guess(self, server, discord_id, score, collection):
        self.db[collection].insert_one(
            {
                str(server): {
                    'discord_id': discord_id,
                    'score': score,
                    'date': time.time()}
            }
            )

    def get_leaderboard(self, server, collection):
        cursor = self.db[collection].find({str(server): {'$exists': 1}})
        cursor.sort("{}.score".format(server), -1)
        leaderboard = list(cursor)
        highscores = []
        entry = 5 if len(leaderboard) > 5 else len(leaderboard)
        for i in range(entry):
            highscores.append(leaderboard[i][server])

        def get_key(item):
            return item['score']
        return sorted(highscores, key=get_key, reverse=True)

if __name__ == '__main__':

    db = DotaDatabase('dota2-db')
    db.connect()
    print(db.get_server_list())
