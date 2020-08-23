from dotenv import load_dotenv
load_dotenv()
import os
token = os.environ['TOKEN']
import psutil
import subprocess

import logging 
import datetime
import textwrap
import discord
import random
import io
from contextlib import redirect_stdout
import sys
import traceback
import asyncio
import importlib
from discord.ext import commands

#Whitelisted users
invite_link = "https://discord.com/oauth2/authorize?client_id=744372909363167314&scope=bot&permissions=257152"
whitelist = [298661966086668290, 412969691276115968, 446290930723717120,685456111259615252,488283878189039626]
bot = commands.Bot(command_prefix = commands.when_mentioned_or('t!'))
@bot.command(name = "exe", brief = "Execute Python code", usage = "<code>", description = "Executes Python code, like a Python interpreter. Some modules and functions are banned, find them on the github! (https://github.com/kym2006/random.bot)")
async def exe(ctx, *, body: str):    
    if ctx.author.id not in whitelist and ctx.author.id != 298661966086668290:
        try: 
            await ctx.send("You have no permission HAHAHAHAHHA HAHAHAHAHAHHAH")
            return 
        except:
            return
    
    env = {
        "bot": bot,
        "ctx": ctx,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
        "whitelist": whitelist
    }  
    stdout = io.StringIO()  
    #env.update(globals())
    #new env: only send (ctx.send)
    '''
    env = {
        "ctx": ctx,
    }
    '''
    exec("", env)
    to_compile = f'async def func():\n  try:\n{textwrap.indent(body, "    ")}\n  except:\n    raise'
    try:
        exec(to_compile, env)
    except:
        await ctx.send(
            embed=discord.Embed(
                description=f"```py\n{traceback.format_exc()}\n```", colour=discord.Color.red(),
            )
        )
        return
    func = env["func"]
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except (AttributeError, Exception, BaseException):
        await ctx.send(
            embed=discord.Embed(
                description=f"```py\n{stdout.getvalue()}{traceback.format_exc()}\n```",colour=discord.Color.red(),
            )
        )
    else:
        value = ret
        try:
            await ctx.message.add_reaction("✅")
        except discord.Forbidden:
            pass

        if stdout.getvalue():
            try:
              if value != None:
                  await ctx.send(
                      embed=discord.Embed(
                          description=f"```py\n{stdout.getvalue()}{value}\n```", colour=discord.Color.green()
                      )
                  )
              else:
                  await ctx.send(
                      embed=discord.Embed(
                          description=f"```py\n{stdout.getvalue()}\n```", colour=discord.Color.green()
                      )
                  )
            except:
              await ctx.send(
                embed=discord.Embed(    
                    description=f"```py\n{traceback.format_exc()[-5000:]}\n```", colour=discord.Color.red()
                )
              )
        else:
            try: 
                #will not send if no return value
                if value != None:
                    await ctx.send(
                        embed=discord.Embed(
                            description=f"```py\n{value}\n```", colour=discord.Color.green()
                        )
                    )
            except:
              await ctx.send(
                embed=discord.Embed(    
                    description=f"```py\n{traceback.format_exc()[-5000:]}\n```", colour=discord.Color.red()
                )
              )   


@bot.command(description="Execute code in bash.", usage="bash <command>", hidden=True)
async def bash(ctx, *, command_to_run: str):
    if ctx.author.id not in whitelist:
        await ctx.send("You have no permission HAHAHAHAHHA HAHAHAHAHAHHAH")
        return 
    try:
        output = subprocess.check_output(command_to_run.split(), stderr=subprocess.STDOUT).decode("utf-8")
        await ctx.send(embed=discord.Embed(description=f"```py\n{output}\n```", colour=discord.Colour.green()))
    except Exception as error:
        await ctx.send(
            embed=discord.Embed(
                description=f"```py\n{error.__class__.__name__}: {error}\n```", colour=discord.Colour.red(),
            )
        )


@bot.command(name = "invite", brief = "Sends invite link", description = "Sends the invite link to this bot!", usage = "")
async def invite(ctx):
    await ctx.send(
            embed=discord.Embed(
                description=f"Invite this bot: {invite_link}", colour=discord.Color.green()
        )
    )
    await ctx.send(
            embed=discord.Embed(
                description=f"Join our support server: https://discord.gg/6yEzEBy", colour=discord.Color.green()
        )
    )


@bot.command(name="export", brief="export channel history")
async def export(ctx):
    f=open(f"c{ctx.channel.id}.txt", "a+")
    await ctx.send(file=discord.File(f"c{ctx.channel.id}.txt"))

@bot.event
async def on_message(message):
    f=open(f"c{message.channel.id}.txt", "a+")
    f.write(f"{message.author.name}#{message.author.discriminator}: {message.content}\n")
    await bot.process_commands(message)

bot.run(token)