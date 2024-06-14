import discord
from discord.ext import commands
import sqlite3

con = sqlite3.connect('bot.db')
cur = con.cursor()


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        cur.execute(f"SELECT role_id FROM roles WHERE guild_id = {member.guild.id}")
        res = cur.fetchone()
        role = discord.utils.get(member.guild.roles, id=res[0])
        channel = discord.utils.get(member.guild.channels, id=1232025281905033289)
        await member.add_roles(role)
        await channel.send(f'Добро пожаловать на сервер, {member.name}!')

    @commands.Cog.listener()
    async def on_ready(self):
        print('BOT connected')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Привет, {ctx.author.name}')

    # clear message
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)

    # kick
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        await ctx.send(f'kick user {member.mention}')

    # issuing roles
    @commands.command(aliases=['set_role'])
    @commands.has_permissions(administrator=True)
    async def set_new_users_role(self, ctx, role_id):
        cur.execute("""CREATE TABLE IF NOT EXISTS roles(
                    guild_id int,
                    role_id int)
                    """)
        con.commit()

        if cur.execute(f"SELECT role_id FROM roles WHERE guild_id = {ctx.guild.id}").fetchone() is None:
            cur.execute(f"INSERT INTO roles VALUES ({ctx.guild.id}, {int(role_id)})")
            await ctx.send('роль задана')
        else:
            cur.execute(f'UPDATE roles SET role_id = {role_id} WHERE guild_id = {ctx.guild.id}')
            await ctx.send('новая роль задана')

    # ban
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.ban(reason=reason)
        await ctx.send(f'ban user {member.mention}')

    # unban
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        await ctx.channel.purge(limit=1)
        await member.unban()
        await ctx.send(f'Unbanned user {member.mention}')

    # mute
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
        await member.add_roles(mute_role)
        await ctx.send(f'У {member.mention}, ограничение чата, за нарушения!')

    # unmute
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        await ctx.channel.purge(limit=1)
        mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
        await member.remove_roles(mute_role)
        await ctx.send(f'У {member.mention} снято ограничение чата!')


async def setup(client):
    await client.add_cog(Commands(client))
