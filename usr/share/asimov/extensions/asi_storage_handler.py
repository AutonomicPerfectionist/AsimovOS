import subprocess
import logging
from asimov import event_dispatch

log = logging.getLogger(__name__)
def init():
	event_dispatch.add_event_listener("STORAGE-BOOT", boot)
	event_dispatch.add_event_listener("STORAGE-ATTACH", attach)

def boot(ev):
	log.info("Exporting filesystem")
	subprocess.call("exportfs -ra", shell=True)

def attach(ev):
	log.info("Attaching filesystem mount")
	log.debug("Server: %s" % (ev.url))
	subprocess.call("gksudo -- mount -t nfs -o proto=tcp,port=" + str(ev.port) + " " + ev.data['host']+ ":/ /home/branden/nfs", shell=True)
init()
