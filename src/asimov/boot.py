import os
import logging
from asimov import event_dispatch

extensionsDir = "usr/share/asimov/extensions/"
log = logging.getLogger(__name__)
def init():
	#Replace with extensions system
	#asimov_event_dispatch.add_event_listener("STORAGE-BOOT", handleStorageBoot)
	#asimov_event_dispatch.add_event_listener("MASTER-BOOT", handleMasterBoot)
	for file in os.listdir(extensionsDir):
		log.debug("Executing extension with filename %s" % (file))
		execfile(extensionsDir + file, {"__name__": file.split(".")[0]})
def passBoot(type):
	log.info("Taking over boot sequence from %s..." % (type))


init()
