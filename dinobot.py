from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import discord
from discord.ext import commands
import uuid
import os
import yaml

# fetch_panel will save off panel 2 from a random comic, and return the URL
# of the comic
def fetch_panel(panel_name):
	URL = "https://www.gocomics.com/random/dinosaur-comics"
	page = requests.get(URL)
	img_src = BeautifulSoup(page.content, 'html.parser').find_all('picture', class_='item-comic-image')[0].find('img')['src']

	# fetch the image and chop out panel 2
	# luckily, these offsets never change
	png_data = requests.get(img_src)
	with Image.open(BytesIO(png_data.content)) as img:
		panel = img.crop((298, 0, 458, 298))
		panel.save(panel_name)
	return page.url

def start_bot(bot):
	f = open('config.yaml')
	config_map = yaml.safe_load(f)
	f.close()	
	bot.run(config_map['discordtoken'])

def create_bot():
	intents = discord.Intents.default()
	intents.message_content = True

	return commands.Bot(command_prefix='$', intents=intents)

# create our bot to add our command to it
bot = create_bot()

@bot.command(name='qwantz')
async def qwantz(ctx):
	file_name = "{0}.gif".format(str(uuid.uuid4()))
	url = fetch_panel(file_name)
	with open(file_name, 'rb') as fp:
		file_to_send = discord.File(fp, filename=file_name)
		await ctx.send("Today is a good day I think for sending a [panel]({0}).".format(url), file=file_to_send)
	os.remove(file_name)

# start up our bot (using the token from the YAML file)
start_bot(bot)
