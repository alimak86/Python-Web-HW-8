from mongoengine import connect
import configparser


class Atlas_Server:

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.mongo_user = self.config.get('DB', 'user')
        self.mongodb_pass = self.config.get('DB', 'pass')
        self.db_name = self.config.get('DB', 'db_name')
        self.domain = self.config.get('DB', 'domain')

    def connect(self):
        # connect to cluster on AtlasDB with connection string
        connect(
            host=
            f"mongodb+srv://{self.mongo_user}:{self.mongodb_pass}@{self.domain}/{self.db_name}?retryWrites=true&w=majority",
            ssl=True)
