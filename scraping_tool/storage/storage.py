import json
import os


class JSONDataHandler:
    def __init__(self, file_path):
        """
        Initializes the JSONDataHandler with the given file path.
        :param file_path: Path to the JSON file where data will be saved.
        """
        self.file_path = file_path
        self._initialize_file()
        self.data = self._load_data()

    def _initialize_file(self):
        """
        Ensures the JSON file exists. If not, creates an empty file.
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def _load_data(self):
        """
        Loads and returns the JSON data from the file.
        :return: List of data from the JSON file.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def save_data(self, data):
        """
        Saves the given data back to the JSON file.
        :param data: List of data to save.
        """
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def create_or_update(self, unique_key_identifier, new_data):
        """
        Creates or updates an entry in the JSON data based on a unique key.
        :param unique_key_identifier: The unique key field to identify data (e.g., "product_title").
        :param new_data: The new data to create or update.
        """
        data = self._load_data()
        for entry in data:
            if entry[unique_key_identifier] == new_data[unique_key_identifier]:
                entry.update(new_data)  # Update existing entry
                break
        else:
            data.append(new_data)  # Add new entry if not found
        self.save_data(data)


    def bulk_create_or_update(self, unique_key_identifier, records):
        """
        Updates or creates multiple records in the JSON file.
        :param unique_key_identifier: Key to identify unique records (e.g., 'product_title').
        :param records: List of dictionaries representing new records.
        """
        existing_data = {item[unique_key_identifier]: item for item in self.data}
        for record in records:
            if record[unique_key_identifier] in existing_data:
                existing_data[record[unique_key_identifier]].update(record)
            else:
                existing_data[record[unique_key_identifier]] = record
        data = list(existing_data.values())
        self.save_data(data)
