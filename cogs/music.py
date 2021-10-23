import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.voice_client import VoiceProtocol

from pytube import YouTube, Playlist, Search

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc: VoiceProtocol = None 
        self.volume = 1.0
        self.playing_now = ""

    #searching the item on youtube
    def search_yt(self, item):
        res = []
        try:
            if "playlist" in item:
                pl = Playlist(item)
                for video in pl.videos:
                    res.append(video)
            elif "https://youtu.be" in item or "https://www.youtube.com" in item or "https://music.youtube.com" in item:
                res.append(YouTube(item))
            else:
                res.append(Search(item).results[0])

        except:
            return None

        
        return res


    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            last_song = self.music_queue.pop()
            song: YouTube = last_song[0]
            s_url = song.streams.filter(only_audio=True).first().url

            #remove the first element as you are currently playing it
            self.playing_now = song.title

            self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(s_url, executable='ffmpeg.exe', **self.FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            last_song = self.music_queue.pop()
            song: YouTube = last_song[0]
            voiceChannel: VoiceChannel = last_song[1]

            s_url = song.streams.filter(only_audio=True).first().url
            
            #try to connect to voice channel if you are not already connected

            if self.vc == None or not self.vc.is_connected() or self.vc == None:
                self.vc = await voiceChannel.connect()
            else:
                await self.vc.move_to(voiceChannel)
            
            #remove the first element as you are currently playing it
            self.playing_now = song.title
            
            if len(self.music_queue) > 0:
                self.play_next()
            else:
                self.vc.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(s_url, executable='ffmpeg.exe', **self.FFMPEG_OPTIONS), volume=self.volume), after=lambda e: self.play_next())
        else:
            self.is_playing = False
            await self.vc.disconnect()


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
            songs = self.search_yt(query)
            if type(songs) == type(True):
                embedvc = discord.Embed(
                    colour= 12255232,#red
                    description = 'Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed=embedvc)
            else:
                if songs == None:
                    embedvc = discord.Embed(
                        colour= 12255232,#red
                        description = 'Ocorreu um erro!'
                    )
                    await ctx.send(embed=embedvc)
                if len(songs) == 0:
                    embedvc = discord.Embed(
                        colour= 12255232,#red
                        description = 'Não encontrei nenhum resultado para a pesquisa!'
                    )
                    await ctx.send(embed=embedvc)
                elif len(songs) == 1:
                    embedvc = discord.Embed(
                        colour= 32768,#green
                        description = f"Você adicionou a música **{songs[0].title}** à fila!)"
                    )
                elif len(songs) > 1:
                    embedvc = discord.Embed(
                        colour= 32768,#green
                        description = f"Você adicionou play list!)"
                    )
                await ctx.send(embed=embedvc)

                for i in songs:
                    self.music_queue.append([i, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Mostra as atuais músicas da fila.",aliases=['q','fila'])
    async def q(self, ctx):
        retval = ""

        if len(self.music_queue) == 0:
            embedvc = discord.Embed(
                colour= 1646116,
                description = 'Não existe músicas na fila no momento.'
            )
            await ctx.send(embed=embedvc)

        for i in range(0, len(self.music_queue)):
            retval += f'**{i+1} - **' + self.music_queue[i][0].title + "\n"
            if len(retval) > 4000:
                embedvc = discord.Embed(
                    colour= 12255232,
                    description = f"{retval}"
                )
                await ctx.send(embed=embedvc)
                retval = ""
            

    @commands.command(name="skip", help="Pula a atual música que está tocando.",aliases=['pular', 'sk'])
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
    async def stop(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você parou a música."
            )
            await ctx.send(embed=embedvc)

    @commands.command(name="pause", help="Pausa a música que está tocando.",aliases=['pausar'])
    async def pause(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.pause()
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você pausou a música."
            )
            await ctx.send(embed=embedvc)
    
    @commands.command(name="resume", help="Resume a música que está tocando.",aliases=['resumir'])
    async def resume(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.resume()
            embedvc = discord.Embed(
                colour= 1646116,#grey
                description = f"Você resumiu a música."
            )
            await ctx.send(embed=embedvc)
        
    @commands.command(name="volume", help="Ajusta o volume da música.",aliases=['vol'])
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
                description = f"Está tocando: **{self.playing_now}**"
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
    
    @commands.command(name="clear", help="Limpa a fila de músicas.",aliases=['limpar'])
    async def clear(self, ctx):
        self.music_queue = []
        embedvc = discord.Embed(
            colour= 1646116,#grey
            description = f"A fila foi limpa."
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