print("Loading the \"mods\" module.")
import ast
import discord
import os
import subprocess
import sys
from discord.ext import commands

nouser = "No user provided."
selfcommand = "You cannot run this on yourself."

class mods(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.User = None, reason=""):
        '''Ban Users. Admin+'''
        if not member:
            await ctx.channel.send(nouser)
            return
        elif member == ctx.message.author:
            await ctx.channel.send(selfcommand)
            return
        reasonraw = ctx.message.content[28:]
        message = f"You have been banned from {ctx.guild.name} for the reason {reasonraw}"
        await ctx.guild.ban(member, reason=reasonraw, delete_message_days=0)
        await ctx.channel.send(f"{member} has been b&. 👍")
        await member.send(message)

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def probate(self, ctx, member: discord.Member = None):
        '''Locks a user to a single channel. Mods+'''
        if not member:
            await ctx.channel.send(nouser)
            return
        elif member == ctx.message.author:
            await ctx.channel.send(selfcommand)
            return

        probateRole = member.guild.get_role(1056074333648338954)
        if probateRole is None:
            await ctx.channel.send("Probate role not found.")
            return
        
        else:
            try:
                await member.edit(roles=[probateRole])
                await ctx.channel.send(f'{member} has been probated.')
            except Exception as e:
                await ctx.channel.send(f'Exception encountered while probating: {e}')

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def unprobate(self, ctx, member: discord.Member = None):
        '''Removes a user from probation.  Mods+'''
        if not member:
            await ctx.channel.send(nouser)
            return
        elif member is ctx.message.author:
            await ctx.channel.send("Either you are stupid enough to try this or you had no idea what would happen. Most likely the former.")

        virginRole = member.guild.get_role(918319461688295484)
        if virginRole == None:
            await ctx.channel.send("Virgin role not found.")
            return

        else:
            try:
                await member.edit(roles=[virginRole])
                await ctx.channel.send(f'{member} has been released from the shadow realm.')
            except Exception as e:
                await ctx.channel.send(f'Exception encountered while unprobating: {e}')
                
    @commands.command()
    async def on_message(self, message: discord.Message):
        if message.author.name == "GitHub" and message.author.discriminator == "0000":
            if message.embeds[0].title.startswith("[keybot:master]"):
                await self.bot.change_presence(status=discord.Status.do_not_disturb)
                await message.add_reaction("\U0001F6D1")

                subprocess.call(["git", "pull", "origin", "master"])
                if os.name == "posix":
                    main_path = f'[\'{sys.argv[0]}\']'
                elif os.name == "nt":
                    main_path = f'[\'"{sys.argv[0]}"\']'
                main_path = ast.literal_eval(main_path)

                await message.add_reaction("\U0000267B")
                
                if os.name == "posix":
                    os.execv(sys.executable, ["python3"] + main_path)
                if os.name == "nt":
                    os.execv(sys.executable, ["python"] + main_path)
        
async def setup(bot):
    await bot.add_cog(mods(bot))
