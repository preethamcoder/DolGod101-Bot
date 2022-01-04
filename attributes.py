import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class attributes(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
    #all the music related stuff
    self.is_playing = False

    # 2d array containing [song, channel]
    self.music_queue = []
    #self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    self.YDL_OPTIONS = {'format': 'bestaudio'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    self.vc = ""

     #searching the item on youtube
  def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

  def play_next(self):
      if len(self.music_queue) > 0:
          self.is_playing = True

            #get the first url
          m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
          self.music_queue.pop(0)

          self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
      else:
          self.is_playing = False

    # infinite loop checking 
  async def play_music(self):
    if len(self.music_queue) > 0:
        self.is_playing = True

        m_url = self.music_queue[0][0]['source']
        
        #try to connect to voice channel if you are not already connected

        if self.vc == "" or not self.vc.is_connected() or self.vc == None:
            self.vc = await self.music_queue[0][1].connect()
        else:
            await self.vc.move_to(self.music_queue[0][1])
        
        print(self.music_queue)
        #remove the first element as you are currently playing it
        self.music_queue.pop(0)

        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
    else:
        self.is_playing = False

  @commands.command(name="p", help="Plays a selected song from youtube", administrator = True)
  async def p(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("You gotta join a voice channel first 😤")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, please try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song's been added, mate!")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

  @commands.command(name="q", help="Displays the current songs in queue", administrator = True)
  async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Nothin' in here, mate!")

  @commands.command(name="skip", help="Skips the current song being played", administrator = True)
  async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()
  
  @commands.command(name="dc", help="Kicks the bot outta the voice chat", administrator = True)
  async def dc(self, ctx):
    await ctx.disconnect()