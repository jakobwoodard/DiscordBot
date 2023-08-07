import youtube_dl
import asyncio
import discord
import json

from youtube_api import YouTubeDataAPI
from client import YT_KEY
## Setup code from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py ###
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
### END MUSIC SETUP ###

### Music bot controls ###
async def music(message, commands):
    # '%music play [query]'
    ctx = message.channel
    yt = YouTubeDataAPI(YT_KEY)
    if (commands[1].lower() == 'play' and len(commands) >= 3):
        if message.guild.voice_client is None:
            await message.author.voice.channel.connect()
        try :
            server = message.guild
            voice_channel = server.voice_client
            

            # async with ctx.typing():
            search = ' '.join(commands[2:])
            videos = yt.search(q=search, max_results=1)
            video = videos[0]
            print(video['video_id'])
            if not video:
                raise KeyError("No video found")
            link = "https://www.youtube.com/watch?v=" + video['video_id']
            print(link)
            filename = await YTDLSource.from_url(link)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.send('**Now playing:** {}'.format(filename))
        except:
            print('in except block')
            if not message.author.voice:
                await ctx.send("{} is not connected to a voice channel".format(message.author.name))
                return
            else:
                channel = message.author.voice.channel
            if message.guild.voice_client is None:
                print('no voice client')
    # '%music stop'
    elif (commands[1].lower() == 'stop'):
        voice_client = message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    # '%music pause'
    elif (commands[1].lower() == 'pause'):
        voice_client = message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")
    # '%music resume'
    elif (commands[1].lower() == 'resume'):
        voice_client = message.guild.voice_client
        print(voice_client)
        if voice_client.is_paused() is None:
            await ctx.send("The bot was not playing anything before this. Use `%music play [query]` command")            
        else:
            await voice_client.resume()
    
