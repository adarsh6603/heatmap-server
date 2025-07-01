from flask import Flask, request, send_file
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "Heatmap server is running"

@app.route('/heatmap', methods=['POST'])
def generate_heatmap():
    data = request.get_json()
    df = pd.DataFrame(data)
    heatmap_data = df.pivot(index='y', columns='x', values='rssi')

    plt.figure(figsize=(6, 4))
    sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", cbar_kws={'label': 'RSSI'})
    plt.gca().invert_yaxis()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
