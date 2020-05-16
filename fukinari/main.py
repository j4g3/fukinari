import discord
from discord.ext import commands, tasks
import asyncio
import time
import json
import os
from itertools import cycle
import datetime as DT
import platform
import wmi
from api import *

a = Gui()
a.main()
token = a.token
a.bye()
token = token
print(token)


computer = wmi.WMI()
computer_info = computer.Win32_ComputerSystem()[0]
os_info = computer.Win32_OperatingSystem()[0]
proc_info = computer.Win32_Processor()[0]
gpu_info = computer.Win32_VideoController()[0]

os_name = os_info.Name.encode('utf-8').split(b'|')[0]
os_version = ' '.join([os_info.Version, os_info.BuildNumber])
system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
Chnls=[]
platM = platform.machine()
osName = os_name
proc = proc_info.Name
ram = system_ram
gpu = gpu_info.Name
activity = discord.Game
status = cycle(['Feito em python com muito stackoverflow', 'Use --help para obter suporte', 'Ha uma diferenca entre conhecer o caminho e percorrer o caminho.', 'Ferroxy#2071 melhor programador do mundo', 'https://github.com/Ferroxyy/fukinari'])


async def get_prefix(client, message):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
message = discord.Client()
guild = discord.utils.get(client.guilds)

@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(activity=activity(next(status)))


@client.event
async def on_ready():
	change_status.start()
	print(f"\nLogado como {client.user}\n")


@client.event
async def on_guild_join(guild):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	prefixes[str(guild.id)] = '--'

	with open('prefixes.json','w') as file:
		json.dump(prefixes, file, indent=4)

@client.event
async def on_guild_remove(guild):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	prefixes.pop(str(guild.id))
	with open('prefixes.json','w') as file:
		json.dump(prefixes, file, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
	with open('prefixes.json','r') as file:
		prefixes = json.load(file)
	prefixes[str(ctx.guild.id)] = prefix

	with open('prefixes.json','w') as file:
		json.dump(prefixes, file, indent=4)

@client.command()
async def ping(ctx):
	name = "\n\u200b"
	embed = discord.Embed(
	title = 'Connection Test',
	description = name,
	color = discord.Color.red()
	)
	embed.add_field(name=name, value=f':ping_pong: Pong! {round(client.latency * 1000)}ms', inline=True)
	await ctx.send(embed=embed)


@client.command()
async def clear(ctx, amount=0):
	if amount == 0:
		await ctx.send(f"```O limite nao pode ser igual ou menor que 0```")
	await ctx.message.delete()
	await ctx.channel.purge(limit=amount)

@client.command()
async def info(ctx):
	name = "\n\u200b"

	embed = discord.Embed(
	title = ':desktop:  Bot Info',
	description = name,
	color = discord.Color.red()
	)

	embed.set_footer(text='By Ferroxy')
	embed.add_field(name=name, value=f"Arch: ```{platM}```", inline=False)
	embed.add_field(name=name, value=f"OS: ```{osName}```", inline=True)
	embed.add_field(name=name, value=f"Processor: ```{proc}```", inline=True)
	embed.add_field(name=name, value=f"RAM: ```{ram}```", inline=True)
	embed.add_field(name=name, value=f"GPU: ```{gpu}```", inline=True)
	embed.add_field(name=name, value="[GitHub](https://github.com/Ferroxyy/fukinari)", inline=False)
	embed.add_field(name=name, value="[Donation](https://github.com/Ferroxyy/fukinari)", inline=True)
	embed.add_field(name=name, value="[Invite](https://github.com/Ferroxyy/fukinari)", inline=False)
	embed.add_field(name=name, value="[Suport](https://github.com/Ferroxyy/fukinari)", inline=True)
	await ctx.send(embed=embed)
@client.command()
async def load(ctx, extension):
	try:
		embed = discord.Embed(
        	color = discord.Color.red()
    		)
		client.load_extension(f'cogs.{extension}')
		embed.add_field(name="Modulos", value=f":green_circle: Carregando modulo {extension}")
		await ctx.send(embed=embed)
	except Exception as cmdDsErrorLoad:
		embed = discord.Embed(
 		color = discord.Color.from_rgb(144, 12, 63)
    		)
		embed.add_field(name=f"Error {cmdDsErrorLoad}", value=f"Modulo {extension} ja carregado (#-#)")
		await ctx.send(embed=embed)

@client.command()
async def unload(ctx, extension):
	try:
		client.unload_extension(f'cogs.{extension}')
		embed = discord.Embed(
       		color = discord.Color.red()
    		)
		client.unload_extension(f'cogs.{extension}')
		embed.add_field(name="Modulos", value=f":red_circle: Descarregando modulo {extension}")
		await ctx.send(embed=embed)
	except Exception as cmdDsErrorUnload:
		embed = discord.Embed(
 		color = discord.Color.from_rgb(144, 12, 63)
    		)
		embed.add_field(name=f"Error {cmdDsErrorUnload}", value=f"Modulo {extension} ja esta descarregado (#-#)")
		await ctx.send(embed=embed)

@client.command()
async def download_database(ctx):
		embed = discord.Embed(color = discord.Color.red())
		file = discord.File("requirements.txt", filename="requirements.txt")
		await ctx.send(f'```requirements.txt```', file=file)

@client.command()
async def register(ctx):
	embed=discord.Embed(
		color = discord.Color.red()
		)
	embed.add_field(name=f"Register",value="Check your DM to register")
	await ctx.send(embed=embed)
	await ctx.author.send("Register")

@client.command()
async def login(ctx):
	embed=discord.Embed(
		color = discord.Color.red()
		)
	embed.add_field(name=f"Login",value="Check your DM to login")
	await ctx.send(embed=embed)
	await ctx.author.send("Login")




for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)
