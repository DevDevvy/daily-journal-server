import json
import sqlite3

from models import Entry
from models.mood import Mood
from models.tag import Tag



def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id,
            m.label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.mood_id
        """)

        # Initialize an empty list to hold all entry representations
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            # Create an entry instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])
            mood = Mood(row['id'], row['label'])
            
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
            
            db_cursor.execute("""
                SELECT t.id, t.tag_name
                FROM entry_tags en
                JOIN tags t ON t.id = en.tag_id
                WHERE en.journal_entry_id = ?
            """, (entry.id, ))
            
            tags = []
            
            tag_dataset = db_cursor.fetchall()
            
            for tag_row in tag_dataset:
                tags.append(tag_row['id'])
                
            entry.tags = tags
            
            # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement. WHERE acts as filter
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.id,
            m.label
        FROM entries e
        JOIN moods m
            ON m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        # finding single row uses fetchone instead of fetchall
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'], data['mood_id'], data['date'])
        mood = Mood(data['id'], data['label'])
        entry.mood = mood.__dict__
    return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entries
        WHERE id = ?
        """, (id, ))
        
        
def search_entries(term):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            e.id
        FROM entries e
        WHERE entry LIKE ?
        """, ( '%' + term + '%', ))
        
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            # Create an entry instance from the current row
            entry = Entry(row['concept'], row['entry'], row['mood_id'],
                            row['date'], row['id'])
            entries.append(entry.__dict__)
            # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def create_journal_entry(new_entry):
    # connect to database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        # make SQL query
        db_cursor.execute("""
        INSERT INTO  entries
            ( concept, entry, mood_id, date)
        VALUES
        ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['entry'], 
              new_entry['mood_id'], new_entry['date'] ))
        
        id = db_cursor.lastrowid
        new_entry['id'] = id
        
        
        
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entry_tags
                (tag_id, journal_entry_id)
            VALUES
                (?, ?);
            """, (tag, new_entry['id']))
            
            
    return json.dumps(new_entry)


def update_entry(id, new_entry):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date'], id ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
        
        
