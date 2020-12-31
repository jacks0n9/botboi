import time
import sqlite3
import praw
import discord
import random
from discord.ext import commands
from discord.ext.commands.core import has_permissions
from prawcore.exceptions import Redirect
reddit=praw.Reddit('bot1')
client = commands.Bot(command_prefix="&")
client.remove_command("help")

@client.event
async def on_ready():
    print(f"Bot engaged. Logged in as: {client.user}")
    await client.change_presence(activity=discord.Game(name="Vscode, copying Dyno one command at a time."))


@client.command(name="ping")
async def pong(ctx):
    await ctx.send("pong")
    message=ctx.message
    await message.add_reaction(str("🏓"))


@client.command(name="echo")
async def echoer(ctx,*args):
    await ctx.send(' '.join(args))


@client.command(name="dm")
async def sendadm(ctx, member: discord.Member, *message):
    await member.send(' '.join(message)+ f"\n \n This message was sent on behalf of {ctx.author}")
    message=ctx.message
    await message.add_reaction(str("📤"))



@client.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kickpeep(ctx,member: discord.Member, *reason):
        reason=' '.join(reason)
        if reason == '':
            reason = "Deserves to be kicked"
        await member.kick(reason=reason)
        embed=discord.Embed(title=f"Kicked {member} for reason: "+reason,color=0x72d345)

        await ctx.send(embed=embed)
        message=ctx.message
        await message.add_reaction(str("👋"))
        if not member.bot:
            await member.send(f"You have been kicked from the server by {ctx.author} for reason: {reason}")
@kickpeep.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to kick members!')   


@client.command(name="ban")
@commands.has_permissions(ban_members=True)
async def banpeep(ctx,member: discord.Member, *reason):
    reason=' '.join(reason)
    if reason == '':
        reason = "Deserves to be banned"
    await member.ban(reason=reason)
    embed=discord.Embed(title=f"Banned {member} for reason: "+reason,color=0x72d345)
    await ctx.send(embed=embed)
    message=ctx.message
    await message.add_reaction(str("🔫"))
    if not member.bot:
        await member.send(f"You have been banned from the server by {ctx.author} for reason: {reason}")
@banpeep.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to ban members!')
    



@client.command(name="reddit")
async def choosepost(ctx,subreddit):
    try:
        sub=reddit.subreddit(subreddit)
        posts=[]
        for post in sub.hot():
            if not post.over_18:
                posts.append(post)
        rand=random.randint(1,98)
        post=posts[rand]
        embed=discord.Embed(title=post.title,url=f"https://reddit.com/r/{subreddit}/comments/{post.id}",color=0x72d345)
        embed.set_image(url=post.url)
        await ctx.send(embed=embed)
    except Redirect:
        await ctx.send("Subreddit not found, try a different one")

@client.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx,member:discord.Member):
    print(ctx.guild.roles)
    silencedrolearray=[]
    silencedrolename="serversilenced"
    for role in ctx.guild.roles:
        if role.name==silencedrolename:
            silencedrolearray.append(role)
            print(role)
    if len(silencedrolearray) > 1:
        await ctx.send(f"You have multiple roles named {silencedrolename}, which is the name of the role that we use to silence members, please delete all roles that have that name.")
        return
    elif len(silencedrolearray) ==0:
        print("creating role")
        role=await ctx.guild.create_role(name=silencedrolename)
        silencedrolearray.append(role)
        print("Created roel")
    print(silencedrolearray)
    first=silencedrolearray[0]
    print("Addign roles")
    await member.add_roles(first)
    
    await ctx.send(f"Muted {member} successfully")

@mute.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to mute members! Make sure you have the manage roles permission!')

@client.command(name="help")
async def givehelp(ctx):
    embed=discord.Embed(title="Bot Boi Help:",description="Ping: I will respond with 'pong' if I am online.\nEcho: Type '&echo [message to echo]' and I will repeat the message\nDm: Send dm to a member of the server. Use it by typing '&dm @[user] [message you want to send]'\nReddit: Reddit integration for discord. Use it by typing '&reddit [subreddit]' and it will pick a random post from that subreddit\nModerator Commands:\nBan: Ban a member. Use it by typing '&ban @[user] [reason]'\nKick: Kicks a member. Use it by typing '&kick @[user] [reason]'\nPurge: Delete certain amount of messages from a channel. Use by typing: '&purge [amount of messages to delete].'\nClearpins: Clear all pinned messages from a channel, may take up to a minute depending on how many messages there are in the channel.\nAddrole: Add a role to a user. Use it by typing '&addrole @[member] @[role]'.\nRemoverole: Remove a role from a user. Use by typing '&removerole @[member] @[role]'",color=0x72d345)
    await ctx.send(embed=embed)



@client.command(name="clearpins")
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    message = await ctx.send("Removing all pinned messages in this channel")
    history=await message.channel.history(limit=None).flatten()
    for message in history:
        if message.pinned:
            await message.unpin()
@clear.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to clear pinned messages!')
    


@client.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx,num):
    print()
    try:
        int(num)
        message=await ctx.send(f"Purging last {str(num)} messages.")
        history=await message.channel.history(limit=int(num)).flatten()
        for message in history[0:int(num)]:
            await message.delete()
        deleted = await ctx.send(f"Done purging {str(num)} messages!")
        time.sleep(5.0)
        await deleted.delete()
            
    except ValueError:
        await ctx.send("Not a number!")
@purge.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to purge messages!')



@client.command(name="addrole")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx,member: discord.Member,role: discord.Role):
        user=member
        mention=f"<@{member.id}>"
        await user.add_roles(role)
        await ctx.send(f"Added role {role} to {mention}")
@addrole.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to manage roles!')
    


@client.command(name="removerole")
@commands.has_permissions(manage_roles=True)
async def removerole(ctx,member: discord.Member,role: discord.Role):
    user=member
    mention=f"<@{member.id}>"
    await user.remove_roles(role)
    await ctx.send(f"Removed role {role} from {mention}")
@removerole.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to manage roles!')
   


@client.command(name="strike")
@commands.has_permissions(ban_members=True)
async def givestrike(ctx,user: discord.Member):
    author = ctx.author
    conn=sqlite3.connect("data.db")
    cursor=conn.cursor()
    message=await ctx.send(f"Please confirm strike on {user} by reacting to this message with the check mark or react with x to cancel.")
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    @client.event
    async def on_raw_reaction_add(payload):
        if payload.message_id == message.id:
            if payload.member == author:
                if payload.emoji.name =="✅":
                    con=f"Strike confirmed on {user}"
                    await message.edit(content=con)
                    cursor.execute('''
                        create table if not exists servers (
                            guildid int

                        
                        
                        );
                     ''')
                elif payload.emoji.name == "❌":
                    await ctx.message.delete()
                    await message.delete()
                else:
                    await ctx.send("Unknown reaction not doing anything")
            elif payload.member==message.author:
                print("Bot voted, not doing anything")
            else:
                await ctx.send("You aren't the issuer of the ban, so you don't have permission to cancel or confirm it!")
@givestrike.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Sorry you are not allowed to strike members!')


@client.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.channels, name="general")
    channel_id=channel.id
    embed=discord.Embed(title="Thanks for inviting me to your server!",description="To get started, type &help to get a list of commands!\nRemember to prefix '&' before your command so I can understand it.",color=0x72d345)
    await channel.send(embed=embed)
    

key=open("key.txt",'r').read() 
client.run(key)



