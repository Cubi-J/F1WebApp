from flask import Flask, render_template, jsonify
import httpx

# Functions

def fetch_data(url):
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}

app = Flask(__name__)
drivers_url = "https://api.openf1.org/v1/drivers?session_key=latest"

@app.route('/')
def index():
    return render_template('index.html')


    
@app.route('/drivers')
def drivers():
    drivers_list = fetch_data(drivers_url) # Assuming the API returns a list of drivers directly
    return render_template('drivers.html', drivers=drivers_list)

if __name__ == "__main__":
    app.run(debug=True)
