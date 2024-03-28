from flask import Flask, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    # Obtention de l'utilisation totale du CPU
    cpu_usage = psutil.cpu_percent(interval=0.1, percpu=False)
    memory = psutil.virtual_memory().percent
    
    if "chrome.exe" in (p.name() for p in psutil.process_iter()):
        server_status = "ON"
    else:
        server_status = "OFF"

    return render_template('index.html', cpu_usage=cpu_usage, memory=memory, server_status=server_status)

if __name__ == '__main__':
    app.run(debug=True)


# ecrit une fonction qui retourne le pourcentage d'utilisation du CPU