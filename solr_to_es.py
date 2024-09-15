import argparse
import pysolr
from elasticsearch import Elasticsearch, helpers

# Function to retrieve documents from Solr
def get_solr_docs(solr, start=0, rows=100):
    params = {
        'start': start,
        'rows': rows,
    }
    results = solr.search('*:*', **params)
    return results

# Function to transform Solr documents to Elasticsearch format
def transform_solr_doc(solr_doc):
    # Remove reserved fields that cannot be indexed in Elasticsearch
    reserved_fields = ['_version']
    es_doc = {key: value for key, value in solr_doc.items() if key not in reserved_fields}
    return es_doc

# Function to index documents to Elasticsearch
def index_docs_to_es(es, es_index, docs):
    actions = [
        {
            '_index': es_index,
            '_id': doc['id'],
            '_source': transform_solr_doc(doc)
        }
        for doc in docs
    ]
    success, failed = helpers.bulk(es, actions, raise_on_error=False)
    if failed:
        print(f"Failed to index {len(failed)} documents:")
        for item in failed:
            print(item)

# Main function to migrate data
def migrate_data(solr, es, es_index, batch_size=100):
    start = 0
    while True:
        solr_docs = get_solr_docs(solr, start=start, rows=batch_size)
        if len(solr_docs) == 0:
            break
        index_docs_to_es(es, es_index, solr_docs)
        start += batch_size
        print(f'Migrated {start} documents so far...')

# Main entry point
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Migrate data from Solr to Elasticsearch')
    parser.add_argument('solr_url', help='URL of the Solr core')
    parser.add_argument('es_url', help='URL of the Elasticsearch cluster')
    parser.add_argument('es_index', help='Name of the Elasticsearch index')
    parser.add_argument('--rows-per-page', type=int, default=100, help='Number of rows to fetch per page from Solr')
    parser.add_argument('--es-timeout', type=int, default=30, help='Timeout for Elasticsearch (seconds)')
    
    args = parser.parse_args()

    # Initialize Solr and Elasticsearch clients
    solr = pysolr.Solr(args.solr_url, always_commit=True, timeout=10)
    es = Elasticsearch(
           [args.es_url],
           basic_auth=('elastic', 'xW5r152nOYoTjbuZbTn8'),  # Replace with actual credentials
           request_timeout=args.es_timeout,
           verify_certs=False  # Disable SSL verification for development purposes
        )
    # es = Elasticsearch(
    #     [args.es_url],
    #     http_auth=('elastic', 'xW5r152nOYoTjbuZbTn8'),  # Replace 'your_password' with the actual password for the 'elastic' user
    #     request_timeout=args.es_timeout
    # )
     
    try:
        # Check if the Elasticsearch index exists
        if not es.indices.exists(index=args.es_index):
            es.indices.create(index=args.es_index)
        
        migrate_data(solr, es, args.es_index, batch_size=args.rows_per_page)
        print('Migration completed!')
    except Exception as e:
        print(f'An error occurred: {e}')
