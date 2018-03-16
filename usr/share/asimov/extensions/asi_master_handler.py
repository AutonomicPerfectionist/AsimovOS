import subprocess
from asimov import event_dispatch
import logging

log = logging.getLogger(__name__)
def init():
	event_dispatch.add_event_listener("MASTER-BOOT", boot)
	event_dispatch.add_event_listener("MASTER-ATTACH", attach)


def boot(data):
	log.info("Booting roscore...")
	subprocess.call("roscore &", shell=True)

def attach(data):
	log.info("Attaching RosCore...")


init()
