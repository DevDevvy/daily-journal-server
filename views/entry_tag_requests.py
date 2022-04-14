import sqlite3
import json
from models.entry_tag import Entry_tag


def get_all_entry_tags():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.journal_entry_id,
            t.tag_id
        FROM Entry_tags t
        ORDER BY id DESC
        """)

        # Initialize an empty list to hold all entry_tag representations
        entry_tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry_tag instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # entry_Tag class above.
            entry_tag = Entry_tag(row['id'], row['journal_entry_id'], row['tag_id'])
            
           
            # Add the dictionary representation of the entry_tag to the list
            entry_tags.append(entry_tag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entry_tags)