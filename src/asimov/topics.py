from __future__ import print_function
import logging
from asimov import event_dispatch
from asimov.event import AsimovEvent
topicManager = None
logger = logging.getLogger(__name__)
def genMethodInvocator(name):
  exec("""
def executeMethod(*args, **kwargs):
  event_dispatch.dispatch_event(AsimovEvent("%s", data=args))
""" % (name))
  return executeMethod

class Namespace(object):
  """
  This class represents a namespace
  """
  def __init__(self):
    self.logger = logging.getLogger(__name__)
  
  def __getattr__(self, name):
        print("Cannot comply, no topic named " + name + " registered")
        raise AttributeError()
  def __str__(self):
      return str(self.__dict__)
  def getNamespaces(self):
      nsList = dict()
      recursiveNameSpaces = dict()
      for name in self.__dict__.keys():
        val = self.__dict__[name]
        
        #If child is a Namespace, add it to the list
        if isinstance(val, Namespace):
          nsList.update({name: val})
          #Now get all namespaces below first level, calling their own getNamespaces() method
          for ns in nsList.values():
            recursiveNameSpaces.update({name + k: v for k, v in ns.getNamespaces().items()})
      nsList.update(recursiveNameSpaces)
      
      #Prepend each with a slash, for formatting reasons
      nsList = {"/" + k: v for k, v in nsList.items()}
      return nsList


class TopicManager(object):
  """
  This class is responsbile for handling topic creation and namespace registration
  """
  def __init__(self):
      self.namespaces = Namespace()
      self.logger = logging.getLogger(__name__)
        
  def registerTopic(self, name, msgType = None):
    """
    Creates a new topic and registers namespaces if required. The topic
    created will only respond to the message type as defined here. Calling
    this method with a different message type WILL OVERRIDE the previous
    definition
    """
    parts = name.split("/")
    namespace = self.namespaces
    self.logger.debug(str(parts))
    if (len(parts) >= 1):
      for n in range(1, len(parts) - 1):
        if parts[n] not in namespace.__dict__:
          namespace.__dict__[parts[n]] = Namespace()
        namespace = namespace.__dict__[parts[n]]
    namespace.__dict__[parts[len(parts) - 1]] = genMethodInvocator(name)
    
      
topicManager = TopicManager()
