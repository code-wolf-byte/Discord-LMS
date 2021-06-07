import discord
from discord.ext import commands
import asyncio
import requests
import datetime
import ast



def perms_to_move():
    async def predicate(ctx):
        if ctx.author.guild_permissions.move_members:
            return True
        else:
            await ctx.send(f"Sorry you don't have permissions for that, {ctx.author.mention}")

    return commands.check(predicate)


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[!] Move initializing...")
        print(f"[!] Move initialization complete!")
        await self.bot.change_presence(activity=discord.Game(name="School Scripts"))

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        # TODO: Update control panel when channels are created, deleted, and moved
        if before.id in self.message_to_channel.values() and before.name != after.name:
            if self.control_panel:
                for mid, cid in self.message_to_channel.items():
                    if before.id == cid:
                        msg = await self.control_panel.fetch_message(mid)
                        if msg:
                            await msg.edit(embed=discord.Embed(title=f'**{after.name}**'))
                        else:
                            self.error('Control panel message not found!')
                        return
            else:
                self.error('Unknown error in "on_guild_channel_update"')

    ######################################## HELPER FUNCTIONS ############################################

    def error(self, msg):
        print(f"[!] Error: {msg}")

    def _any_null(self, *args):
        for a in args:
            if a is None:
                return True
        return False

    def _get_channel(self, server, chname: str) :
        for channel in server.channels:
            if type(channel) is discord.channel.VoiceChannel and chname.lower() in channel.name.lower():
                return channel
        return None


    async def _mbr_helper(self, server, role_name: str, src_channel, dst_channel) -> None:
        role = self._get_role(server, role_name)
        if role:
            all_members = src_channel.members
            for member in all_members:
                if role in member.roles:
                    await member.move_to(dst_channel)

    def _get_role(self, server, role_name: str) -> discord.Role:
        for role in server.roles:
            if role_name.lower() in role.name.lower():
                return role
        return None



########################################################################################################################


    @commands.command()
    async def send(self,ctx, member: discord.Member, *, content):
        server = ctx.message.guild
        print(server.name)
        channel = await member.create_dm()
        await channel.send(content)

    @commands.command()
    async def send_dm(self, ctx, member: discord.Member, * , content):
        server = ctx.message.guild
        url = ctx.message.attachments[0].url
        url_split = url.split('/')
        file_name = url_split.pop()
        file = requests.get(url)
        print(file_name)
        print(server.name)

        channel = await member.create_dm()
        send = "============================================ \n"+"From:"+ ctx.author.name+"  at  "+ctx.guild.name + '\n' + content + "\n ============================================ "
        await channel.send(send)
        await channel.send(discord.file(file))

    @commands.command()
    async def verify(self, ctx):
        server = ctx.message.guild
        channel = ctx.message.channel
        user_id = ctx.author.id
        member = ctx.author
        data = None
        with open('data.txt') as fileread:
            x = fileread.read()
            data = ast.literal_eval(x)
        fileread.close()
        flag = False
        for id in data.keys():
            if id != user_id:
                continue
            flag = True
        if flag:
            nickname = data[user_id]
            await member.edit(nick=nickname)
        else:
            try:
                await channel.send("Please enter your name: (You have 60 seconds to complete the verification)")
                msg = await self.bot.wait_for("message", timeout=60)
                txt = msg.content
                data[user_id] = txt
                wrt = str(data)
                file = open('data.txt','w')
                file.write(wrt)
                file.close()
                await member.edit(nick=txt)

            except asyncio.TimeoutError:
                await channel.send("Sorry You did not reply in time")
                await channel.send("Please run the !verify command again")


async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None:
        await ctx.send("You did not mention a channel!")
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()

    @commands.command()
    async def info(self,ctx,user):
        server = ctx.message.guild
        members = server.members
        for member in members:
            if member.name == user:
                await ctx.channel.send(member)

    @commands.command()
    async def assignment(self,ctx,*name):
        server = ctx.message.guild
        ch = ''
        for n in name:
            ch= ch +n
            ch= ch+'-'
        bot_channel = discord.utils.get(ctx.guild.channels, name='assignment-issue')
        await bot_channel.clone(name=ch)
        channel = discord.utils.get(ctx.guild.channels, name='assignment-issue')
        await channel.clone(name=ch+'-submission')

    @commands.command()
    async def check(self,ctx,*name):
        ch = ''
        for n in name:
            ch = ch + n
            ch = ch + ' '

    @commands.command()
    async def status(self,ctx,*name):
        server = ctx.message.guild
        ch = ''
        for n in name:
            ch = ch + n
            ch = ch + '-'
        ch= ch+'-submission'
        channel = discord.utils.get(ctx.guild.channels, name=ch)
        


    @commands.command()
    async def move(self, ctx, role_name: str, dst_name: str):
        server = ctx.message.guild
        dst_channel = self._get_channel(server, dst_name)
        got_role = self._get_role(server, role_name)
        all_members = server.members

        if self._any_null(dst_channel, got_role):
            null_names = [name for obj, name in [(dst_channel, dst_name), (got_role, role_name)] if obj is None]
            await ctx.send(f"Sorry, {' and '.join(null_names)} could not be found.")
            return

        for member in all_members:
            if (member.voice is not None and member.voice.channel != dst_channel):
                for role in member.roles:
                    if role == got_role:
                        await member.move_to(dst_channel)

    @commands.command()
    async def attendence(self,ctx,role_name:str,chn_name:str):
        server = ctx.message.guild
        dst_channel = self._get_channel(server, chn_name)
        got_role = self._get_role(server, role_name)
        members = server.members
        ch = 'attendence-log'
        channel = discord.utils.get(server.channels, name=ch)
        str = "Attendence requested by "+ ctx.message.author.name +" at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for member in members:
            if (member.voice is not None and member.voice.channel == dst_channel and not member.voice.afk ):
                for role in member.roles:
                    if role == got_role:
                        print(member.nick)
                        str = str.append(member.nick)
        await channel.send(str)
#########################################################################################################################


    def reaction_add_check(self, reaction, user):
        requirements = \
            (
                user != self.bot.user,
                reaction.emoji == EMOJI,
                reaction.message.guild.get_member(user.id).guild_permissions.move_members,
                reaction.message.channel == self.control_panel,
                reaction.message.id in self.message_to_channel
            )
        return all(requirements)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.reaction_add_check(reaction, user):
            def check(r, u):
                return r.emoji == EMOJI and u == user and r.message.id in self.message_to_channel
            try:
                next_reaction, _ = await self.bot.wait_for('reaction_add', check=check, timeout=3)
                dst_channel = self.bot.get_channel(self.message_to_channel[next_reaction.message.id])
            except asyncio.TimeoutError:
                await reaction.message.remove_reaction(EMOJI, user)
                return

            src_channel = self.bot.get_channel(self.message_to_channel[reaction.message.id])
            members_to_move = [member.move_to(dst_channel) for member in src_channel.members]
            await asyncio.gather(*members_to_move)
            await reaction.message.remove_reaction(EMOJI, user)
            await next_reaction.message.remove_reaction(EMOJI, user)
            print(f"{user.display_name}/{user.name} moved everyone from {src_channel.name} to {dst_channel.name}")





