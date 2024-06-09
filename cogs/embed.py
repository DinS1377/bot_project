import discord
from discord.ext import commands
PREFIX = '$'


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.remove_command(help)

    @commands.command()
    async def help(self, ctx):
        emb = discord.Embed(title="навигация по командам", colour=discord.Colour.green())
        emb.set_author(name='SVOBOT')
        emb.add_field(name='{}clear ( {{количество сообщений}} )'.format(PREFIX),
                      value="очищает последние сообщения из чата. По умолчанию удаляются 100 сообщений")
        emb.add_field(name='{}kick ( {{id_пользователя}}, [причина] ).'.format(PREFIX),
                      value='выгоняет пользователя с сервера, вторым аргументом можно указать причину кика')
        emb.add_field(name='{}set_new_users_role( {{id роли}} )'.format(PREFIX),
                      value='задаёт роль которая будет автоматически выдаваться новым участникам на сервере')
        emb.add_field(name='{}ban ( {{id пользователя}}, [причина] )'.format(PREFIX),
                      value='банит пользователя')

        await ctx.send(embed=emb)


async def setup(client):
    await client.add_cog(Embed(client))
