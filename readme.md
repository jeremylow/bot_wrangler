#### Bot Wrangler

##### Usage

The gist is that you can run a bot wrangler independent of your bots but if they tweet something that you don't like, you have an easy way to delete that tweet without having to log into their account and manually delete it.

The basic configuration is to add your user id on twitter to the `humans` part of the `config_secrets.py`. If you want other people to be able to wrangle your bots, just add another human (give them a different name from `me`, which is only a suggestion anyway). They don't have to give you any special info (no access keys or anything), but they can reply to a bot's tweet with `@[bot] delete` and the bot will delete that tweet itself.

The `delete` command is the only one currently implemented (only one I could think of...), but if folks have other ideas, please let me know.

##### Installation

Highly suggested that you use a virtual environment for this.

* Create a new application on twitter for your bot wrangler. Ideally (I guess?) this is controlled by your user account or maybe just one of your bot accounts. It really doesn't matter.
* Install the required dependencies with `pip install requirements.txt`
* Copy `config.py` to `config_secrets.py`: `cp config.py config_secrets.py`
* Edit `config_secrets.py` to include your bots and the wrangler app.
* Run the wrangler with `python wrangler.py`


##### Advanced Installation

Using a virtual environment is really highly recommended for this.

If you're hosting this on a server and you have supervisord installed, you can use the files in the `conf` and `bin` directories to manage the wrangler though that.

Symlink the wrangler.conf file to your `/etc/supervisord/conf.d/`:

    sudo ln -s bot_wrangler/conf/wrangler.conf /etc/supervisord/conf.d/wrangler.conf

You'll need to update the wrangler.conf file to your specific installation, though. There are a few things to note:

* The `command` portion should point to the full path of the `bin/wrangler_start.sh` file wherever it is on your system. For me, that's something like /home/jeremy/bot_wrangler/bin/bot_wrangler.sh
* `user` change to your username. For me that's `jeremy`.
* `stdout_logfile` is where you want to store the log. It's probably a good idea, but you can replace with /dev/null if you don't care.

Same basic principles apply for the file in the `bin/` directory:

* Replace `YOU` with your username.
* WRANGLERDIR is where you cloned this repo.
* VENVDIR is the directory of your virtualenv for the wrangler.

Other than that it should work (I hope). If not, open up an issue and I'm happy to guide you through it.
