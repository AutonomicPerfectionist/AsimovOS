class AsimovEvent( object ):
    """
    Event object to use with MEventDispatch.
    """

    def __init__(self, event_type, url, port, nodeType, data=None):
        """
        The constructor accepts an event type as string and a custom data
        """
        self._type = event_type
	self.url = url
	self.port = port
	self.nodeType = nodeType
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
