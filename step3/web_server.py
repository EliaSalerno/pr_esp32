from microdot import Microdot
import wifi_config

wifi_config.connect_wifi("TP-Link_4CF8","74610693")

app=Microdot()

@app.route('/')
def index(request):
    return 'Ciao da esp32!'

app.run(port=80)
