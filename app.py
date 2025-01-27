from flask import Flask, render_template_string, request,url_for
import random

app = Flask(__name__)

# Simulated graph filenames in 'static' directory
GRAPH_FILES = {
    "NO2 Concentration": "graph1.png",
    "O3 Concentration": "graph2.png",
    "CO Concentration": "graph3.png",
    "HCHO Concentration": "graph4.png",
    "SO2 Concentration": "graph5.png",
    "CH4 Concentration": "graph6.png",
    "Relative Humidity": "graph7.png",
    "Temperature": "graph8.png"
}

# Set a fixed seed for consistent random values per session
random.seed(42)
CARD_VALUES = {
    "NO2 Concentration": f"{random.uniform(20, 40):.2f} µg/m³",
    "O3 Concentration": f"{random.uniform(40, 60):.2f} µg/m³",
    "CO Concentration": f"{random.uniform(5, 15):.2f} µg/m³",
    "HCHO Concentration": f"{random.uniform(5, 20):.2f} µg/m³",
    "SO2 Concentration": f"{random.uniform(5, 10):.2f} µg/m³",
    "CH4 Concentration": f"{random.uniform(50, 150):.2f} µg/m³",
    "Relative Humidity": f"{random.uniform(30, 70):.2f} %",
    "Temperature": f"{random.uniform(10, 30):.2f} °C"
}

# HTML Template with Form, Consistent Values, and Units
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Quality Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body, html {
            height: 100%;
            margin: 0;
            background: url('ui1.jpg')
            background-size: cover;
            background-color:#0b0742;
        }
        h1 {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
            background: linear-gradient(to right, #32CD32, #228B22);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .card {
            width: 200px;
            height: 150px;
            margin: 15px;
            background: linear-gradient(to bottom right, #4da3ff, #0066cc);
            color: white;
            text-align: center;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            cursor: pointer;
        }
        .card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            padding: 20px;
        }
        .left-panel {
            width: 300px;
            margin-left: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            color: black;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-label {
            font-weight: bold;
        }
        .modal-img {
            width: 100%;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>Air Quality Indicator</h1>
    <div class="d-flex">
        <!-- Left Panel for AQI Calculation -->
        <div class="left-panel">
            <h4>Calculate AQI</h4>
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">Temperature (°C)</label>
                    <input type="number" step="0.1" name="temperature" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label class="form-label">Relative Humidity (%)</label>
                    <input type="number" step="0.1" name="humidity" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-success w-100">Calculate AQI</button>
            </form>
            {% if aqi %}
            <div class="mt-3">
                <h5>Estimated AQI: <span class="badge bg-primary">{{ aqi }}</span></h5>
            </div>
            {% endif %}
        </div>

        <!-- Cards for Values -->
        <div class="container">
            {% for gas, value in values.items() %}
            <div class="card" data-bs-toggle="modal" data-bs-target="#graphModal" onclick="showGraph('{{ graphs[gas] }}', '{{ gas }}')">
                <div class="card-body d-flex flex-column justify-content-center align-items-center">
                    <h4 class="mb-1">{{ value.split()[0] }}</h4>
                    <small>{{ gas }}</small>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Modal for Displaying Graphs -->
    <div class="modal fade" id="graphModal" tabindex="-1" aria-labelledby="graphModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="graphModalLabel">Graph</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <img id="graphImage" class="modal-img" src="" alt="Graph Image">
                </div>
            </div>
        </div>
    </div>

    <script>
        function showGraph(filename, title) {
            document.getElementById("graphImage").src = "/static/" + filename;
            document.getElementById("graphModalLabel").innerText = title;
        }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    aqi = None
    if request.method == 'POST':
        # Simulate AQI calculation using temperature and humidity
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        aqi = round(temperature * 0.5 + humidity * 0.5)  # Simplified AQI formula
    return render_template_string(HTML_TEMPLATE, graphs=GRAPH_FILES, values=CARD_VALUES, aqi=aqi)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
