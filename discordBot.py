#!!!THERES A MESSAGE STACK SO YOU DONT HAVE TO CARE ABOUT DOING ASYNC REQUESTS


import discord as dis
import requests as req
import re
import asyncio
import logging
import NoidFaxer as noid
from PIL import Image
import random
import os
import json

logging.basicConfig(level=logging.INFO) #so that info is logged
#logging.basicConfig(level=logging.ERROR) #so that I can get errors through the logging module

bot = dis.Client()
IMG_FILE = 'NoidFaxImg.png'

with open('credentials.json') as f:
    CREDENTIALS = json.loads(f.read())
TOKEN, ADDRESS = CREDENTIALS['token'], CREDENTIALS['printer_addr']


true_print = print
def print(*args):
    try:
        true_print(*args)
    except UnicodeEncodeError:
        logging.error("unicode print error, idle is dumb, just ignore this")

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

def save_and_resize(data): #saves the data to 'NoidFaxImg.png' and resizes it so it can be printed
    path = str(random.random()) + '.png'
    f = open(path, 'wb')
    f.write(data)
    f.close()
    i = Image.open(path)
    i = i.resize((950,1400))
    i.save(path)
    return path

async def say(mess, channel):
    await channel.send("`" + mess + "`")

async def fax_image(url, channel): #faxes the image at url to the noid, communicates to user on channel
    for attempt in range(2): #try to download the data twice
        data = get_image_data(url)
        if data: #if image data was succesfully found
            print(url)
            await say("Got image data! Resizing image...", channel)
            f_path = save_and_resize(data)
            await say("Resized, faxing...", channel)
            noid.send_mail(ADDRESS, file_loc = f_path)
            os.remove(f_path)
            await say("Payload delivered, may god help us all.", channel)
            break #don't retry
        else: #if image data was not found
            error = "Error: Could not get image data from " + url
            if attempt == 0:
                error += '\nRetrying...'
            await say(error, channel)    

TEXT_FILE = 'text_fax.txt'
async def fax_text(text, channel):
    with open(TEXT_FILE, 'a+', encoding = 'utf-8') as f:
        if text != "!fax": #don't write commands to file
            f.write(text + '\n')
        f.seek(0)
        all_text = f.read()
        print("ALL_TEXT:", all_text)
    num_lines = all_text.count('\n')
    if text == "!fax" or num_lines >= 50: #wait for ~50 messages:
        open(TEXT_FILE, 'w').close() #empty text file
        temp_file = str(random.random()) + ".txt" #create a new text file so that TEXT_FILE can be edited by other corutines
        with open(temp_file, 'w', encoding = 'utf-8') as tf:
            tf.write(all_text)
        await say("Faxing " + str(num_lines) + " lines...", channel)
        noid.send_mail(ADDRESS, file_loc = temp_file) #sending it as a file instead of text so the printer formats it better
        os.remove(temp_file)
        await say("The wicked deed is done.", channel)
    else:
        await say("Message added to queue ({}/50 lines)".format(num_lines), channel)
    print("TEXT: ", text)

@bot.event #pass on_message corutine to bot's message event listener
async def on_message(mess): #fired when there is a message
    if mess.channel.name == 'noid-pipeline' and mess.author.id != bot.user.id: #if its the correct channel and not it's own message
        print("Recieved message")
        print(mess.content)
        mess_text = mess.content
        for link_data in mess.attachments: #go through all the links, fax them if possible
            if hasattr(link_data, 'width'): #if an image file
                print('FILE')
                await fax_image(link_data.url, mess.channel)
        for url in links_in(mess.content):
            mess_text = mess_text.replace(url, '') #remove url from text
            await fax_image(url, mess.channel) #we'll check if it's an actual image later
        if mess_text != '':
            await fax_text(mess_text, mess.channel)


bot.run(TOKEN) #login and start the bot
