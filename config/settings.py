import os

# ----------------
# GENERAL SETTINGS
# ----------------

# Bot Prefix
prefix = os.getenv('PREFIX', '!')

# -------------
# COG SETTINGS
# -------------

# Core Cog
core_config = {
    'custom_status': os.getenv('CUSTOM_STATUS', 'Doing Stuff')
}

# ---------------
# COG TOGGLES
# ---------------
features = {
    'ping': os.getenv('PING', 'True').lower() in 'true',
    'course_checking': os.getenv('COURSE_CHECKING', 'True').lower() in 'true',
}
