import random

start_image = [
    r"""
    +----------------------+
    |  CONTACT-BOT READY   |
    |     WHAT'S THE PLAN? |
    +----------------------+
    """,
    r"""
    +----------------+
    |    ASSISTANT   |
    |     ONLINE     |
    +----------------+
    """,
    r"""
    +----------------+
    |   LOADING…     |
    |  CONTACT DATA  |
    |     PLEASE     |
    |      WAIT      |
    +----------------+
    """
]

exit_image = [
    r"""
    +----------------------+
    |    BOT IS SLEEPING   |
    |     DO NOT WAKE UP   |
    +----------------------+
    """,
    r"""
    +----------------------+
    |       I'M OUT…       |
    |     CLEAN UP LATER   |
    +----------------------+
    """,
    r"""
    +----------------+
    |  CONTACT BOT   |
    |    SAVED ✓     |
    |    CLOSED      |
    +----------------+
    """,
    r"""
    +----------------+
    |    SESSION     |
    |    FINISHED    |
    |      ✓         |
    +----------------+
    """
]

def random_start_image():
    return random.choice(start_image)

def random_exit_image():
    return random.choice(exit_image)