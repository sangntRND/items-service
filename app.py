from flask import Flask, request, jsonify

app = Flask(__name__)

# Hardcoded secret for Trivy to detect
API_KEY = "12345-ABCDE-SECRET-KEY"

# In-memory data storage
data = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data), 200

@app.route('/items', methods=['POST'])
def create_item():
    item = request.json
    data.append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item is not None:
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in data if item['id'] == item_id), None)
    if item is not None:
        updated_item = request.json
        item.update(updated_item)
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    data = [item for item in data if item['id'] != item_id]
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
