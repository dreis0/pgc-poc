from random import randint
from flask import Blueprint

from api import app
from observability.metrics import roll_counter
from observability.tracing import tracer

endpoint = Blueprint('rolldice', __name__, url_prefix='/rolldice')


@endpoint.route('/')
def roll_dice():
    with tracer.start_as_current_span("do_roll") as rollspan:
        res = randint(1, 6)

        rollspan.set_attribute("roll.value", res)
        roll_counter.add(1, {"roll.value": res})
        app.logger.info("Rolled a %s", res)

    return str(res)
