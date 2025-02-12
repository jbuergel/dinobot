# dinobot
Discord Bot for posting the second panel of a random Dinosaur Comic

# what?
Yeah, you know, [Dinosaur Comics](https://www.qwantz.com/)?

# why.
Seemed like a good idea. Anyway, you will need to create a bot ([these are good instructions](https://discordpy.readthedocs.io/en/stable/discord.html)), add your token to a config.yaml, invite the bot to a server, and have the code running somewhere. I made it into a service on a server, but whatever you want to do. It has some dependencies, but they should all be in pypi (bs4, Pillow, discord).

For the record, my systemd service file for dinobot looks like this:

```
[Unit]
Description=dinobot

[Service]
WorkingDirectory=/home/ubuntu/dinobot
ExecStart=python3 /home/ubuntu/dinobot/dinobot.py

[Install]
WantedBy=multi-user.target
```
