import os
import sys
import sqlite3
sys.path.append(os.getcwd())

if __name__ == '__main__':
    conn = sqlite3.connect('rooms.db')
    conn.execute('''CREATE TABLE rooms (room text, course text, start_time real, end_time real, prof text)''')
    conn.commit()
    conn.close()



