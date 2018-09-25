#!/bin/env python

import os
import logging
from asimov import event_dispatch
from asimov import extension
from asimov.enabler import Enabler
from asimov import topics

from configobj import ConfigObj


"""
This is the entrypoint for AsimovOS.
Boot is responsible for... well, booting the system...
First it loads the extensions, then runs the Enabler scripts,
builds the master configuration and transmits it,
before transmitting the /asimov/boot/lifecycle start event
to start the extension initialization sequence.
Once all extensions have processed this event the 
/asimov/boot/lifecycle finished event is transmitted.
All other events are transmitted by their respective extensions.
"""
extensionsDir = "usr/share/asimov/extensions/"
extensionsLibDir = "usr/share/asimov/extension-lib/"

mainConfigLoc = "etc/asimov-local/asimov.conf"
configDir = "etc/asimov-local/asimov.conf.d"

log = logging.getLogger(__name__)
log.debug("Files in CWD:\n%s" % (str(os.listdir("."))))
messages = topics.topicManager.namespaces

conf = dict()

def init():
  global conf
  conf = build_configuration(mainConfigLoc, configDir)
  logLevel = logging.INFO
  if conf["system"]["debug"]:
    logLevel = logging.DEBUG
  logging.basicConfig(level=logLevel)

  #Since boot is not an extension, this must be called manually
  topics.topicManager.registerTopic("/asimov/boot/lifecycle")
  topics.topicManager.registerTopic("/asimov/boot/config")
  try:
    os.setpgrp()
  except OSError as e:
    log.error("OSError on os.setpgrp(): %s" % (str(e)))


  #TODO Pass config dict so that enabler scripts have access to it  
  load_extensions(extensionsDir)
  messages.asimov.boot.config(conf)
  messages.asimov.boot.lifecycle("start")
	
	
def load_extensions(folder):
  """
  Load extensions in folder and run Enabler scripts
  """
  extension.load_extensions(extensionsDir)
  extension.enabler = Enabler(extension.registered_extensions, {}, {"extensions.client": True, "extensions.asi_master_handler": False, "extensions.asi_storage_handler": True, "extensions.node_registry": False, "extensions.node_service": False, "extensions.cli": False, "__builtin__": True, "extensions.webui": False, "extensions.server": True})
	
def build_configuration(main, folder):
  """
  Build the master configuration dictionary. Main is the file
  location of the primary configuration, and folder is the directory
  where secondary files are located
  """
  if not folder.endswith('/'):
			folder += '/'
  #TODO Load and combine secondary configs
  return ConfigObj(main)

def passBoot(type):
	log.info("Taking over boot sequence from %s..." % (type))

