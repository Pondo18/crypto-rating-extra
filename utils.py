import yaml


class ConfigReader:
    def __init__(self):
        self.config_variables = self.get_config_variables()

    @staticmethod
    def get_config_variables():
        with open('config.yml') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            variables = {
                'host': data.get('database.postgres.host'),
                'user': data.get('database.postgres.user'),
                'password': data.get('database.postgres.password'),
                'database': data.get('database.postgres.database'),
                'reddit.user_agent': data.get('reddit.user_agent'),
                'reddit.client_id': data.get('reddit.client_id'),
                'reddit.client_secret': data.get('reddit.client_secret'),
            }
            return variables

