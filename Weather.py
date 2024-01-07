import discord
from discord.ext import commands
import requests 

#
BOT_TOKEN = 'MT'
OPENWEATHERMAP_API_KEY = '004'

# Store User Locations 
UserLocation = {}

#
intents = discord.Intents.default()
intents.message_content = True 

#
bot = commands.Bot(command_prefix="!", intents=intents) 


@bot.event
async def on_ready():
    
    GuildCount = 0 # Track how many servers the bot is connected too
    
    for guilds in bot.guilds:  # Loop through all the guilds
        GuildCount = GuildCount + 1 # Increase counters
    print("Guild Count: " + str(GuildCount))
    
    print(f'{bot.user.name} has connected to Discord!')
 
@bot.event
async def on_guild_join(ctx):
    print(f'Joined a New Server: {ctx.guild.name}')
    
    Welcome_Message = f"Thank you for inviting me to {ctx.guild.name}"
    
    default_channel = ctx.channel
    if(default_channel) is not None:
        await default_channel.send(Welcome_Message)

# Bot Commands

@bot.command(name = 'SetLocation')
async def SetLocation(ctx, location):
    User = ctx.author
    UserLocation[ctx.author.id] = str(User) + ':' +location  
    
    
@bot.command(name = 'weather')
async def get_weather(ctx):
    await ctx.send("Please provide city")
    
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel
    
    try:
        user_response = await bot.wait_for('message', timeout = 30.0, check=check)
        city = user_response.content
    except TimeoutError:
        await ctx.send("Time is up. Please try the command again and provide your city.")
        return
    
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    
    params = {'q': city, 'appid': OPENWEATHERMAP_API_KEY, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if response.status_code == 200:
        temperature = data['main']['temp']
        temperature_feels_like = data['main']['feels_like']
        Humidity = data['main']['humidity']
        Wind = data['wind']['speed']
        description = data['weather'][0]['description']
        Country = data['sys']['country']
        await ctx.send(f'The weather in {city}, {Country} is {description} with a temperature of {temperature}°C, but feels like {temperature_feels_like}°C with {Humidity}% and wind speeds of {Wind}')
    else:
        await ctx.send(f'Error: Unable to fetch weather data for {city}.')


# Help 

@bot.command(name = 'Help')
async def HelpCommand(ctx):
    await ctx.send(f'Help Commands')


#End of bot commands


# Run Bot
bot.run(BOT_TOKEN)
