from microdot import Microdot
#from microdot.utemplate import Template
import wifi_config

wifi_config.connect_wifi("TP-Link_4CF8","74610693")

app=Microdot()

@app.route('/')
def index(request):
    return '<html><head><title>Sito di prova</title></head><body><h1>CIAO A TUTTI!</h1><table border="2px"><tr><td>Ciao</td><td>a tutti!</td></tr></table></body></html>',200,{'Content-Type':'text/html'}
#    return Template('index.htm').render(nome='Mondo')
#,200,{'Content-Type':'text/html'}

app.run(port=80)
