#import sys
#sys.path.append(".")
from asimov import boot
#boot.init()
boot.load_extensions(boot.extensionsDir)
import emb
from asimov.event_dispatch import dispatch_event_python
from asimov.event import AsimovEvent
from msgpack import unpackb
from msgpack import packb

def dispatch_ev_py(topic, args):
	a = unpackb(args)
	dispatch_event_python(AsimovEvent(topic, a))
	return 6
def t():
	emb.dispatch("/asimov/test", packb([3, 5, 7]))
	return 0
