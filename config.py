# Bot's token
import os

from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

# The default prefix for commands
default_prefix = "t!"

# Status of the bot
activity = f"{default_prefix}help"

# The main bot owner
owner = 298661966086668290

# Bot owners that have access to owner commands
owners = [
    298661966086668290,
    412969691276115968,
    446290930723717120,
    488283878189039626,
    685456111259615252,
    723794074498367498,
]

# Bot admins that have access to admin commands
admins = []

# Cogs to load on startup
initial_extensions = [
    "cogs.admin",
    "cogs.core",
    "cogs.error_handler",
    "cogs.events",
    "cogs.general",
    "cogs.miscellaneous",
    "cogs.owner",
]

# Channels to send logs
join_channel = 744376264718155814
event_channel = 744376264718155815
admin_channel = 744376264860893244

# This is where patron roles are at
main_server = 744376264118239262

# Patron roles for premium servers
premium1 = 000000000000000000
premium3 = 000000000000000000
premium5 = 000000000000000000

# The colour used in embeds
primary_colour = 0x00FF7F
error_colour = 0xFF0000
