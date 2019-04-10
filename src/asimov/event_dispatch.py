import logging
import asimov.event
import msgpack

single_process_mode = True
try:
	import emb
except ImportError:
	single_process_mode = False #Not running in single-process mode

#from julia import Julia
#jl = Julia(runtime="/Users/branden/git/julia/julia")

#from julia import EventDispatch

from threading import RLock
from threading import get_ident
from queue import Queue
"""
Generic event dispatcher which listen and dispatch events
"""

import sys
import faulthandler
faulthandler.enable()
def trace(frame, event, arg):
    print("%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno))
    return trace

#sys.settrace(trace)

q = Queue()

logger = logging.getLogger(__name__)
_events = dict()
jl_dispatch = None
jl_dispatch_event = None
jl_dispatch_add = None
jl_dispatch_module = None
jl_event = None
lock = RLock()

def set_jl_dispatch(d, jl_module,jl_d_event, jl_add, ev) :
	global jl_dispatch
	global jl_dispatch_module
	global jl_dispatch_event
	global jl_dispatch_add
	global jl_event
	jl_dispatch = d
	jl_dispatch_module = jl_module
	jl_dispatch_event = jl_d_event
	jl_dispatch_add = jl_add
	jl_event = ev
	asimov.event.set_event_type(ev)

def has_listener(event_type, listener):
	"""
	Return true if listener is register to event_type
	"""
	# Check for event type and for the listener
	if event_type in _events.keys():
		return listener in _events[ event_type ]
	else:
		return False

def dispatch_event(ev):
	if jl_dispatch_event:
		#jl_dispatch_event(jl_dispatch, ev)
		#EventDispatch.dispatch_event(EventDispatch.dispatch, ev)
		#lock.acquire()
		#logger.debug("Acessing queue")
		#q.put(ev)
		#lock.release()
		#logger.debug("Released lock")
		pass
	if single_process_mode:
		emb.dispatch(ev.type, msgpack.packb(ev.data))
	else:
		dispatch_event_python(ev)
def dispatch_event_python(event):
	"""
	Dispatch an instance of AsimovEvent class
	"""
	# Dispatch the event to all the associated listeners
	logger.debug("Searching for listeners on topic %s" % event.type)
	logger.debug("Event data: %s" % str(event.data))
	if event.type in _events.keys():
	  listeners = _events[ event.type ]
	  for listener in listeners:
	    if event.data is not None and len(event.data) > 0:
	      listener( *event.data )
	    else:
	      listener()

def add_event_listener(event_type, listener):
	"""
	Add an event listener for an event type
	"""
	# Add listener to the event type
	if jl_dispatch_add:
		jl_dispatch_add(jl_dispatch, event_type, listener)
	else:
		if not has_listener( event_type, listener ):
			logger.debug("Adding event listener to topic %s" %  (event_type))
			listeners = _events.get( event_type, [] )
	
			listeners.append( listener )
	  
			_events[ event_type ] = listeners

def remove_event_listener(event_type, listener):
	"""
	Remove event listener.
	"""
	# Remove the listener from the event type
	if has_listener( event_type, listener ):
		listeners = _events[ event_type ]

		if len( listeners ) == 1:
			# Only this listener remains so remove the key
			del _events[ event_type ]

		else:
			# Update listeners chain
			listeners.remove( listener )

			_events[ event_type ] = listeners
