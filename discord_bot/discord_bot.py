import requests
import os
import discord
from discord.ext import commands,tasks

intents = discord.Intents().all()
client = discord.Client()

@client.event
async def on_ready():
    print('Fact checker is live %')


@client.event
async def on_message(message):
        
    if message.author == client.user:
        return

    if message.content.lower().startswith('!check '):
        claim = message.content[7:]
        response = requests.get(url = f'http://127.0.0.1:5001/quicktool?claim1={claim}')
        result = response.json()
        try:
            embed = discord.Embed(title = 'Fact checker verdict',url=result['url'])
        except:
            embed = discord.Embed(title = 'Fact checker verdict')

        embed.add_field(name = 'Claim ',value=claim)
        try:
            embed.add_field(name = 'Claim rating ', value=result['truth'],inline=False)
        except:
            embed.add_field(name = 'Claim rating ', value='Indeterminable',inline=False)

        await message.channel.send(embed=embed)



api_key=''
with open(os.path.expanduser('~/TextRef/api_key.txt')) as f:
    api_key = f.read().split()[1]
    request_headers = {"x-api-key": api_key}
    pass

client.run(api_key)