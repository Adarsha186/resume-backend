import functions_framework
from google.cloud import firestore

# Initialize Firestore client with specific database ID
db = firestore.Client(project="t-science-434802-f8", database="counter")

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function to update the visitor counter."""
    
    # Reference to the document in Firestore
    doc_ref = db.collection('viewer_count').document('count')

    try:
        # Use a transaction to safely update the counter
        @firestore.transactional
        def update_counter(transaction, doc_ref):
            snapshot = doc_ref.get(transaction=transaction)
            new_count = snapshot.get('count') + 1
            transaction.update(doc_ref, {'count': new_count})
            return new_count

        # Create a new transaction and update the counter
        transaction = db.transaction()
        updated_count = update_counter(transaction, doc_ref)

        response = f"{updated_count}"
        return (response, 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        })
    except Exception as e:
        return (f"Error updating counter: {str(e)}", 500, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        })
