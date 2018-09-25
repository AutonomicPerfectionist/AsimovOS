from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
from RestrictedPython.transformer import RestrictingNodeTransformer
from RestrictedPython.transformer import copy_locations
from asimov import event_dispatch
from asimov import topics
from abc import ABCMeta
from abc import abstractmethod
import sys
import os
import ast
import logging
import warnings
registered_extensions = dict()
enabler = None
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore', "Parent module")
class ExtensionMeta(ABCMeta):
	def __new__(cls, name, bases, dict):
		ext = super(ExtensionMeta, cls).__new__(cls, name, bases, dict)
		if ext.__name__ is not "Extension":
			cls.registerExtension(ext)
			ext.logger = logging.getLogger(ext.__module__ + '.' + ext.__name__)
		return ext

	@classmethod
	def registerExtension(cls, ext):
		logger.debug("Registered extension: " + ext.__name__)
		registered_extensions.update({ext.__name__: ext})
		
			


class Extension(object):
	__metaclass__ = ExtensionMeta
	logger = None
	listeners = dict()
	publishers = list()
	messages = topics.topicManager.namespaces
	def __new__(cls):
	  self = super(Extension, cls).__new__(cls)
          self.logger.debug(self.__class__.__name__ + ".listeners.keys() = " + str(self.listeners.keys()))
	  for topic, listener in self.listeners.items():
	    self.logger.debug("Listening on topic " + topic)
	    topics.topicManager.registerTopic(topic)
	    event_dispatch.add_event_listener(topic, getattr(self, listener))
	  return self

	#@abstractmethod
	def test(self):
		pass

	
class ExtensionPolicy(RestrictingNodeTransformer):
  def check_name(self, node, name):
        if name is None:
            return

        elif name.endswith('__roles__'):
            self.error(node, '"%s" is an invalid variable name because '
                       'it ends with "__roles__".' % name)

        elif name == "printed":
            self.error(node, '"printed" is a reserved name.')

        elif name == 'print':
            # Assignments to 'print' would lead to funny results.
            self.error(node, '"print" is a reserved name.')
            
  def visit_Attribute(self, node):
        """Checks and mutates attribute access/assignment.
        'a.b' becomes '_getattr_(a, "b")'
        'a.b = c' becomes '_write_(a).b = c'
        'del a.b' becomes 'del _write_(a).b'
        The _write_ function should return a security proxy.
        """

        if node.attr.endswith('__roles__'):
            self.error(
                node,
                '"{name}" is an invalid attribute name because it ends '
                'with "__roles__".'.format(name=node.attr))

        if isinstance(node.ctx, ast.Load):
            node = self.node_contents_visit(node)
            new_node = ast.Call(
                func=ast.Name('_getattr_', ast.Load()),
                args=[node.value, ast.Str(node.attr)],
                keywords=[])

            copy_locations(new_node, node)
            return new_node

        elif isinstance(node.ctx, (ast.Store, ast.Del)):
            node = self.node_contents_visit(node)
            new_value = ast.Call(
                func=ast.Name('_write_', ast.Load()),
                args=[node.value],
                keywords=[])

            copy_locations(new_value, node.value)
            node.value = new_value
            return node

        else:
            return self.node_contents_visit(node)


def load_extensions(folder, recursive=False):
  
  for name, code in read_extensions(folder, recursive).iteritems():
    byte_code = compile(code, name, 'exec') #,policy=ExtensionPolicy)
    global_vars = {}
    global_vars.update(globals())
    #global_vars.update({"__builtins__": safe_builtins})
    global_vars.update({"__name__": name})
    #global_vars.update({"__write__": lambda x: x})
    #global_vars['__builtins__'].update({"__import__": __import__})
    exec(byte_code, global_vars)

def read_extensions(folder, recursive=False):
  walk_dir = folder
  extension_code = dict()
  
  logger.debug('walk_dir = ' + walk_dir)
  
  # If your current working directory may change during script  execution, it's recommended to
  # immediately convert program arguments to an absolute path. Then the variable root below will
  # be an absolute path as well. Example:
  # walk_dir = os.path.abspath(walk_dir)
  logger.debug('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

  for root, subdirs, files in os.walk(walk_dir):
    logger.debug('--\nExtension Directory Root = ' + root)
    for subdir in subdirs:
        logger.debug('\t- subdirectory ' + subdir)
          
    for filename in files:
      file_path = os.path.join(root, filename)
      logger.debug('\t- file %s (full path: %s)' % (filename, file_path))
      if filename.endswith(".py"):
        with open(file_path, 'rb') as f:
          f_content = f.read()
          logger.debug("Opened a python file")
          extension_code.update({"extensions." + filename.split('.')[0]: f_content})
            

  return extension_code
