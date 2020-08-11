import pickle, os, copy

database = None

default_db = {
        'guilds': {},
        }

server_db = {
    'counting': {
        'channel': None,
        'current-num': 0,
        'last-counter': None
    },
    'points': [],
    'prefix': 'mg '
}


class DataBase():
    def __init__(self, bot, path):
        self.locks = {}
        self.bot = bot
        self.path = path
        self.parse_database()

    def create_database(self):
        with open(self.path, 'wb+') as f:
            copy_of_default_db = copy.deepcopy(default_db)
            pickle.dump(copy_of_default_db, f)

    def parse_database(self):
        guilds = self.bot.guilds

        if not os.path.isfile(self.path):
            self.create_database()
        with open(self.path, 'rb') as f:
            self.db = pickle.load(f)
        # checks
        for guild in guilds:
            self.add_guild(guild.id)

    def save_database(self):
        with open(self.path, 'wb') as f:
            try:
                string = pickle.dumps(self.db)
                f.write(string)
            except Exception as e:
                print(type(e), e)
                print(self.db)

    def add_guild(self, guild_id):
        if guild_id not in self.db['guilds'].keys():
            copy_of_server_db = copy.deepcopy(server_db)
            self.db['guilds'][guild_id] = copy_of_server_db

    def remove_guild(self, guild_id):
        if guild_id in self.db['guilds'].keys():
            del self.db['guilds'][guild_id]


def set_database(bot, path='database.pickle'):
    global database
    database = DataBase(bot, path)