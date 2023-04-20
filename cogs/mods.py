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
    async def ban(self, ctx, member: discord.User = None, *, reason = None):
        '''Ban Users. Admin+'''
        if not member:
            await ctx.channel.send(nouser)
            return
        elif member == ctx.message.author:
            await ctx.channel.send(selfcommand)
            return
        message = f"You have been banned from {ctx.guild.name} for the following reason:\n" + reason
        await member.send(message)
        await ctx.guild.ban(member, reason=reason, delete_message_days=0)
        await ctx.channel.send(f"{member} has been b&. 👍")

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, userId: discord.User.id):
        user = get(id=userId)
        await ctx.guild.unban(user)

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

        probate_role = member.guild.get_role(1056074333648338954)
        if probateRole is None:
            await ctx.channel.send("Probate role not found.")
            return
        
        else:
            try:
                await member.edit(roles=[probate_role])
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

        virginrole = member.guild.get_role(918319461688295484)
        if virginRole == None:
            await ctx.channel.send("Virgin role not found.")
            return

        else:
            try:
                await member.edit(roles=[virginrole])
                await ctx.channel.send(f'{member} has been released from the shadow realm.')
            except Exception as e:
                await ctx.channel.send(f'Exception encountered while unprobating: {e}')
                
        
async def setup(bot):
    await bot.add_cog(mods(bot))
