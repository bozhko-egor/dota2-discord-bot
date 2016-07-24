import pymongo


class DotaDatabase:
    """class to simplify calls to db"""
    match_search_args = {   # only search for valid matches:
                'game_mode': {'$in': [0, 1, 2, 3, 4, 5, 12, 14, 16, 22]},  # see /ref/game_modes.json
                'duration': {'$gt': 720},  # match duration > 10min
                'players.level': {'$nin': [1, 2, 3, 4, 5]},
                'players.leaver_status': {'$nin': [5, 6]},
                'lobby_type': {'$in': [0, 5, 6, 7]}
                }

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
            return "No such db entry"
        return acc_id[str(server)][str(discord_id)]

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

    def add_match_stat(self, data):
        self.db['matches_all'].insert_one(data)

    def get_match_stat(self, match_id):
        return self.db['matches_all'].find_one({'match_id': match_id})

    def get_match_list(self, criteria, sort=-1):
        # sort==-1 desc order
        # sort==1 asc order
        criteria.update(DotaDatabase.match_search_args)
        cursor = self.db['matches_all'].find(criteria)
        cursor.sort('start_time', sort)
        return list(cursor)


if __name__ == '__main__':

    db = DotaDatabase('dota2-db')
    db.connect()
    print(db.get_server_list())
