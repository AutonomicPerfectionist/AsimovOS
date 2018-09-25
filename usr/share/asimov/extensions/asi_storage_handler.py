import subprocess
import logging
from asimov import event_dispatch
from asimov.extension import Extension

class AsiStorage(Extension):
  listeners = {"/asimov/storage/boot": "boot", "/asimov/storage/attach": "attach"}
  def __init__(self):
	  event_dispatch.add_event_listener("STORAGE-BOOT", self.boot)
	  event_dispatch.add_event_listener("STORAGE-ATTACH", self.attach)

  def boot(self, ev):
	  self.logger.info("Exporting filesystem")
	  subprocess.call("exportfs -ra", shell=True)

  def attach(self, ev):
	  self.logger.info("Attaching filesystem mount")
	  self.logger.debug("Server: %s" % (ev.url))
	  subprocess.call("gksudo -- mount -t nfs -o proto=tcp,port=" + str(ev.port) + " " + ev.data['host']+ ":/ /home/branden/nfs", shell=True)
  
  
