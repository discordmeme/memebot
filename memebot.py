import discord, asyncio

bot = discord.Client(max_messages=100)

@bot.event
async def on_ready():
    print("Logged in as", bot.user.name, "#", bot.user.discriminator)
    await bot.change_presence(game=discord.Game(name="www.discordme.me", type=0))
    if not discord.opus.is_loaded():
        discord.opus.load_opus("libopus.so")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content.lower() == "!nicememe":
        if message.channel.is_private:
            pass
        elif message.author.voice.voice_channel != None and message.server.me.voice.voice_channel == None:
            voicechannel = message.author.voice.voice_channel
            perms = message.server.me.permissions_in(voicechannel)
            if perms.connect and perms.speak:
                try:
                    voice = await bot.join_voice_channel(voicechannel)
                    player = voice.create_ffmpeg_player("nicememe.mp3")
                    player.start()
                    while True:
                        if player.is_done():
                            await asyncio.sleep(0.5)
                            await voice.disconnect()
                            break
                        else:
                            await asyncio.sleep(1)
                except Exception as error:
                    print(error)
            else:
                if message.channel.permissions_for(message.server.me).send_messages:
                    await bot.send_message(message.channel, "I need the `connect` and `speak` permissions to work!")
    elif message.content.lower() == "!invite" and (message.channel.is_private or message.channel.permissions_for(message.server.me).send_messages):
        await bot.send_message(message.channel, "<http://discordme.me/invite>")
    elif message.content.lower() == "!help" and (message.channel.is_private or message.channel.permissions_for(message.server.me).send_messages):
        await bot.send_message(message.channel, "`!nicememe` - `plays 'nice meme' in your voice channel`\n`!invite` - `obtain the bot invite link`")
    elif message.content.lower().startswith("!eval") and message.author.id == "146726280245673984":
        try:
            await bot.send_message(message.channel, content="```py\n" + str(eval(message.content[6:])) + "```")
        except Exception as e:
            await bot.send_message(message.channel, "```py\n" + repr(e) + "```")

bot.run("token")
