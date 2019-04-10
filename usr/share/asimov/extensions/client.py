from zeroconf import ServiceBrowser, Zeroconf
from asimov.utils import AsimovConfig
from asimov.event import AsimovEvent
from asimov.extension import Extension
from asimov import event_dispatch
from asimov import boot
import logging

conf = {}
cluster_name = ""

class ZeroConfListener(object):
	def remove_service(self, zeroconf, type, name):
		print("Service %s removed" % (name,))
	def add_service(self, zeroconf, type, name):
		print(f"Added service {type}, {name}")
		info = zeroconf.get_service_info(type, name)
		serviceClusterName = info.properties[b"clusterName"].decode('utf-8')
		print(f"name = {serviceClusterName}, cluster_name = {cluster_name}")
		if cluster_name == serviceClusterName:
			event_dispatch.dispatch_event(AsimovEvent("/asimov/extension/" + info.properties[b'type'].decode('utf-8') + "/attach", [info.properties]))


class ZeroconfClient(Extension):
	listeners = {"/asimov/boot/config": "config", "/asimov/boot/finished": "run"}
	
	def config(self, conf):
		global config
		global cluster_name
		config = conf
		cluster_name = config[b"cluster"][b"name"]

	def lifecycle(self, ev):
		if self.ev == "finished":
			self.run()

	def run(self):
		self.logger.info("Starting Zeroconf client")
		zeroconf = Zeroconf()
		listener = ZeroConfListener()
		browser = ServiceBrowser(zeroconf, "_asimov._tcp.local.", listener)
