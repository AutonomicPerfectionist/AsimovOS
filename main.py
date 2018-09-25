import subprocess
from threading import Thread
from asimov import boot
import sys
import time


if __name__ == "__main__":
 
  #Thread(target=server.run).start()
  #Thread(target=lambda *args: subprocess.call("python startClient.py", shell=True)).start()
  boot.init()
