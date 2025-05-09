import pandas as pd
from sqlalchemy import create_engine

# Connexion à la base SQLite
engine = create_engine("sqlite:///data/streaming.db")

# Requête SQL
query = "SELECT event_type, COUNT(*) as count FROM events GROUP BY event_type;"
result = pd.read_sql_query(query, engine)

print(result)
