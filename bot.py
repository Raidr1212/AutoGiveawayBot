import discum     
import config
import telegram_send

bot = discum.Client(token=config.token, log={"console":False, "file":False})
@bot.gateway.command
def Raidr(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        bot.gateway.subscribeToGuildEvents(wait=1)
    if resp.event.message:
        m = resp.parsed.auto()
        guildID = m['guild_id'] if 'guild_id' in m else None #because DMs are technically channels too
        channelID = m['channel_id']
        username = m['author']['username']
        userId = m['author']['id']
        messageID = m['id']
        discriminator = m['author']['discriminator']
        content = m['content'] 
        link = "https://discord.com/channels/"+guildID+"/"+channelID+"/"+messageID
        if(userId == config.giveawayBotID):
            print("> guild {} channel {} | {}#{}: {}".format(guildID, channelID, username, discriminator, content))
            if(content.startswith('<:yay:585696613507399692>   **GIVEAWAY**')):
                if(config.telegramNotifications == 1):
                    telegram_send.send(messages=["🔔 | "+content+"\n"+link],disable_web_page_preview=True,silent=True)
                bot.addReaction(channelID,messageID,'🎉')
            if(content.startswith('Congratulations <@'+bot.gateway.session.user['id'])):
                if(config.telegramNotifications != 0):
                    telegram_send.send(messages=["🎉 | "+content+"\n"+link],disable_web_page_preview=True)
                print(content)


        

bot.gateway.run(auto_reconnect=True)