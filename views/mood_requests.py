import json
import sqlite3

from models.mood import Mood


def get_all_moods():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)

        # Initialize an empty list to hold all animal representations
        moods = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            # Create an entry instance from the current row
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)
            # Use `json` package to properly serialize list as JSON
    return json.dumps(moods)

def get_single_mood(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """, ( id, ))
        
        data = db_cursor.fetchone()
        # Create an entry instance from the current row
        mood = Mood(data['id'], data['label'])
    # Use `json` package to properly serialize list as JSON
    return json.dumps(mood)