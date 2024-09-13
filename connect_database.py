import json
import os

class ConnectDatabase:
    def __init__(self, filename='students_info.json'):
        self.filename = filename
        self.load_data()  # Load existing data from the JSON file into memory

    def load_data(self):
        """Load data from JSON file into memory."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = []

    def save_data(self,new_data):
        """Save data from memory to JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_info(self, student_id, first_name, last_name, state, city, email_address):
        """Add new student info to JSON file."""
        self.load_data()  # Reload data to make sure we're working with the latest state
        new_student = {
            'studentId': student_id,
            'firstName': first_name,
            'lastName': last_name,
            'state': state,
            'city': city,
            'emailAddress': email_address
        }
        self.data.append(new_student)
        self.save_data()

    def loadData(self):
        """Load data from JSON file."""
        self.load_data()
        return self.data

    def update_info(self, student_id, first_name, last_name, state, city, email_address):
        """Update student info in JSON file."""
        self.load_data()
        for student in self.data:
            if student['studentId'] == student_id:
                student.update({
                    'firstName': first_name,
                    'lastName': last_name,
                    'state': state,
                    'city': city,
                    'emailAddress': email_address
                })
                self.save_data()
                return
        raise ValueError(f"Student ID {student_id} not found.")

    def delete_info(self, student_id):
        """Delete student info from JSON file."""
        self.load_data()
        
        # check if data is loaded or not
        if not hasattr(self, 'data') or self.data is None:
            print("No data loaded or 'data' attribute not found.")
            return
        
        found = False
        
        for studentItem in self.data:
            print(studentItem)
            if studentItem["studentId"] == student_id:
                print("Student ID {student_id} is exists")
                self.data.remove(studentItem)
                found = True
                break
            
            if not found:
                print(f"Student ID {student_id} not found.")
                return
            try:
                self.save_data(self.data)
                print(f"Student ID {student_id} successfully deleted.")
            except Exception as e:
                print(f"Error saving data: {e}")
    def search_info(self, student_id=None, first_name=None, last_name=None, state=None, email_address=None, city=None):
        """Search for student info based on given criteria."""
        self.load_data()
        result = []
        for student in self.data:
            if (student_id == student['studentId']):
                result.append(student)
        return result

    def get_all_states(self):
        """Get a list of all unique states."""
        self.load_data()
        states = {student['state'] for student in self.data}
        return list(states)

    def get_all_cities(self):
        """Get a list of all unique cities."""
        self.load_data()
        cities = {student['city'] for student in self.data}
        return list(cities)
