from discord.ext import commands
import random

class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.word1 = ["artless", "bawdy", "beslubbering", "bootless", "churlish", "cockered", "clouted", "craven", "currish", "dankish", "dissembling", "droning", "errant", "fawning", "fobbing", "froward", "frothy",	"gleeking", "goatish", "gorbellied", "impertinent", "infectious", "jarring", "loggerheaded", "lumpish", "mammering", "mangled", "mewling", "paunchy", "pribbling", "puking", "puny", "qualling", "rank", "reeky", "roguish", "ruttish", "saucy", "spleeny", "spongy", "surly", "tottering", "unmuzzled", "vain", "venomed", "villainous",	"warped", "wayward", "weedy", "yeasty"]
        self.word2 = ["base-court", "bat-fowling", "beef-witted", "beetle-headed", "boil-brained", "clapper-clawed", "clay-brained", "common-kissing", "crook-pated", "dismal-dreaming", "dizzy-eyed", "doghearted", "dread-bolted", "earth-vexing", "elf-skinned", "fat-kidneyed", "fen-sucked", "flap-mouthed", "fly-bitten", "folly-fallen",	"fool-born", "full-gorged", "guts-griping", "half-faced", "hasty-witted", "hedge-born", "hell-hated", "idle-headed", "ill-breeding", "ill-nurtured", "knotty-pated", "milk-livered",	"motley-minded", "onion-eyed", "plume-plucked", "pottle-deep", "pox-marked", "reeling-ripe", "rough-hewn", "rude-growing", "rump-fed", "shard-borne", "sheep-biting", "spur-galled", "swag-bellied", "tardy-gaited", "tickle-brained", "toad-spotted", "unchin-snouted", "weather-bitten"]
        self.word3 = ["apple-john", "baggage", "barnacle", "bladder", "boar-pig", "bugbear", "bum-bailey", "canker-blossom", "clack-dish", "clotpole", "coxcomb", "codpiece", "death-token", "dewberry", "flap-dragon", "flax-wench", "flirt-gill", "foot-licker", "fustilarian", "giglet", "gudgeon", "haggard",	"harpy", "hedge-pig", "horn-beast", "hugger-mugger", "joithead", "lewdster", "lout", "maggot-pie", "malt-worm", "mammet", "measle", "minnow", "miscreant", "moldwarp", "mumble-news", "nut-hook", "pigeon-egg", "pignut", "puttock", "pumpion", "ratsbane", "scut", "skainsmate", "strumpet", "varlot", "vassal", "whey-face", "wagtail"]
        self.roasts = ["I'd offer you some gum but your smiles got plenty of it.", "Repeat after me: semen is not hair gel.", "Your body fat is about as evenly distributed as wealth in the US economy." "You are proof evolution can go in reverse." "I wasn't born with enough middle fingers to let you know how I feel about you.", "Your birth certificate is an apology letter from the condom factory."]
        self.help_message = """
```
General commands:
>help - displays all the available commands
>clear amount - will delete the past messages with the amount specified
Spiritual connect:
>thought - randomly displays a cool thought 😎
Music commands:
>p <keywords> - finds the song on youtube and plays it in your current channel
>q - displays the current music queue
>skip - skips the current song being played
>dc - leaves the voice channel and stops playing all the songs
Fun section:
>sh_roast - light-heartedly roasts the tagged person in Shakespearnean English. Caution: THIS CAN BE EXTREMELY OFFENSIVE 😲😲
>roast - randomly roasts the tagged person in *REGULAR* English
```
"""
        self.text_channel_list = []

    #some debug info so that we know the bot has started          

    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)

    @commands.command(name="clear", help="Clears a specified amount of messages")
    async def clear(self, ctx, arg):
        #extract the amount to clear
        amount = 5
        try:
            amount = int(arg)
        except Exception: pass

        await ctx.channel.purge(limit=amount)
    
    @commands.command(name="sh_roast", help="Roasts the tagged user by saying something random")
    async def sh_roast(self, ctx):
        members = ctx.message.mentions
        if(len(members) == 0):
            await ctx.send(f"I don't know who to roast, {ctx.author.mention}")
        else:
            mes = ''
            for ind in range(len(members)):
                w1_ind = random.randint(0, len(self.word1)-1)
                w2_ind = random.randint(0, len(self.word2)-1)
                w3_ind = random.randint(0, len(self.word3)-1)
                mes += f"{members[ind].mention}, thou " + self.word1[w1_ind] + " " + self.word2[w2_ind] + " " + self.word3[w3_ind] + '\n'
            await ctx.send(mes)
