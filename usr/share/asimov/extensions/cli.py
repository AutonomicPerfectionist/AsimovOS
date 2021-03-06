from asimov.extension import Extension
from asimov import event_dispatch
from asimov.event import AsimovEvent
from asimov import extension
from cmd2 import Cmd
import time
import ctypes
import sys, platform, psutil, threading
def hello(self, hoi):
  self.poutput("Hi!")

class AsiCli(extension.Extension):
  listeners = {"/asimov/extension/cli/add_command": "add_command", "/asimov/boot/finished": "start_cli", "/asimov/boot/lifecycle": "lifecycle"}
  def __init__(self):
    event_dispatch.add_event_listener("BOOT-FINISHED", self.start_cli)
    #self.messages.asimov.extension.cli.add_command(hello)

  def lifecycle(self, ev):
    if ev == "start":
      event_dispatch.dispatch_event(AsimovEvent("/asimov/extension/cli/prerun_hook", None))
      pass
  def add_command(self, command_func, command_string, help_text):
    setattr(AsiCliInterpreter, "help_%s" % (command_string), lambda x: x.poutput(help_text))
    setattr(AsiCliInterpreter,"do_%s" % (command_string), command_func)

  def start_cli(self):
    #hello.__doc__ = "This is a test"

    #AsiCliInterpreter.__dict__.update({"do_hello": hello})
    #self.logger.debug("Starting CLI")
    a = AsiCliInterpreter()
    #a = Cmd()
    threading.Thread(target=a.cmdloop).start()

class AsiCliInterpreter(Cmd):

  def __init__(self):
    Cmd.__init__(self, use_ipython = True)
    self.intro = self.get_logo() + self.colorize("""

    Welcome to the AsimovOS shell!
    Type help for information on available commands.
    """, "cyan")
    self.prompt = self.colorize("AsimovOS>", "yellow")
    self.allow_cli_args = False

  def do_exit(self, arg):
    """
    Shutdown system immediately
    """
    self.do_quit(arg)

  def do_quit(self, arg):
    """
    Shutdown system immediately
    """
    event_dispatch.dispatch_event(AsimovEvent("/asimov/system/shutdown", []))
    

  def do_server(self, arg):
    """
    Control the AsimovOS server. Available commands are start, stop, and kill. Stop and kill are synonymous.
    """
    if "kill" in arg or "stop" in arg:
      event_dispatch.dispatch_event(AsimovEvent("/asimov/extension/server/kill", []))
    elif "start" in arg:
      event_dispatch.dispatch_event(AsimovEvent("/asimov/extension/server/start", []))
      
  def do_dispatch(self, arg):
    """
    Usage: dispatch {topic} {arg1} {arg2}...
    Due to limitations in the CLI, all args are converted to strings, thus topics expecting other types will fail
    """
    args = arg.split(" ")
    topic = args[0]
    event_dispatch.dispatch_event(AsimovEvent(topic, args[1:]))

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
  

  def get_logo(self):
    """Asimov logo translated to ANSI art"""
    return """
                       [0m
            [38;5;231m##[38;5;231m##[38;5;231m##[38;5;231m##          [0m
              [38;5;231m##[38;5;231m##[38;5;231m##          [0m
        [38;5;80m##[38;5;80m##[38;5;80m##[38;5;231m##[38;5;231m##[38;5;231m##[38;5;231m##        [0m
        [38;5;80m##[38;5;80m##[38;5;80m##  [38;5;231m##[38;5;231m##[38;5;231m##[38;5;231m##      [0m
      [38;5;80m##[38;5;80m##[38;5;80m##      [38;5;231m##[38;5;231m##[38;5;231m##      [0m
    [38;5;37m##[38;5;80m##[38;5;80m##[38;5;80m#       [38;5;231m##[38;5;231m##[38;5;231m##[38;5;195m##    [0m
    [38;5;80m##[38;5;80m##[38;5;80m##[38;5;80m#         [38;5;231m##[38;5;231m##[38;5;231m##    [0m
  [38;5;80m##[38;5;80m##[38;5;80m##[38;5;80m##          [38;5;231m##[38;5;231m##[38;5;231m##    [0m
  [38;5;80m##[38;5;80m##[38;5;80m##              [38;5;231m##      [0m
  [38;5;80m##[38;5;80m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[0m
  [38;5;80m #[38;5;80m##  [38;5;167m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##  [0m
          [38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##[38;5;203m##   """
                       
