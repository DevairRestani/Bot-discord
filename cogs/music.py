import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""
        self.volume = 1.0
        self.playing_now = ""

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
            self.playing_now = self.music_queue.pop(0)

            self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(m_url, executable='ffmpeg.exe', **self.FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.play_next())
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
            self.playing_now = self.music_queue.pop(0)
            
            if len(self.music_queue) > 0:
                self.play_next()
            else:
                self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(m_url, executable='ffmpeg.exe', **self.FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            await self.vc.disconnect()

    @commands.command(name="help",alisases=['ajuda'],help="Comando de ajuda")
    async def help(self,ctx):
        helptxt = ''
        for command in self.client.commands:
            helptxt += f'**{command}** - {command.help}\n'
        embedhelp = discord.Embed(
            colour = 1646116,#grey
            title=f'Comandos do {self.client.user.name}'
        )
        embedhelp.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embedhelp)


    @commands.command(name="play", help="Toca uma música do YouTube",aliases=['p','tocar'])
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        try:
            voice_channel = ctx.author.voice.channel
        except:
        #if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = 'Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await ctx.send(embed=embedvc)
            return
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                embedvc = discord.Embed(
                    colour= 12255232,#red
                    description = 'Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed=embedvc)
            else:
                embedvc = discord.Embed(
                    colour= 32768,#green
                    description = f"Você adicionou a música **{song['title']}** à fila!)"
                )
                await ctx.send(embed=embedvc)
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Mostra as atuais músicas da fila.",aliases=['q','fila'])
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f'**{i+1} - **' + self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            embedvc = discord.Embed(
                colour= 12255232,
                description = f"{retval}"
            )
            await ctx.send(embed=embedvc)
        else:
            embedvc = discord.Embed(
                colour= 1646116,
                description = 'Não existe músicas na fila no momento.'
            )
            await ctx.send(embed=embedvc)

    @commands.command(name="skip", help="Pula a atual música que está tocando.",aliases=['pular', 'sk'])
    @commands.has_permissions(manage_channels=True)
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()
            embedvc = discord.Embed(
                colour= 1646116,#ggrey
                description = f"Você pulou a música."
            )
            await ctx.send(embed=embedvc)
        
    @commands.command(name="stop", help="Para a música que está tocando.",aliases=['parar'])
    @commands.has_permissions(manage_channels=True)
    async def stop(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você parou a música."
            )
            await ctx.send(embed=embedvc)

    @commands.command(name="pause", help="Pausa a música que está tocando.",aliases=['pausar'])
    @commands.has_permissions(manage_channels=True)
    async def pause(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.pause()
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você pausou a música."
            )
            await ctx.send(embed=embedvc)
    
    @commands.command(name="resume", help="Resume a música que está tocando.",aliases=['resumir'])
    @commands.has_permissions(manage_channels=True)
    async def resume(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.resume()
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você resumiu a música."
            )
            await ctx.send(embed=embedvc)
        
    @commands.command(name="volume", help="Ajusta o volume da música.",aliases=['vol'])
    @commands.has_permissions(manage_channels=True)
    async def volume(self, ctx, volume: int):
        if self.vc != "" and self.vc:
            self.vc.source.volume = volume/100
            self.volume = volume/100
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você ajustou o volume para **{volume}%**."
            )
            await ctx.send(embed=embedvc)
    
    @commands.command(name="nowplaying", help="Mostra a música que está tocando.",aliases=['np','atual'])
    async def nowplaying(self, ctx):
        if self.vc != "" and self.vc:
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Está tocando: **{self.playing_now[0]['title']}**"
            )
            await ctx.send(embed=embedvc)
        else:
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = 'Não há nada tocando no momento.'
            )
            await ctx.send(embed=embedvc)

    @commands.command(name="ping", help="Mostra o ping do bot.")
    async def ping(self, ctx):
        embedvc = discord.Embed(
            colour= 1646116,#grey
            description = f"O ping do bot é **{round(self.client.latency*1000)}ms**"
        )
        await ctx.send(embed=embedvc)

    
    @skip.error #Erros para kick
    async def skip_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            embedvc = discord.Embed(
                colour= 12255232,
                description = f"Você precisa da permissão **Gerenciar canais** para pular músicas."
            )
            await ctx.send(embed=embedvc)     
        else:
            raise error

def setup(client):
    client.add_cog(music(client))