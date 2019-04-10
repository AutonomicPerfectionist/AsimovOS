import logging
import threading
from asimov import event_dispatch
from asimov.extension import Extension
from rpyc.utils.registry import TCPRegistryServer
from rpyc.utils.registry import REGISTRY_PORT

class NodeRegistry(Extension):
  listeners = {"/asimov/extension/master/boot": "boot", "/asimov/extension/master/attach": "attach"}
  def __init__(self):
	  event_dispatch.add_event_listener("MASTER-BOOT", self.boot)
	  event_dispatch.add_event_listener("MASTER-ATTACH", self.attach)

  def boot(self, ev):
    self.logger.debug("Starting server")
    server = TCPRegistryServer(host="0.0.0.0", port=REGISTRY_PORT, logger=self.logger)
    thread = threading.Thread(target=server.start)
    thread.daemon = True
    thread.start()
  def attach(self, ev):
  	pass
  
