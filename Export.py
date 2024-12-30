import sqlite3
import csv
import os

class Export:

    def _validate_table_name(self, table_name):
        """Validate the table name to ensure it only contains safe characters."""
        allowed_characters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        return all(c in allowed_characters for c in table_name)

    def export_to_csv(self, table_name, csv_filename):
        
        if not self._validate_table_name(table_name):
            print(f"Invalid table name: {table_name}. Only alphanumeric characters and underscores are allowed.")
            return
        
        try:
            
            with sqlite3.connect('DVDManager.db') as conn:
                cursor = conn.cursor()


                cursor.execute(f'SELECT * FROM {table_name}')
                rows = cursor.fetchall()

                if rows:
                    column_names = [description[0] for description in cursor.description]

                    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        csv_writer.writerow(column_names)  # Write the header
                        csv_writer.writerows(rows)  # Write the data

                    print(f"Exported '{table_name}' to '{csv_filename}'.")
                else:
                    print(f"No data found in '{table_name}'.")

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Error: {e}")
