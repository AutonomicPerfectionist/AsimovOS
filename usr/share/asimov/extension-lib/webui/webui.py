import platform
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.debug = True
  
def run():
  #app.run(port=8888, host="0.0.0.0")
  app.run(port=8888)
  with app.app_context():
    url_for("asimov", filename="server.py")
@app.route("/system")
def sys_info():
  """
  Usage: sys_info
  
  Prints system information
  """
  def linux_distribution():
    try:
      return platform.linux_distribution()
    except:
      return "N/A"
  return ('''<h5>Python version:</h5> %s
<h5>linux_distribution:</h5> %s
<h5>system:</h5> %s
<h5>machine:</h5> %s
<h5>platform:</h5> %s
<h5>uname:</h5> %s
<h5>version:</h5> %s
<h5>mac_ver:</h5> %s
''' % (
  sys.version.split('\n'),
  linux_distribution(),
  platform.system(),
  platform.machine(),
  platform.platform(),
  platform.uname(),
  platform.version(),
  platform.mac_ver(),
  ))

@app.route('/')
def index():
   return render_template("index.html", system_info=sys_info())

run()

