# secure-solr-elasticsearch-bulk-migration
This project provides a Python script to migrate bulk data from a Solr core to an Elasticsearch index, with added security for Elasticsearch authentication.

Prerequisites
Before running the migration script, make sure you have the following:

Python installed on your machine.
Solr and Elasticsearch running.
Solr accessible at localhost:8983
Elasticsearch accessible at localhost:9200

Solr Commands
Start Solr:

solr start

Stop Solr:

solr stop -all

Access Solr Admin UI: http://localhost:8983/solr

Create a Core in Solr:

solr create -c core_name

Python Package Requirements
Install the necessary Python packages:


pip install pysolr
pip install elasticsearch
pip install solr-to-es
pip install --upgrade setuptools
Migration Script
Usage
The migration script transfers data from a Solr core to an Elasticsearch index, removing reserved fields that Elasticsearch doesn't accept.

Command to Run the Migration

python solr_to_es.py <solr_core_url> <elasticsearch_url> <elasticsearch_index_name> --rows-per-page 500 --es-timeout 60



python solr_to_es.py http://localhost:8983/solr/test http://localhost:9200 es_index --rows-per-page 500 --es-timeout 60




Arguments
solr_core_url: The URL of the Solr core from which data will be exported.
elasticsearch_url: The URL of the Elasticsearch cluster to which data will be migrated.
elasticsearch_index_name: The name of the Elasticsearch index where data will be stored.
--rows-per-page: (Optional) The number of rows to fetch from Solr per page. Default is 100.
--es-timeout: (Optional) The timeout in seconds for Elasticsearch. Default is 30.
Helper Function
The script uses a helper function to transform Solr documents by removing fields that cannot be indexed in Elasticsearch (such as _version).

Example Solr Commands
Delete a document from Solr:

curl -XPOST "http://localhost:8983/solr/your_core/update?commit=true" -d "<delete><id>document_id</id></delete>"




Delete all documents from Solr:

<delete>
  <query>*:*</query>
</delete>
Search Query in Solr:

Example to find documents where name starts with 'ra':

name=*ra*
Sorting Results: Use the sort parameter in Solr to order results, e.g., by age asc or age desc.

Retrieve Specific Fields: Use the fl parameter in Solr to retrieve specific fields, such as:

fl=name,age
Elasticsearch Setup
The script checks if the Elasticsearch index exists. If it doesn’t, the script will automatically create it before migrating the data.
