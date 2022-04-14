import sqlite3
import json
from models.entry_tag import Entry_tag

from models.tag import Tag

def get_all_tags():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.tag_name
        FROM Tags t
        """)

        # Initialize an empty list to hold all animal representations
        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            # Create an entry instance from the current row
            tag = Tag(row['id'], row['tag_name'])
            tags.append(tag.__dict__)
            # Use `json` package to properly serialize list as JSON
    return json.dumps(tags)

def get_all_entry_tags():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.tag_id,
            t.journal_entry_id
        FROM Tags t
        """)

        # Initialize an empty list to hold all animal representations
        entry_tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            # Create an entry instance from the current row
            entry_tag = Entry_tag(row['id'], row['tag_id'], row['journal_entry_id'])
            entry_tags.append(entry_tag.__dict__)
            # Use `json` package to properly serialize list as JSON
    return json.dumps(entry_tags)

def create_entry_tag(new_entry):
    # connect to database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        # make SQL query
        db_cursor.execute("""
        INSERT INTO  Entry_tags
            ( tag_id, journal_entry_id)
        VALUES
        ( ?, ? );
        """, ( new_entry['tag_id'], new_entry['Journal_entry_id'] ))
        
    return json.dumps(new_entry)