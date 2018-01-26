#!!!THERES A MESSAGE STACK SO YOU DONT HAVE TO CARE ABOUT DOING ASYNC REQUESTS
#THE TOKEN AND PRINTER EMAIL HAVE BEEN SET TO EMPTY STRINGS (since I don't want random people on github to find those)


import discord as dis
import requests as req
import re
import logging
import NoidFaxer as noid
from PIL import Image
import random
import os


logging.basicConfig(level=logging.INFO) #so that info is logged
#logging.basicConfig(level=logging.ERROR) #so that I can get errors through the logging module

bot = dis.Client()
TOKEN = '' #token to log in the bot (removed for github)
CHANNEL = 'noid-pipeline' #the name of the discord channel that accepts commands
PRINTER_ADDRESS = '' #address that the image is sent to for printing


def links_in(s):
    return re.findall(r'https?://[^\s]+', s)

def get_image_data(url):
    try:
        page = req.get(
            url,
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'},
            timeout = 10
            )
        if 'image' in page.headers['Content-Type'].lower():
            return page.content
    except:
        pass
    return ''

def save_and_resize(data): #saves the data and resizes it so it can be printed
    path = str(random.random()) + '.png'
    f = open(path, 'wb')
    f.write(data)
    f.close()
    i = Image.open(path)
    i = i.resize((950,1400))
    i.save(path)
    return path

async def say(mess, channel):
    await bot.send_message(channel, "`" + mess + "`")

async def fax(url, channel): #prints the image specified by the url, communicates to user on channel
    for attempt in range(2): #try to download the data twice
        data = get_image_data(url)
        if data: #if image data was succesfully found
            print(url)
            await say("Got image data! Resizing image...", channel)
            f_path = save_and_resize(data)
            await say("Resized, Faxing...", channel)
            noid.sendFile(f_path, PRINTER_ADDRESS)
            os.remove(f_path)
            await say("Payload delivered, may god help us all.", channel)
            break #don't retry
        else: #if image data was not found
            error = "Error: Could not get image data from " + url
            if attempt == 0:
                error += '\nRetrying...'
            await say(error, channel)

@bot.event #pass on_message corutine to bot's message event listener
async def on_message(mess): #fired when there is a message
    if mess.channel.name == CHANNEL and mess.author.id != bot.user.id: #if its the correct channel and not it's own message
        print("Recieved message")
        await say("Recieved message", mess.channel)
        for link_data in mess.attachments: #go through all the links, fax them if possible
            if 'width' in link_data: #if an image file
                print('FILE')
                await fax(link_data['url'], mess.channel)
        for url in links_in(mess.content):
            await fax(url, mess.channel) #we'll check if it's an actual image later


bot.run(TOKEN) #login and start the bot
