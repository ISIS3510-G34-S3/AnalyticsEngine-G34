In this proyect we implement the layers of our Analytics Pipeline.

In the Llaves directory include the analytics-ingestion.json file with the credentials of the firebase.
Use the specifications under "Postgres" in the .env when creating the postgres database.
Use ingestion_integration\sql\00_schema.sql to create the schema of the postgres database.

To run the ingestion and integration services execute ingestion_integration\run_all.py.

AVAILABLE ANALYTICS DASHBOARDS:

To run the analytics dashboards, you can use the runner scripts or run them individually:

Quick Start (using runner):
    run_dashboard.ps1    (PowerShell - Recommended)
    run_dashboard.bat    (Command Prompt)

Individual Dashboard Commands:

1. Main Dashboard Launcher (Overview of all business questions):
    streamlit run presentation\dashboard_launcher.py

2. Q7 - Feature Usage Analysis (Least-used features identification):
    Business Question: Which app features (e.g., messaging hosts, filtering by sustainability, calendar booking) are used least often and may need redesign or removal?
    Type: Type 3 (Feature Analysis)
    Owner: Andrés Felipe Gómez García
    Command: streamlit run presentation\feature_usage_least_often.py

3. Q9 - Host Verification Impact Analysis:
    Business Question: How does the host verification feature affect the number of bookings compared to unverified hosts?
    Type: Type 3 (Product Feature Analysis)
    Owner: Juan Diego Osorio
    Command: streamlit run presentation\q9_host_verification_impact.py

4. Q11 - Authentic Experience Regions Analysis:
    Business Question: Which regions in Colombia show the highest concentration of authentic experience bookings and how could this aggregated data be shared with regional tourism boards?
    Type: Type 4 (External Data Sharing)
    Owner: Ignacio Chaparro
    Command: streamlit run presentation\q11_authentic_experiences_regions.py

5. Q12 - Regional Offers for Public Entities Analysis:
    Business Question: Which regions in Colombia have the greatest concentrations of experience offers, what are most of these offers typically like, and how could this information be useful to public entities?
    Type: Type 4 (External Data Sharing)
    Owner: Santiago Arenas
    Command: streamlit run presentation\q12_regional_offers_public_entities.py

6. Q16 - Device Distribution Monthly:
    Business Question: What is the distribution of devices where our app is installed on?
    Type: Type 1 (App Telemetry)
    Owner: Andrés Felipe Gómez García
    Command: streamlit run presentation\device_distribution_monthly.py

7. Q17 - Common Skills in Top Departments:
   Business Question: What are the most common “skills to learn” in the experiences of the top 5 departments with the highest number of experiences?
   Type: Type 4 (Benfits from Data)
   Owner: Andrés Felipe Gómez García
   Command: streamlit run presentation\skills_top5_departments.py

NOTES:
- All dashboards include mock data functionality when the database is not available
- Dashboards are designed for different stakeholder types (product teams, tourism boards, public entities)
- Real-time data requires proper database setup and Firebase credentials
- Default port is 8501, but can be changed using --server.port parameter