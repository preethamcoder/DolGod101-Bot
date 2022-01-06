import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import random

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
    self.thoughts = ["The wise lament neither for the living nor the dead.", "Never was there a time when you did not exist, nor our master, nor all these people; nor in the future shall any of us cease to be.", "As the embodied soul continually passes, in this body, from boyhood to youth to old age, the soul similarly passes into another body at death. The self-realized soul is not bewildered by such a change.", 
    "The temporary appearance of happiness and distress, and their disappearance in due course, are like the appearance and disappearance of winter and summer seasons. They arise from sense perception, and one must learn to tolerate them without being disturbed.", 
    "For the soul there is never birth nor death. Nor, having once been, does he ever cease to be. He is unborn, eternal, ever-existing, undying and primeval. He is not slain when the body is slain.", 
    "As a person puts on new garments, giving up old ones, similarly, the soul accepts new material bodies, giving up the old and useless ones.", 
    "The soul can never be cut into pieces by any weapon, nor can he be burned by fire, nor moistened by water, nor withered by the wind.", "For one who has taken his birth, death is certain; and for one who is dead, birth is certain. Therefore, in the unavoidable discharge of your duty, you should not lament."
    "Wherever there is Kṛṣṇa, the master of all mystics, and wherever there is Arjuna, the supreme archer, there will also certainly be opulence, victory, extraordinary power, and morality. That is my opinion."
    "All living entities are born into delusion, overcome by the dualities of desire and hate.", "You have a right to perform your prescribed duty, but you are not entitled to the fruits of action. Never consider yourself to be the cause of the results of your activities, and never be attached to not doing your duty."]
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
        voice_channel = ''
        if(ctx.author.voice.channel == None):
            await ctx.send("Ayo, you gottaa be in a voice channel first 😡")
        else:
            voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("You gotta join a voice channel first 😤")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, please try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send(f"{ctx.author.name}, your song's been added, mate!")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

  @commands.command(name="q", help="Displays the current songs in queue", administrator = True)
  async def queue(self, ctx):
        retval = ""
        for index in range(0, len(self.music_queue)):
            retval += self.music_queue[index][0]['title'] + "\n"

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
  
  @commands.command(name="thought", help="Randomly throws some knowledge out 😂", administrator = True)
  async def thought(self, ctx):
    lim = len(self.thoughts)
    ind = random.randint(0, lim-1)
    await ctx.send(self.thoughts[ind])
    
  @commands.command(name="dc", help="Kicks the bot outta the voice chat", administrator = True)
  async def dc(self, ctx):
    await self.vc.disconnect()
