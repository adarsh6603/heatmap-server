from flask import Flask, request, send_file
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
from scipy.interpolate import griddata

app = Flask(__name__)

@app.route('/heatmap', methods=['POST'])
def generate_heatmap():
    data = request.get_json()
    df = pd.DataFrame(data)

    # Make sure coordinates and RSSI exist
    if not all(col in df.columns for col in ['x', 'y', 'rssi']):
        return {"error": "Missing x, y or rssi in input data"}, 400

    # Extract coordinate values
    x = df['x'].values
    y = df['y'].values
    z = df['rssi'].values  # RSSI

    # Create grid for interpolation
    grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

    # Plotting
    plt.figure(figsize=(6, 5))
    plt.imshow(grid_z.T, extent=(min(x), max(x), min(y), max(y)), origin='lower', cmap='coolwarm', aspect='auto')
    plt.colorbar(label='RSSI (dBm)')
    plt.title("WiFi RSSI Heatmap")

    # Save to buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
