from flask import Flask, jsonify, request
from google.cloud import firestore
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore client with specific database ID
db = firestore.Client(project="t-science-434802-f8", database="counter")

@app.route('/', methods=['GET'])
def hello_http():
    """Flask route to update the visitor counter."""
    
    # Reference to the document in Firestore
    doc_ref = db.collection('viewer_count').document('count')

    try:
        # Use a transaction to safely update the counter
        @firestore.transactional
        def update_counter(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            new_count = snapshot.get('count') + 2
            transaction.update(doc_ref, {'count': new_count})
            return new_count

        # Create a new transaction and update the counter
        transaction = db.transaction()
        updated_count = update_counter(transaction, doc_ref)

        # Return the updated count as a response
        return jsonify({"updated_count": updated_count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Make the app listen on the correct port for Cloud Run
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
