import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._create_table()
    
    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS targets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """)
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS subdomains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_seen_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(target_id, name),
                FOREIGN KEY (target_id) REFERENCES targets (id)
            );
        """)
        self.conn.commit()

    def get_or_create_target(self, target_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM targets WHERE name = ?", (target_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            cursor.execute("INSERT INTO targets (name) VALUES (?)", (target_name,))
            self.conn.commit()
            return cursor.lastrowid

    def get_active_subdomains(self, target_id):
        cursor = self.conn.cursor() 
        cursor.execute("SELECT name from subdomains WHERE is_active = TRUE and target_id = ?", (target_id,))
        return {row[0] for row in cursor.fetchall()}

    def update_subdomains(self, target_id, new_subdomains, old_subdomains):
        added_subdomains = new_subdomains - old_subdomains
        removed_subdomains = old_subdomains - new_subdomains
        unchanged_subdomains = new_subdomains.intersection(old_subdomains)

        cursor = self.conn.cursor()

        if added_subdomains:
             cursor.executemany(
                "INSERT OR IGNORE INTO subdomains (target_id, name) VALUES (?, ?)",
                [(target_id, name) for name in added_subdomains]
            )

        if removed_subdomains:
            cursor.executemany(
                "UPDATE subdomains SET is_active = FALSE WHERE target_id = ? AND name = ?",
                [(target_id, name) for name in removed_subdomains]
            )

        if unchanged_subdomains:
            cursor.executemany(
                "UPDATE subdomains SET last_seen_at = CURRENT_TIMESTAMP WHERE target_id = ? AND name = ?",
                [(target_id, name) for name in unchanged_subdomains]
            )

        self.conn.commit()
