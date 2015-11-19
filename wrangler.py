import yaml
import re

import tweepy

from models import Bot

with open('config_secrets.yml', 'r') as f:
    config = yaml.load(f)
    CONSUMER_KEY = config['wrangler']['consumer_key']
    CONSUMER_SECRET = config['wrangler']['consumer_secret']
    ACCESS_KEY = config['wrangler']['access_key']
    ACCESS_SECRET = config['wrangler']['access_secret']

COMMANDS = [
    'delete',
]


class WranglerStream(tweepy.StreamListener):

    def __init__(self, *args, **kwargs):
        with open('config_secrets.yml', 'r') as f:
            self.config = yaml.load(f)

        self.humans = []
        for human in self.config['humans']:
            self.humans.append(self.config['humans'][human]['user_id'])

        self.bot_ids = []
        for bot in self.config['bots']:
            self.bot_ids.append(self.config['bots'][bot]['user_id'])

        self.bot_names = []
        for bot in self.config['bots']:
            self.bot_names.append(bot.lower())

        print("Wrangling bots:", ["{0}: {1}".format(bot[0], bot[1]) for bot in zip(self.bot_ids, self.bot_names)])

        super(WranglerStream, self).__init__(*args, **kwargs)

    @staticmethod
    def _get_api():
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api

    @staticmethod
    def _stripw(text):
        """ Simple function to strip out all whitespace """
        return re.sub(r'\s+', '', text)

    def _execute_command(self,
                         command=None,
                         bot_name=None,
                         wrangler=None,
                         status=None):

        if command in COMMANDS:
            bot = Bot(self.config['bots'][bot_name])
            if command == 'delete':
                bot.delete_status(status=status)
        else:
            api = self._get_api()
            api.send_direct_message(
                user_id=wrangler,
                text="{0} command not found.".format(command))

    def on_connect(self):
        self.api = self._get_api()
        print('Connected!')

    def on_status(self, status):
        """ Basic case: reply to a tweet with a command. """

        command = None
        status_id = None
        bot_name = None
        wrangler = None

        status = status._json

        try:
            if status['in_reply_to_user_id'] in self.bot_ids:
                print('got reply')
                wrangler = status['user']['id']
                status_id = status['in_reply_to_status_id']
                bot_screenname = '@{0}'.format(status['in_reply_to_screen_name'])
                bot_name = status['in_reply_to_screen_name'].lower()
                text = status['text'].replace(bot_screenname, '')
                command = self._stripw(text).lower()

            print('found:', status_id, bot_name, command)

            if command and bot_name and wrangler:
                self._execute_command(
                    command=command,
                    bot_name=bot_name,
                    wrangler=wrangler,
                    status=status_id)
        except Exception as e:
            print(e)


def main():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    with open('config_secrets.yml', 'r') as f:
        config = yaml.load(f)

    humans = []
    for human in config['humans']:
        humans.append(str(config['humans'][human]['user_id']))
    print("Tracking humans:", humans)

    stream = tweepy.Stream(auth, WranglerStream())
    stream.filter(follow=humans)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nLater, alligator\n\n")
