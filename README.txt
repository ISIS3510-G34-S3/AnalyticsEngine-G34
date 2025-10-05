In this proyect we implement the layers of our Analytics Pipeline.

In the Llaves directory include the analytics-ingestion.json file with the credentials of the firebase.
Use the specifications under "Postgres" in the .env when creating the postgres database.
Use ingestion_integration\sql\00_schema.sql to create the schema of the postgres database.

To run the ingestion and integration services execute ingestion_integration\run_all.py.
To run the analytics service related to the business question with code Q7, run the command:
    streamlit run presentation\feature_usage_least_often.py