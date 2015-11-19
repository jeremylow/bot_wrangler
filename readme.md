#### Bot Wrangler

##### Usage

Highly suggested that you use a virtual environment for this.

* Create a new application on twitter for your bot wrangler. Ideally (I guess?) this is controlled by your user account or maybe just one of your bot accounts. It really doesn't matter.
* Install the required dependencies with `pip install requirements.txt`
* Copy `config.py` to `config_secrets.py`: `cp config.py config_secrets.py`
* Edit `config_secrets.py` to include your bots and the wrangler app.
* Run the wrangler with `python wrangler.py`


##### Advanced Usage

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
