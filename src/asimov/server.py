from zeroconf import *
import zeroconf
import logging
import socket
import os
import signal
from asimov.utils import AsimovConfig
from asimov.event import AsimovEvent
global event_dispatch
from asimov import event_dispatch
from asimov import boot
import netifaces as ni
import traceback

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
conf = AsimovConfig("etc/asimov-local/")
confDict = conf.getConf()
clusterName = conf.getClusterName()
types = conf.getNodeTypes()

interfaces = conf.getInterfaces()
logLevel = logging.DEBUG
if confDict["system"]["debug"] == True:
	logLevel = logging.DEBUG
logging.basicConfig(level=logLevel)
log = logging.getLogger(__name__)

#Do this so that all processes started by the boot procedure are killed on exit
os.setpgrp()

r = None
log.info("Registering ZeroConf services...")

ipArray = []
for interface in interfaces:
	try:
		ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
		ipArray.append(ip)
		log.info("IP %s on interface %s" % (ip, interface))

	except ValueError as v:
		log.error("Interface %s in asimov.conf not present on system. Skipping interface..." % (interface))
		continue
r = Zeroconf(interfaces=ipArray)
#socket.inet_aton(ipArray[0])
infoCache = []
try:
	for type in types:
		desc = {'host': conf.getHostname(), 'clusterName': clusterName, 'type': type}
		info = ServiceInfo("_asimov._tcp.local.","AsimovOS Type " + type + " on " + conf.getHostname() + "._asimov._tcp.local.", socket.inet_aton(ipArray[0]), int(conf.getNodeTypeParams(type)["port"]), 0, 0, desc)
		infoCache.append(info)
		r.register_service(info)
		event_dispatch.dispatch_event(AsimovEvent(type + "-BOOT", conf.getHostname(), conf.getNodeTypeParams(type)["port"], "SERVER", data=conf.getNodeTypeParams(type)))

	boot.passBoot("SERVER")
	raw_input("Waiting (press Enter to exit)...\n") 
except Exception:
	log.error("Unable to boot system... Exception caught in boot sequence")
	traceback.print_exc()

finally:
	log.info("Unregistering...")
	for info in infoCache:
		r.unregister_service(info)
	r.close()
	os.killpg(0, signal.SIGTERM)
