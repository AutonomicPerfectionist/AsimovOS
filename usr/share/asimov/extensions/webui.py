import subprocess
import logging
from asimov import event_dispatch
from asimov.extension import Extension
from threading import Thread

class WebUI(Extension):
  listeners = {"/asimov/boot/lifecycle": "lifecycle"}
  def lifecycle(self, ev):
    if ev == "start":
  	  Thread(target=lambda *args: subprocess.call("cd usr/share/asimov/extension-lib/webui/; python webui.py", shell=True)).start()
