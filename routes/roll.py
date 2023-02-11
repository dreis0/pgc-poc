from random import randint
from flask import Blueprint, Flask

from observability.metrics import roll_counter
from observability.tracing import tracer


class RollDiceEndpoint:
    blueprint = None
    app = None

    def __init__(self, app: Flask):
        self.app = app
        self.blueprint = Blueprint('rolldice', __name__, url_prefix='/rolldice')
        self.blueprint.route('/', methods=['GET'])(self.roll_dice)

    def roll_dice(self):
        with tracer.start_as_current_span("do_roll") as rollspan:
            res = randint(1, 6)

            rollspan.set_attribute("roll.value", res)
            roll_counter.add(1, {"roll.value": res})
            self.app.logger.info("Rolled a %s", res)

        return str(res)
