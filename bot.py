import discord
import json
import os
from discord.ext import commands


#get prefix 

def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	return prefixes[str(message.guild.id)]	



client = commands.Bot( command_prefix = '?' )

client.remove_command( 'help' )

@client.event 

async def on_ready():
	print('Bot connected')

	await client.change_presence( status = discord.Status.online, activity = discord.Game(' ?help ')  ) 

#prefix command

@client.event

async def on_guild_join(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = '?'

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 4)

@client.event

async def on_guild_remove(guild):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 4)

@client.command()

async def setprefix(ctx, prefix):
	with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

	prefixes[str(ctx.guild.id)] = prefix

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent = 4)

#error event (arguments)

@client.event
async def on_command_error(ctx,error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Ошибка.Пожалуйста введите все нужные аргументы.')


#clear message	

@client.command ( pass_context = True )	
@commands.has_permissions( administrator = True )

async def clear(ctx, amount : int):
	await ctx.channel.purge(limit = amount)

#kick

@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def kick( ctx, member: discord.Member, *, reason = None ):
	await member.kick( reason = reason ) 
	await ctx.send( f,'{member.mention} was kicked')

#ban	

@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def ban( ctx, member: discord.Member, *, reason = None ):
	await member.ban( reason = reason ) 
	await ctx.send( f,'{member.mention} was banned')

#unban

@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def unban( ctx, *, member ):
	banned_users = await ctx.guild.bans() 

	for ban_entry in banned_users:
		user = ban_entry.user 

		await ctx.guild.unban ( user ) 
		await ctx.send ( f,'{user.mention} was unbanned' )

		return
#avatar command

@client.command()

async def avatar(ctx, member : discord.Member):

	show_avatar = discord.Embed(

		color = discord.Color.dark_blue()
		)

	emb = discord.Embed( title = 'Аватар пользователя {user_mention}' )
	show_avatar.set_image(url = '{}'.format(member.avatar_url)) 
	await ctx.send(embed = show_avatar)
#help command

@client.command ( pass_context = True )		

async def help( ctx ):
	emb = discord.Embed( title = 'Навигация по коммандам' )

	emb.add_field( name = 'clear'.format(client), value = 'Очистка чата'  )
	emb.add_field( name = 'kick'.format(client), value = 'Выгнать человека с сервера'  )
	emb.add_field( name = 'ban'.format(client), value = 'Ограничение доступа к серверу'  )
	emb.add_field( name = 'unban'.format(client), value = 'Убрать ограничение'  )
	emb.add_field( name = 'invite'.format(client), value = 'Пригласить бота на свой сервер')
	emb.add_field( name = 'mute'.format(client), value = 'Дать ограничение в написание чат')
	emb.add_field( name = 'unmute'.format(client), value = 'Снять ограничение написания в чат')
	emb.add_field( name = 'setprefix'.format(client), value = 'Поставить другой префикс(в разработке)')
	emb.add_field( name = 'avatar'.format(client), value = 'Увидеть аватар человека')
	await ctx.send ( embed = emb )

#invite command

@client.command ( pass_context = True )

async def invite ( ctx ):
	await ctx.author.send ( 'Нажми на ссылку чтоб пригласить бота: https://discord.com/api/oauth2/authorize?client_id=744594189190430841&permissions=335767574&scope=bot')

#Mute 

@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def mute ( ctx, member: discord.Member ):

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Muted' )

	await member.add_roles( mute_role )
	await ctx.send ( f' {member.mention} was muted' )

#Unmute

@client.command ( pass_context = True )
@commands.has_permissions( administrator = True )

async def unmute ( ctx, member: discord.Member ):

	mute_role = discord.utils.get( ctx.message.guild.roles, name = 'Muted' )

	await member.remove_roles( mute_role )
	await ctx.send ( f' {member.mention} was unmuted' )


#Connect


token = os.environ.get('TOKEN')
client.run(token)
