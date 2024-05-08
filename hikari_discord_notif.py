# Hikari3 Discord Post Notification Bot
# Original version written by Lily

# Importing necessary libraries

from bs4 import BeautifulSoup
import requests
import discord 
import asyncio
import time
import datetime

# Creating necessary lists

url_list = [] # Temporarily storing the URLs of posts from Hikari3's recent posts section
post_content = [] # Temporarily storing post preview content from Hikari3's recent posts section
# Both of those temporary lists get cleared out for memory optimization purposes after the loop finishes.
already_submitted_url = [] # A permanent list storing URLs that were already posted to Discord. Isn't wiped at the end of the loop.
# The permanent list WILL BE a HUGE MEMORY HOG over time. This bot sucks ass and is inefficient as fuck.

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        channel = client.get_channel(#channelid) # Replace with channel ID you wanna send stuff to.

        while True:
            
            await asyncio.sleep(30)
            url = "https://www.hikari3.ch/"
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, "lxml")

            for link in soup.find_all("a", class_="linkPost title"): # Scraping recent URLs from Hikari3
                results = link.get('href') 
                url_list.append("https://hikari3.ch" + results) # Appending URLs to temporary URL list

            for post in soup.find_all("span", class_="labelPreview"):
                results = post.text # Scraping recent post preview content from Hikari3
                post_content.append(results) # Appending them to the temporary list

            for i, j in zip(url_list, post_content): # The part that actually posts to Discord.

                if i not in already_submitted_url: # If a URL isn't in the already submitted list
                    await channel.send("Post: " + i + "\nPost Preview:\n" + j) # Post it to Discord
                    already_submitted_url.append(i) # And put the URL in the permanent already submitted list.

            url_list.clear()
            post_content.clear()

    async def on_message(self, message): # Shit from the boilerplate. Not strictly necessary, but was useful for debugging
        print(f'Message from {message.author}: {message.content}')




intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('token')

# Bot token in the line above. Block of code actually starts the bot.

# How does this bot work? It's dumb.
# Step 1: Create the necessary lists to store stuff in.
# Like the temporary URL list, the temporary post list, and the permanent posted URLs list.
# Step 2: Enclose EVERYTHING in an infinite while loop.
# Step 3: Making a request to Hikari3's homepage to get the HTML
# Step 4: Scraping from the HTML
# The recent URLs are appended to the temporary URL list
# The recent post previews are appended to a temporary post preview list.
# Step 5: Posting
# Iterating through both the temp url list and the temp post preview list
# If a URL wasn't in the already submitted list (so if it hasn't been posted yet to Discord)
# It and the post preview is posted to Discord, and the URL is added to the permanent already submitted list.
# Step 6: Cleanup
# The temporary lists are deleted to help clean up memory.
# And then finally Step 7: Restarting
# The infinite loop starts all over again, and everything happens again.

# Issues:
# When you first start the thing up it'll post EVERYTHING on the recent posts page to Discord, but after that it should work properly
