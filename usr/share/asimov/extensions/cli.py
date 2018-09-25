from asimov.extension import Extension
from asimov import event_dispatch
from asimov.event import AsimovEvent
from asimov import extension
from cmd2 import Cmd
import sys, platform, psutil, threading
class AsiCli(Extension):
  listeners = {"/asimov/boot/finished": "start_cli"}
  def __init__(self):
    event_dispatch.add_event_listener("BOOT-FINISHED", self.start_cli)
  def start_cli(self, ev):
    AsiCliInterpreter().cmdloop()


class AsiCliInterpreter(Cmd):
  def __init__(self):
    Cmd.__init__(self, use_ipython = True)
    self.intro = self.colorize("""
    Welcome to the AsimovOS shell! 
    Type help for information on available commands.
    """, "cyan")
    self.prompt = self.colorize("AsimovOS>", "yellow")
  
  def do_server(self, arg):
    """
    Control the AsimovOS server. Available commands are start and kill
    """
    if "kill" in arg:
      event_dispatch.dispatch_event(AsimovEvent("SERVER-KILL", None, None, "CLIENT"))
      
  def do_enable(self, arg):
    """
    Allows control over Enabler
    """
    extension.enabler.overrides.update({arg: True})
    extension.enabler.resolve_enable()
    
  def do_subps(self, arg):
    """
    Enumerate subprocesses
    """
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    self.poutput(str(children))
    
  def do_threads(self, arg):
    """
    List running threads
    """
    self.poutput(str(threading.enumerate()))
    
  def do_sys_info(self, arg):
    """
    Usage: sys_info
    
    Prints system information
    """
    def linux_distribution():
      try:
        return platform.linux_distribution()
      except:
        return "N/A"
    self.poutput("""Python version: %s
dist: %s
linux_distribution: %s
system: %s
machine: %s
platform: %s
uname: %s
version: %s
mac_ver: %s
""" % (
  sys.version.split('\n'),
  str(platform.dist()),
  linux_distribution(),
  platform.system(),
  platform.machine(),
  platform.platform(),
  platform.uname(),
  platform.version(),
  platform.mac_ver(),
  ))