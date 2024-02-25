import os
from discord.ext import commands
from datetime import datetime, timedelta
from googletrans import Translator
import discord
from keep_alive import keep_alive




message_lastseen = datetime.now()
message2_lastseen = datetime.now()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

Token = os.getenv('TOKEN')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def repeat(ctx,arg):
    await ctx.send(arg)

@bot.command(name="ban", help="command to ban user")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """ command to ban user. Check !help ban """
    try:
        await member.ban(reason=reason)
        await ctx.channel.send(f'{member.name} has been banned from server'
                               f'Reason: {reason}')
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission to ban someone. Upgrade the Permissions")


@bot.command(name="unban", help="command to unban user")
@commands.has_permissions(administrator=True)
async def unban(ctx, *,member_id: int ):
    """ command to unban user. check !help unban """
    await ctx.guild.unban(discord.Object(id=member_id))
    await ctx.send(f"Unban {member_id}")

@bot.command(name="kick", help="command to kick user")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """ command to kick user. Check !help kick """
    try:
        await member.kick(reason=reason)
        await ctx.channel.send(f'{member.name} has been kicked from server'
                               f'Reason: {reason}')
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission to kick someone. Upgrade the Permissions")

@bot.command(name="timeout",help="command to time out ")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: discord.Member, time, reason=None):
    """ command to timeout user. Check !help timeout """
    try:
     if ctx.author.id == member.id: 
        await ctx.channel.send(":x: You can't ban yourself!")
        return
     if "s" in time:
        time.replace("s","")
        print(time)
        await member.timeout_for(until=datetime.timedelta(hours=time), reason=reason)
     if "h" in time:
        time.replace("h","")
        print(time)
        await member.timeout_for(until=datetime.timedelta(hours=time), reason=reason)
     if "h" in time:
        time.replace("h","")
        print(time)
        await member.timeout_for(until=datetime.timedelta(hours=time), reason=reason)
     elif "d" in time:
        time.replace("d","")
        print(time)
        await member.timeout_for(until=datetime.timedelta(days=time), reason=reason)
     await ctx.channel.send(f'{member.name} has been timed out'
                               f'Reason: {reason}')
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission to time out. Upgrade the Permissions")

@bot.command(name="remove timeout",help="command to remove timeout ")
@commands.has_permissions(moderate_members = True)
async def removetimeout(ctx, member: discord.Member):
    try:
        if not member.is_time_out():
            await ctx.channel.send(f'{member.name} ')
        else:
            await member.edit(timed_out_until=None)
            await ctx.channel.send(f'{member.name} has been unmuted')
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")


@bot.command(name="addrole",help="command to addrole ")
@commands.has_permissions(manage_roles = True)
async def addrole(ctx, member: discord.Member,role: discord.Role):
    """ command to addrole . Check !help addrole """
    try:
        await bot.add_roles(member,role)
        await ctx.channel.send(f'add role {role.name} to {member.name} '
                               )
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")

@bot.command(name="removerole",help="command to removerole ")
@commands.has_permissions(manage_roles = True)
async def removerole(ctx, member: discord.Member,role: discord.Role):
    """ command to removerole . Check !help removerole """
    try:
        await bot.remove_roles(member,role)
        await ctx.channel.send(f'remove role {role.name} to {member.name} '
                               )
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")

@bot.command(name="move",help="command to move user")
@commands.has_permissions(move_members = True)
async def move(ctx, member: discord.Member,channelID):
    """ command to move user . Check !help move """
    try:
        channel = bot.get_channel(channelID)
        await member.move_to(channel, reason=None)
        await ctx.channel.send(f'move {member.name} to {channel.name} '
                               )
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")

@bot.command(name="disconnected",help="disconnect user")
@commands.has_permissions(move_members = True)
async def disconnect(ctx, member: discord.Member):
    """ command to disconnect . Check !help disconnect """
    try:
        guild = bot.get_guild(id)
        member = guild.get_member(id)
        await member.move_to(channel=None)
        await ctx.channel.send(f'disconnect {member.name} from {channel.name} '
                               )
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")


@bot.command()
@commands.has_permissions(ban_members = True)
async def deafen(ctx, member: discord.Member):
    try:
        role = discord.utils.get(member.server.roles, name='Deafened')
        await bot.add_roles(member, role)
        embed=discord.Embed(title="User Deafened!", description="**{0}** was deafened by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
        await bot.say(embed=embed)
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")

@bot.command()
@commands.has_permissions(ban_members = True)
async def undeafen(ctx, member: discord.Member):
    try:
        await member.edit(Deafened=False)
        await ctx.channel.send(f' {member.name} has been undeafened '
                               )
    except Exception:
        await ctx.channel.send(f"Bot doesn't have enough permission. Upgrade the Permissions")

@bot.command()
@commands.has_permissions(read_message_history = True)
async def history(ctx, *, word: str,channelID):
    channel = bot.get_channel(channelID)
    messages = await ctx.channel.history(limit=200).flatten()

    for msg in messages:
        if word in msg.content:
            print(msg.jump_url)

@bot.command()
async def translate(ctx, lang, *, thing):
    """ command to translate . Check !help translate """
    try:
        translator = Translator()
        translation = translator.translate(thing, dest=lang)
        await ctx.channel.send(f'Translate to {lang}: {translation.text}'
                              )     
    except Exception:
        await ctx.channel.send(f"Translation failed")

@bot.event
async def on_message(message):
    if message.content == '!hello':
        await message.channel.send("hi")    

    if message.content == '!What is your name':
        await message.channel.send("my name is " + str(bot.user.name))
    await bot.process_commands(message)

@bot.command()
async def guide(ctx):
    embed=discord.Embed(title="How to use siren",description = "All availble commands", color = 0x80cbc4)
    embed.add_field(name="!help",value="get help command",inline=False)
    embed.add_field(name="!repeat",value="respond messages that you've send",inline=False)
    embed.add_field(name="!ban",value="ban user",inline=False)
    embed.add_field(name="!unban",value="unban user",inline=False)
    embed.add_field(name="!kick",value="kick user",inline=False)
    embed.add_field(name="!timeout",value="mute user",inline=False)
    embed.add_field(name="!removetimeout",value="unmute user",inline=False)
    embed.add_field(name="!move",value="move user",inline=False)
    embed.add_field(name="!addrole",value="add role to user",inline=False)
    embed.add_field(name="!removerole",value="remove role from user",inline=False)
    embed.add_field(name="!deafen",value="deafen user",inline=False)
    embed.add_field(name="!undeafen",value="undeafen user",inline=False)
    embed.add_field(name="!history",value="jump to the word that you want",inline=False)
    embed.add_field(name="!hello",value="bot say hi to user",inline=False)
    embed.add_field(name="!What is your name",value="bot say its name",inline=False)
    embed.add_field(name="!translate",value="translate a message",inline=False)
    await ctx.channel.send(embed=embed)


@bot.command()
async def translatelang(ctx):
    embed=discord.Embed(title="list of language code",description = "https://gist.github.com/alexanderjulo/4073388", color = 0x80cbc4)
    await ctx.channel.send(embed=embed)



@bot.event 
async def on_member_join(member):
    channel = bot.get_channel(1096045908707258471)
    text = f"Welcome {member.mention}"
    em = discord.Embed(title = 'Welcome to the server!', description = text, color = 0x0066FF)
    await message.channel.send(text)
    await message.channel.send(embed= em)
    await bot.process_commands(message)

@bot.event 
async def on_member_remove(member):
    channel = bot.get_channel(1096045908707258471)
    await message.channel.send(f"Bye {member.mention}")
    await bot.process_commands(message)

keep_alive()

bot.run(Token)
