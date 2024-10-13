from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('something.html')

# Route to handle prediction requests
@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the JSON request sent by JavaScript
    data = request.json
    user_input = data.get('userInput')
    if not user_input:
        return jsonify({"error": "No input provided!"}), 400

    # Run the external Python script with the user input
    result = subprocess.run(
        ['python3', 'something.py', user_input], 
        capture_output=True, 
        text=True
    )
    print("hey the subprocess was supposed to run")
    if result.returncode != 0:
        return jsonify({"error": "Error executing Python script"}), 500

    # Return the output from the script as a JSON response
    return jsonify({"prediction": result.stdout})

if __name__ == '__main__':
    app.run(debug=True)