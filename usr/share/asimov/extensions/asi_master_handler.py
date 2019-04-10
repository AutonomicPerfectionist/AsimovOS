import subprocess
from asimov import event_dispatch
from asimov.extension import Extension
import logging

class AsiMaster(Extension):
  listeners = {
    "/asimov/extension/master/boot": "boot",
    "/asimov/extension/master/attach": "attach",
    "/asimov/boot/config": "config"
  }
  conf = dict()
  def __init__(self):
	  #event_dispatch.add_event_listener("MASTER-BOOT", self.boot)
	  event_dispatch.add_event_listener("MASTER-ATTACH", self.attach)


  def boot(self, data):
	  self.logger.info("Booting roscore...")
	  subprocess.call("roscore &", shell=True)

  def attach(self, data):
	  self.logger.info("Attaching RosCore...")

  def config(self, conf):
    self.conf = conf
