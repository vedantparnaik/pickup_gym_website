import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('gym_schedule.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table for the gym schedule
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_slot TEXT NOT NULL,
    availability TEXT NOT NULL
)
''')

# Insert initial data
cursor.executemany('''
INSERT INTO schedule (time_slot, availability)
VALUES (?, ?)
''', [
    ('6:00 AM - 7:00 AM', 'Available'),
    ('7:00 AM - 8:00 AM', 'Full'),
    ('8:00 AM - 9:00 AM', 'Available')
])

# Commit and close the connection
conn.commit()
conn.close()
print("Database setup complete.")
