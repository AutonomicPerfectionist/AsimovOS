"""
Generic event dispatcher which listen and dispatch events
"""

_events = dict()

def has_listener(event_type, listener):
	"""
	Return true if listener is register to event_type
	"""
	# Check for event type and for the listener
	if event_type in _events.keys():
		return listener in _events[ event_type ]
	else:
		return False

def dispatch_event(event):
	"""
	Dispatch an instance of AsimovEvent class
	"""
	# Dispatch the event to all the associated listeners
	if event.type in _events.keys():
		listeners = _events[ event.type ]
		for listener in listeners:
			listener( event )

def add_event_listener(event_type, listener):
	"""
	Add an event listener for an event type
	"""
	# Add listener to the event type
	if not has_listener( event_type, listener ):
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