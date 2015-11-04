import os
import yaml

from twython import Twython, TwythonStreamer

APP_KEY = os.environ['CONSUMER_KEY']
APP_SECRET = os.environ['CONSUMER_SECRET']
OAUTH_TOKEN = os.environ['ACCESS_KEY']
OAUTH_TOKEN_SECRET = os.environ['ACCESS_SECRET']


class MyStreamer(TwythonStreamer):

    def __init__(self, *args, **kwargs):
        with open('config.yml', 'r') as f:
            cfg = yaml.load(f)

        self.humans = []
        for human in cfg['humans']:
            self.humans.append(cfg['humans'][human]['user_id'])

        super(MyStreamer, self).__init__(*args, **kwargs)

    def _get_bot_api():
        api = Twython(APP_KEY,
                      APP_SECRET,
                      OAUTH_TOKEN,
                      OAUTH_TOKEN_SECRET)
        return api

    def on_success(self, data):
        if 'direct_message' in data:
            dm = data['direct_message']
            if dm['sender_id'] in self.humans:
                api = self._get_bot_api()
                api.lookup_status(id=123)


if __name__ == '__main__':
    stream = MyStreamer(
        APP_KEY,
        APP_SECRET,
        OAUTH_TOKEN,
        OAUTH_TOKEN_SECRET)

    stream.user()
