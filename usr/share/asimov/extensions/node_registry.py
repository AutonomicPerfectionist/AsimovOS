import logging
import threading
from asimov import event_dispatch
from rpyc.utils.registry import TCPRegistryServer
from rpyc.utils.registry import REGISTRY_PORT

log = logging.getLogger(__name__)

def init():
	event_dispatch.add_event_listener("MASTER-BOOT", boot)
	event_dispatch.add_event_listener("MASTER-ATTACH", attach)

def boot(ev):
	server = TCPRegistryServer(host="0.0.0.0", port=REGISTRY_PORT, logger=log)
	thread = threading.Thread(target=server.start)
	thread.daemon = True
	thread.start()
def attach(ev):
	pass

init()
