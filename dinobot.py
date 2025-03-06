from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import discord
from discord.ext import commands
import uuid
import os
import yaml
import random

# table of crop rectangles for the various panels. These were determined
# using a paint program on a downloaded comic.
CROP_RECTANGLES = [
	(0, 0, 297, 298),
	(298, 0, 458, 298),
	(457, 0, 899, 298),
	(0, 296, 239, 595),
	(237, 296, 604, 595),
	(602, 296, 899, 595),
]

# we have canned error messages for if commands are bogus. They are not helpful.
# they are, however, from the comic. 17? Why not.
ERROR_MESSAGES = [
	"Sherlock Holmes, who we all already deduced was the world's greatest detective, frowned. He was faced with a new crime! And it was a crime unlike any he'd seen before. This crime......was a COMPUTER CRIME.",
	"I can't even use a computer anymore, my hands go right through the keys!",
	"Babbage's Analytical Engine was designed in the 1830s! Sherlock COULD be familiar with basic computer stuff.",
	"A poster with just a picture of a computer and a cellphone and beneath that it says \"ANYWAY, I STARE AT THESE A LOT\"!!",
	"You ever see what I do with my computers? I drop 'em by accident and then get new ones.",
	"Is the future TRULY full of computers doing a crappier job than we'd do, but for helluva cheaper??",
	"Ah. So we're explaining a simple language concept via a complicated CS concept.",
	"A lot of things we do today are mediated by the computers on the internet!",
	"I read 150 stories last year and not ONE included an embarrassing display of ignorance regarding the actual bandwidth capacities of 2400 baud modems.",
	"Am I TRULY a Luddite now??",
	"IT'S LOOM SMASHING TIME",
	"I'm tired of doing things on computers!",
	"Dracula is canonically a hacker with an immortal dog??",
	"That was your FIRST old man story. It had no point except to point out that when you were younger things were different than they are now. I think we should acknowledge it, like a first grey hair!",
	"Unfortunately, the machine used an older and obsolete SCSI bus type. To even get it to spin up, Maldives was reduced to daisy-chaining a SCSI to IDE bridge with an IDE to SATA adapter, hoping that would work. It didn't!!",
	"Okay, so we all know computers can turn electricity into bad tweets. But did you know that's not intentional? When they were invented, tweets weren't even a thing yet!!",
	"That's just a bunch of strange computers that now I'm renting instead of owning!!",
	"Do you know that millennials use COMPUTERS more often than seniors do, and seniors use computers precisely the correct amount?",
]

# fetch_panel will save off panel 2 from a random comic, and return the URL
# of the comic
def fetch_panel(panel_name, panel_number):
	URL = "https://www.gocomics.com/random/dinosaur-comics"
	page = requests.get(URL)
	img_src = BeautifulSoup(page.content, 'html.parser').find_all('picture', class_='item-comic-image')[0].find('img')['src']

	# fetch the image and chop out panel 2
	# luckily, these offsets never change
	png_data = requests.get(img_src)
	with Image.open(BytesIO(png_data.content)) as img:
		panel = img.crop(CROP_RECTANGLES[panel_number])
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

# we're going to default to the second panel, if the user doesn't provide
# an option, because that's usually the funniest panel
# note that the panel numbers are one-indexed, because it's a human
# on the other end. I mean, probably.
# note as well that we define target_panel here as a string, so if someone passes a
# non-integer string, we don't just error in the framework, but error here.
# That gives us a chance to send a dumb, useless error message.
@bot.command(name='qwantz')
async def qwantz(ctx, target_panel="2"):
	# we need to be careful with the panel parameter, because some 
	# smartass in one of my server is definitely going to try 
	# "$qwantz -1", "$qwantz 42069", and/or "$qwantz beer"
	try:
		panel_number = int(target_panel)
		# this is dumb, but a negative index for a panel number could
		# be here (see: smartasses), and python will just treat it as an index 
		# from the end of the list of panels. That is goofy, so we'll just 
		# return an error in that case. Again, not a helpful one.
		if panel_number < 0:
			raise IndexError("Nice try.")
		file_name = "{0}.gif".format(str(uuid.uuid4()))
		# make sure to subtract one to make the panel_number zero-indexed
		url = fetch_panel(file_name, panel_number - 1)
		with open(file_name, 'rb') as fp:
			file_to_send = discord.File(fp, filename=file_name)
			await ctx.send("Today is a good day I think for sending a [panel]({0}).".format(url), file=file_to_send)
		os.remove(file_name)
	except (ValueError, IndexError) as e:
		await ctx.send(random.choice(ERROR_MESSAGES))

# start up our bot (using the token from the YAML file)
start_bot(bot)
