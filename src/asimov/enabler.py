import logging
from extension import Extension

class Enabler(object):
  def __init__(self, ext, enable_functions, overrides):
    self.extensions = ext
    self.enabled = list()
    self.enable_functions = enable_functions
    self.overrides = overrides
    self.logger = logging.getLogger(self.__class__.__name__)
    
    self.resolve_enable()
    
  def resolve_enable(self):
    for ext in self.extensions.values():
      if ext.__module__ in self.overrides.keys():
        self.logger.debug("Found override for extension %s" % (ext.__module__ + '.' + ext.__name__))
        if self.overrides[ext.__module__]:
          self.logger.warn("Extension %s forcibly enabled. Enabler script will not be run" % (ext.__module__ + '.' + ext.__name__))
          self.enabled.append(ext())
        else:
          self.logger.warn("Extension %s forcibly disabled. Enabler script will not be run" % (ext.__module__ + '.' + ext.__name__))
        continue
      #If we make it here, ext is not overriden
      if ext.__module__ in self.enable_functions.keys() and self.enable_functions[ext.__module__]():
        self.enabled.append(ext())
      else:
        self.logger.warn("No overrides or Enabler scripts found for extension %s... Implicitly disabling" % (ext.__module__ + '.' + ext.__name__))