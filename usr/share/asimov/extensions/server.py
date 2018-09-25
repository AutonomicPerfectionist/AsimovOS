from asimov.zeroconf import *
import asimov.zeroconf
import logging
import socket
import os
import signal
from asimov.utils import AsimovConfig
from asimov.event import AsimovEvent
global event_dispatch
from asimov import event_dispatch
from asimov import boot
from asimov.extension import Extension
import netifaces as ni
import traceback




class Server (Extension):
	listeners = {"/asimov/boot/config": "config", "/asimov/extension/server/kill": "kill_server", "/asimov/boot/lifecycle": "lifecycle"}
	conf = {}
	clusterName = ""
	log = logging.getLogger(__name__)
	types = []
	interfaces = []
	r = None
	infoCache = []
	def config(self, conf):
		self.conf = conf
		self.clusterName = conf["cluster"]
		self.types = self.conf["cluster"]["types"].keys()
		self.interfaces = self.conf["system"]["interfaces"]
		#self.logLevel = logging.INFO
		#if self.conf["system"]["debug"]:
		#	logLevel = logging.DEBUG
		#logging.basicConfig(level=logLevel)
		#self.log = logging.getLogger(__name__)


	def lifecycle(self, ev):
		self.log.debug("Lifecycle event received: %s" % (ev))
		if ev is "start":
			self.run()
	def run(self):
		#Do this so that all processes started by the boot procedure are killed on exit
		try:
			os.setpgrp()
		except OSError as e:
			log.error("OSError on os.setpgrp(): %s" % (str(e)))
		#boot.init()
		event_dispatch.add_event_listener("SERVER-KILL", self.kill_server)
  
		self.log.info("Registering ZeroConf services...")
  
		ipArray = []
		for interface in self.interfaces:
			try:
				ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
				ipArray.append(ip)
				self.log.info("IP %s on interface %s" % (ip, interface))
    
			except Exception as v:
				self.log.error("Interface %s in asimov.conf not present on system. Skipping interface..." % (interface))
				continue
		self.r = Zeroconf(interfaces=ipArray)
		#socket.inet_aton(ipArray[0])
  
		try:
			for type in self.types:
				typeParams = self.conf["cluster"]["types"][type]
				desc = {'host': self.conf['system']['hostname'], 'clusterName': self.clusterName, 'type': type}
				info = ServiceInfo("_asimov._tcp.local.","AsimovOS Type " + type + " on " + self.conf['system']['hostname'] + "._asimov._tcp.local.", socket.inet_aton(ipArray[0]), int(typeParams["port"]), 0, 0, desc)
				self.infoCache.append(info)
				self.r.register_service(info)
				event_dispatch.dispatch_event(AsimovEvent("/asimov/%s/%s" % (type.lower(), "boot"), self.conf["system"]["hostname"], typeParams["port"], "SERVER", data=typeParams))
    			boot.passBoot("SERVER")
			event_dispatch.dispatch_event(AsimovEvent("/asimov/boot/finished", None, None, "SERVER"))
    
		#raw_input("Waiting (press Enter to exit)...\n") 
		except Exception:
			self.log.error("Unable to boot system... Exception caught in boot sequence")
			traceback.print_exc()
			self.kill_server(None)
	  
	def kill_server(self, ev):
		self.log.info("Server shutting down...")
		for info in self.infoCache:
			self.r.unregister_service(info)
			self.r.close()
		os.killpg(0, signal.SIGTERM)
