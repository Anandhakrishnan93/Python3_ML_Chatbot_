import csv

class TravelDataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.questions = []
        self.answers = []

    def load(self):
        """Reads the CSV and populates lists. Returns True if successful."""
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.questions = []
                self.answers = []
                for row in reader:
                    self.questions.append(row['Question'])
                    self.answers.append(row['Answer'])
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False