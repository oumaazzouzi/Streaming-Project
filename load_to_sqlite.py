import pandas as pd
from sqlalchemy import create_engine

# === Chemins ===
csv_path = "data/user_events.csv"        # Ton fichier CSV
sqlite_db_path = "data/streaming.db"  # Fichier SQLite

# === Lire les données du CSV ===
df = pd.read_csv(csv_path)

# === Créer une connexion SQLite ===
engine = create_engine(f"sqlite:///{sqlite_db_path}")

# === Charger les données dans la table "events" ===
df.to_sql("events", con=engine, if_exists="replace", index=False)

print("✅ Données chargées dans la base SQLite.")
