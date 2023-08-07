# import youtube_dl

### Setup code from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py ###
# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)
#         self.data = data
#         self.title = data.get('title')
#         self.url = ""

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]
#         filename = data['title'] if stream else ytdl.prepare_filename(data)
#         return filename
# ### END MUSIC SETUP ###

# ### Music bot controls ###
# async def music(message, commands):
#     # '%music play [query]'
#     ctx = message.channel
#     if (commands[1].lower() == 'play' and len(commands) >= 3):
#         try :
#             server = ctx.message.guild
#             voice_channel = server.voice_client

#             ## Webscrape for top result from yt and play audio ##
#             async with ctx.typing():
#                 search_link = "http://www.youtube.com/results?search_query=" + '+'.join(commands[3:])
#                 search_result = requests.get(search_link).text
#                 soup = BeautifulSoup(search_result, 'html.parser')
#                 videos = soup.select(".yt-uix-tile-link")
#                 if not videos:
#                     raise KeyError("No video found")
#                 link = "https://www.youtube.com" + videos[0]["href"]
#                 filename = await YTDLSource.from_url(link)
#                 voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
#             await ctx.send('**Now playing:** {}'.format(filename))
#         except:
#             if not ctx.message.author.voice:
#                 await ctx.send("{} is not connected to a voice channel".format(message.author.name))
#                 return
#             else:
#                 channel = message.author.voice.channel
#             await channel.connect()
#             music(message, commands)
#     # '%music stop'
#     elif (commands[1].lower() == 'stop'):
#         voice_client = message.guild.voice_client
#         if voice_client.is_playing():
#             await voice_client.stop()
#         else:
#             await ctx.send("The bot is not playing anything at the moment.")
#     # '%music pause'
#     elif (commands[1].lower() == 'pause'):
#         voice_client = message.guild.voice_client
#         if voice_client.is_playing():
#             await voice_client.pause()
#         else:
#             await ctx.send("The bot is not playing anything at the moment.")
#     # '%music resume'
#     elif (commands[1].lower() == 'resume'):
#         voice_client = message.guild.voice_client
#         if voice_client.is_paused():
#             await voice_client.resume()
#         else:
#             await ctx.send("The bot was not playing anything before this. Use `%music play [query]` command")
    
