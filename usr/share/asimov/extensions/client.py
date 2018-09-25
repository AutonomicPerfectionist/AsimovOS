from zeroconf import ServiceBrowser, Zeroconf
from asimov.utils import AsimovConfig
from asimov.event import AsimovEvent
from asimov.extension import Extension
from asimov import event_dispatch
from asimov import boot
import logging

conf = AsimovConfig("etc/asimov-local/")
confDict = conf.getConf()
logLevel = logging.INFO
if confDict["system"]["debug"]:
	logLevel = logging.DEBUG
logging.basicConfig(level=logLevel)
clusterName = conf.getClusterName()

class ZeroConfListener(object):
	def remove_service(self, zeroconf, type, name):
		print("Service %s removed" % (name,))
	def add_service(self, zeroconf, type, name):
		info = zeroconf.get_service_info(type, name)
		serviceClusterName = info.properties["clusterName"]
		if clusterName == serviceClusterName:
			event_dispatch.dispatch_event(AsimovEvent(info.properties['type'] + "-ATTACH", info.properties["host"], info.port, "CLIENT", data=info.properties))


class ZeroconfClient(Extension):
	listeners = {"/asimov/boot/finished": "run"}

	def lifecycle(self, ev):
		if self.ev == "finished":
			self.run()

	def run(self, ev):
		zeroconf = Zeroconf()
		listener = ZeroConfListener()
		browser = ServiceBrowser(zeroconf, "_asimov._tcp.local.", listener)
