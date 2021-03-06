import tweepy
import yaml

with open('config_secrets.yml', 'r') as f:
    cfg = yaml.load(f)
    MAIN = cfg['main_app']


class Bot(object):

    """ Model for a bot that you 'control' """

    def __init__(self, config=None, **kwargs):
        print("Bots making bots. This will end well.")
        if config:
            for (param, val) in config.items():
                setattr(self, param, config.get(param))
            if self.use_main:
                self.consumer_key = MAIN['consumer_key']
                self.consumer_secret = MAIN['consumer_secret']
        else:
            default_params = {
                'use_main': False,
                'consumer_key': None,
                'consumer_secret': None,
                'access_key': None,
                'access_secret': None,
                'user_id': None
            }
            for (param, default) in default_params.items():
                setattr(self, param, kwargs.get(param, default))

        print("Bot created:", self.__repr__())

    def _get_api(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    def delete_status(self, status=None):
        print('Initiating delete of status {0}'.format(status))
        api = self._get_api()
        try:
            api.destroy_status(id=status)
            print('Deleted status {0}'.format(status))
            return True
        except:
            return False

    def __repr__(self):
        return "Bot(ID: {0}, Main App: {1})".format(
                self.user_id,
                self.use_main
            )
