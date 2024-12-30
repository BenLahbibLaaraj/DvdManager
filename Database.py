import sqlite3
import time


class Database:
    def create(self):
        db = sqlite3.connect('DVDManager.db')
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DVD (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                release_date TEXT,
                language TEXT,
                barcode INTEGER
            )
        ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Actor (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    dvd_id INTEGER NOT NULL,      
                    FOREIGN KEY (dvd_id) REFERENCES DVD (id)
                )
            ''')
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS Character (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    actor_id INTEGER NOT NULL,
                    FOREIGN KEY (actor_id) REFERENCES Actor (id)
                )
            ''')
        db.commit()
        db.close()


class DVDMod:
    def _connect_db(self):
        return sqlite3.connect('DVDManager.db')

    def insertdvd(self, title, release_date, language, barcode=None):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT title FROM DVD WHERE title = ?', (title,))
        existing_dvd = cursor.fetchone()
        if existing_dvd:
            print("DVD already added")
        else:
            if barcode is None:
                cursor.execute("INSERT INTO DVD (title, release_date, language) VALUES (?, ?, ?)",
                               (title, release_date, language))
            else:
                cursor.execute("INSERT INTO DVD (title, release_date, language, barcode) VALUES (?, ?, ?, ?)",
                               (title, release_date, language, barcode))
            db.commit()
            print("DVD Added")
        db.close()

    def readdvd(self, id):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT title, release_date, language FROM DVD WHERE id = ?', (id,))
        dvd = cursor.fetchone()
        db.close()
        return dvd

    def removedvd(self, title):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM DVD WHERE title = ?', (title,))
        existing_dvd = cursor.fetchone()
        if existing_dvd:
            cursor.execute('DELETE FROM DVD WHERE title = ?', (title,))
            db.commit()
            print("DVD Removed")
        else:
            print("DVD not found")
        db.close()

    def updatedvd(self, orgtitle, title=None, barcode=None):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT id, title, release_date, language, barcode FROM DVD WHERE title = ?', (orgtitle,))
        dvd = cursor.fetchone()
        if dvd:
            print("DVD found")
            time.sleep(2)
            title = title or dvd[1]
            barcode = barcode or dvd[4]
            cursor.execute('UPDATE DVD SET title = ?, release_date = ?, language = ?, barcode = ? WHERE id = ?',
                           (title, dvd[2], dvd[3], barcode, dvd[0]))
            db.commit()
            print("DVD Updated")
        else:
            print("DVD not found")
        db.close()

    def listDVD(self):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM DVD')
        dvd_records = cursor.fetchall()
        if dvd_records:
            print("{:<5} {:<20} {:<15} {:<15} {:<10}".format("ID", "Title", "Release Date", "Language", "Barcode"))
            print("-" * 70)
            for record in dvd_records:
                formatted_record = tuple('NULL' if value is None else value for value in record)
                print("{:<5} {:<20} {:<15} {:<15} {:<10}".format(*formatted_record))
        else:
            print("The 'DVD' table is empty.")
        db.close()


class ActorMod:
    def _connect_db(self):
        return sqlite3.connect('DVDManager.db')

    def addActor(self, actorName, dvdTitle):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM DVD WHERE title = ?', (dvdTitle,))
        existing_dvd = cursor.fetchone()
        if existing_dvd:
            cursor.execute("INSERT INTO Actor (name, dvd_id) VALUES (?, ?)", (actorName, existing_dvd[0]))
            db.commit()
            print("Actor added successfully.")
        else:
            print("DVD not found in the database.")
        db.close()

    def listActor(self):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Actor')
        dvd_records = cursor.fetchall()
        if dvd_records:
            print("{:<5} {:<20} {:<15}".format("ID", "Name", "Dvd_id"))
            print("-" * 70)
            for record in dvd_records:
                formatted_record = tuple('NULL' if value is None else value for value in record)
                print("{:<5} {:<20} {:<15}".format(*formatted_record))
        else:
            print("The 'Actor' table is empty.")
        db.close()


class CharacterMod:
    def _connect_db(self):
        return sqlite3.connect('DVDManager.db')

    def addCharacter(self, characterName, actorName):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT id FROM Actor WHERE name = ?', (actorName,))
        existing_actor = cursor.fetchone()
        if existing_actor:
            cursor.execute("INSERT INTO Character (name, actor_id) VALUES (?, ?)",
                           (characterName, existing_actor[0]))
            db.commit()
            print("Character added successfully.")
        else:
            print("Actor not found in the database.")
        db.close()

    def listCharacters(self):
        db = self._connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Character')
        dvd_records = cursor.fetchall()
        if dvd_records:
            print("{:<5} {:<20} {:<15}".format("ID", "Name", "Actor_id"))
            print("-" * 70)
            for record in dvd_records:
                formatted_record = tuple('NULL' if value is None else value for value in record)
                print("{:<5} {:<20} {:<15}".format(*formatted_record))
        else:
            print("The 'Character' table is empty.")
        db.close()
