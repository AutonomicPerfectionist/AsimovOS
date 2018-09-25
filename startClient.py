from asimov.zeroconf import ServiceBrowser, Zeroconf
from asimov.utils import AsimovConfig
from asimov.event import AsimovEvent
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
logger = logging.getLogger(__name__)
class ZeroConfListener(object):
     def remove_service(self, zeroconf, type, name):
          print("Service %s removed" % (name,))
     def add_service(self, zeroconf, type, name):
          info = zeroconf.get_service_info(type, name)
          serviceClusterName = info.properties["clusterName"]
          if clusterName == serviceClusterName:
                 #print("Cluster service %s added for cluster %s, type: %s" % (name, info.properties['clusterName'], str(info.properties['type'])))
                 event_dispatch.dispatch_event(AsimovEvent(info.properties['type'] + "-ATTACH", info.properties["host"], info.port, "CLIENT", data=info.properties))

if __name__ == "__main__":
  boot.init()
  zeroconf = Zeroconf()
  listener = ZeroConfListener()
  browser = ServiceBrowser(zeroconf, "_asimov._tcp.local.", listener)
  boot.passBoot("CLIENT")
  