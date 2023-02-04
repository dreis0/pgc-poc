from random import randint
from flask import Blueprint

from api import app
from observability.metrics import roll_counter

endpoint = Blueprint('rolldice', __name__, url_prefix='/rolldice')


@endpoint.route('/')
def roll_dice():
    res = randint(1, 6)
    roll_counter.add(1, {"roll.value": res})
    app.logger.info("Rolled a %s", res)

    return str(res)
