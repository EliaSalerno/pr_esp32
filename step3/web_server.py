from microdot import Microdot
from microdot.utemplate import Template
import wifi_config

wifi_config.connect_wifi("TP-Link_4CF8","74610693")

app=Microdot()

@app.route('/')
def index(request):
    return Template('index.htm').render(nome='Mondo')
#,200,{'Content-Type':'text/html'}

app.run(port=80)
