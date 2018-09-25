import rpyc
import logging
import threading
from rpyc.utils.server import ThreadedServer
from rpyc.utils.registry import TCPRegistryClient, REGISTRY_PORT
from asimov import event_dispatch
from asimov.utils import AsimovConfig
from asimov.extension import Extension

class NodeServiceExt(Extension):
  def __init__(self):
	  event_dispatch.add_event_listener("NODE-BOOT", self.boot)
	  event_dispatch.add_event_listener("NODE-ATTACH", self.attach)
  def boot(self, ev):
	  NodeService.setConfig(ev)
	  thread = threading.Thread(target=ThreadedServer(NodeService, port=int(ev.port), registrar=TCPRegistryClient(ip="0.0.0.0", port=REGISTRY_PORT)).start)
	  thread.daemon = True
	  thread.start()
	  self.logger.info("Node Service started")

def attach(self, ev):
	self.logger.debug(str(ev.data))


class NodeService(rpyc.Service):
	config = None

	def __init__(self, conn):
		rpyc.Service.__init__(self, conn)
		#TODO: Add to registry

	@classmethod
	def setConfig(cls, config):
		cls.config = config
		cls.ALIASES = config.data["aliases"]
		
	
	def on_connect(self):
		# code that runs when a connection is created
		# (to init the serivce, if needed)
		self.log = logging.getLogger(__name__)
		self.log.debug("Connection established")

	def on_disconnect(self):
		# code that runs when the connection has already closed
		# (to finalize the service, if needed)
		pass

	def exposed_get_answer(self): # this is an exposed method
		return 42

	def get_question(self):  # while this method is not exposed
		return "what is the airspeed velocity of an unladen swallow?"


