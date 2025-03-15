from flask import Flask, request, jsonify
import pandas as pd

# Load the dataset
csv_file = "medication_lookup_data.csv"  # Update with correct path if needed
medication_data = pd.read_csv(csv_file)

# Initialize Flask app
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_medication():
    query = request.args.get('query', '').strip()
    search_type = request.args.get('type', 'name').strip().lower()
    
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400
    
    if search_type == "gtin":
        result = medication_data[medication_data["GTIN"].astype(str) == query]
    elif search_type == "appid":
        result = medication_data[medication_data["APPID"].astype(str) == query]
    else:  # Default search by medication name
        result = medication_data[medication_data["NM"].str.contains(query, case=False, na=False)]
    
    if result.empty:
        return jsonify({"message": "No matching medication found."}), 404
    
    return jsonify(result.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
