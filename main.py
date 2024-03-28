from flask import Flask, render_template
import psutil
import json
import threading

app = Flask(__name__)

cpu_percentages = []
ram_percentages = []

def record_system_usage():
    while True:
        cpu_percent = psutil.cpu_percent(interval=10)  # Collecter les données toutes les 10 secondes
        ram_percent = psutil.virtual_memory().percent
        cpu_percentages.append(cpu_percent)
        ram_percentages.append(ram_percent)
        if len(cpu_percentages) > 360:  # Garder les données des 360 dernières valeurs (10 secondes * 360 = 3600 secondes = 1 heure)
            cpu_percentages.pop(0)
        if len(ram_percentages) > 360:
            ram_percentages.pop(0)
        time.sleep(10)  # Attendre 10 secondes avant de collecter la prochaine donnée

def save_data():
    data = {
        "cpu": cpu_percentages,
        "ram": ram_percentages
    }
    with open("data.json", "w") as f:
        json.dump(data, f)

def load_data():
    global cpu_percentages, ram_percentages
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            cpu_percentages = data["cpu"]
            ram_percentages = data["ram"]
    except FileNotFoundError:
        pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cpu_data')
def cpu_data():
    return json.dumps(cpu_percentages)

@app.route('/ram_data')
def ram_data():
    return json.dumps(ram_percentages)

if __name__ == '__main__':
    import time
    load_data()

    usage_thread = threading.Thread(target=record_system_usage)
    usage_thread.daemon = True
    usage_thread.start()

    save_thread = threading.Thread(target=save_data)
    save_thread.daemon = True
    save_thread.start()

    app.run(debug=True)
