#from julia import EventDispatch

import threading
from queue import Queue

creation_q = Queue()
created_dict = {}

def update_created_dict(key, value):
	created_dict[key] = value

class AsiEventCreationWaiter(threading.Event):
	args = []
	id = 0

	def __init__(self, args, thread_id):
		threading.Event.__init__(self)
		self.args = args
		self.id = thread_id	

class AsimovEvent( object ):
	"""
	Event object to use with MEventDispatch.
	"""

	def __init__(self, event_type, data=None):
		"""
		The constructor accepts an event type as string and a custom data
		"""
		self._type = event_type
		self._data = data

	@property
	def type(self):
		"""
		Returns the event type
		"""
		return self._type

	@property
	def data(self):
		"""
		Returns the data associated to the event
		"""
		return self._data

	def __str__(self):
		return "AsimovOS event of type %s at url %s, %s side" % (self._type, self.data, self.nodeType)

#AsimovEvent = None

def set_event_type(a):
	print("Setting event type: " + str(a))
	global AsimovEvent
	AsimovEvent = get_asi_event_threaded

def get_asi_event_threaded(*args):
	if threading.current_thread() == threading.main_thread():
		return EventDispatch.AsiEvent(*args)
	else:
		#Request main thread to generate AsiEvent and block until notified
		waiter = AsiEventCreationWaiter(args, threading.get_ident())
		creation_q.put(waiter)
		waiter.wait() #AsiEvent created in main thread, via Julia
		ev = created_dict[threading.get_ident()]
		del created_dict[threading.get_ident()]
		return ev
