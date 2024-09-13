import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem,QDialog
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

# import the UI and Database connection class
from main_ui import Ui_MainWindow
from connect_database import ConnectDatabase

# Create a main Window class

class MainWindow(QMainWindow):  
    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Initialize the UI properly

        #create a database connection object
        self.db = ConnectDatabase()

        # connect UI elements to class variables
        self.student_id = self.ui.lineEdit
        # restrict input to integers
        self.student_id.setValidator(QIntValidator())

        self.first_name = self.ui.lineEdit_2
        self.last_name = self.ui.lineEdit_3
        self.email_address = self.ui.lineEdit_4
        self.state = self.ui.comboBox
        self.city = self.ui.comboBox_2

        self.addBtn = self.ui.addBtn
        self.updateBtn = self.ui.updateBtn
        self.deleteBtn = self.ui.deleteBtn
        self.clearBtn = self.ui.clearBtn
        self.searchBtn = self.ui.searchBtn
        self.selectBtn = self.ui.selectBtn

        self.viewTable = self.ui.tableWidget
        self.viewTable.setSortingEnabled(False)
        self.buttons_list = self.ui.function_frame.findChildren(QPushButton)

        self.init_single_slot()

    
    def init_single_slot(self):
        #connect buttons to their respective
        self.addBtn.clicked.connect(self.add_info)
        self.updateBtn.clicked.connect(self.update_info)
        self.searchBtn.clicked.connect(self.search_info)
        self.selectBtn.clicked.connect(self.select_info)
        self.clearBtn.clicked.connect(self.clear_form_info)
        self.deleteBtn.clicked.connect(self.delete_info)
        self.set_data_in_table()

    def search_info(self):
        # finction for search for student info and populate the table 
        
        student_info = self.get_student_info()
        
        student_reslut = self.db.search_info(
            student_id=student_info["student_id"],
            first_name=student_info["first_name"],
            last_name=student_info["last_name"],
            email_address=student_info["email_address"],
            state=student_info["state"],
            city=student_info["city"]
        )
        
        self.show_data(student_reslut)

    # def update_state_city(self):
    #     # function to populate the state and city dropdown

    #     state_result = self.db.get_all_states()
    #     city_result = self.db.get_all_cities()

    #     self.state.clear()
    #     self.city.clear()

    #     state_list = [""]
    #     for item in state_result:
    #         for k,v in item.items():
    #             if v != "":
    #                 state_list.append(v)
        
    #     city_list = [""]
    #     for item in city_result:
    #         for k,v in item.items():
    #             if v != "":
    #                 city_list.append(v)

    #     if len(state_list) > 1:
    #         self.state.addItems(state_list)
    #     if len(city_list) > 1:
    #         self.city.addItems(city_list)

    def add_info(self):
        self.disable_buttons()

        student_info = self.get_student_info()
        
        if student_info["student_id"] and student_info["first_name"]:
            print(student_info)
            check_result = self.check_student_id(student_id=int(student_info["student_id"]))

            if check_result:
                QMessageBox.information(self, "Error", "Student ID already exists! , Enter new Id", QMessageBox.StandardButton.Yes)
                self.enable_buttons()
                return
            
            add_result = self.db.add_info(
                student_id=int(student_info["student_id"]),
                first_name=student_info["first_name"],
                last_name=student_info["last_name"],
                email_address=student_info["email_address"],
                state=student_info["state"],
                city=student_info["city"],
                )
            QMessageBox.information(self, "Success", f"Student added Scussed", QMessageBox.StandardButton.Ok)
            self.enable_buttons()
            self.clear_form_info()
            self.set_data_in_table()
                
            if add_result:  
                QMessageBox.information(self, "Warning", f"Student added Failll : {add_result} try again", QMessageBox.StandardButton.Yes)
                self.enable_buttons()
                return
        else:
            QMessageBox.information(self, "Error", "All fields are required!", QMessageBox.StandardButton.Yes)
            self.search_info()
            self.enable_buttons()
            return

    def update_info(self):
        # function to update information student 
        
        new_student_info = self.get_student_info()
        
        if new_student_info["student_id"]:
            update_result = self.db.update_info(
                student_id=int(new_student_info["student_id"]),
                first_name=new_student_info["first_name"],
                last_name=new_student_info["last_name"],
                email_address=new_student_info["email_address"],
                state=new_student_info["state"],
                city=new_student_info["city"],
            )
            
            if update_result:
                QMessageBox.information(self, "Warning", f"Student updated Failll : {update_result} try again", QMessageBox.StandardButton.Yes)
            else:
                self.search_info()
                
        else:
            QMessageBox.information(self, "Error", "Student Not selected !", QMessageBox.StandardButton.Yes)


    def clear_form_info(self):
       # function for clearing the form
       self.student_id.clear()
       self.student_id.setEnabled(True)
       self.first_name.clear()
       self.last_name.clear()
       self.email_address.clear()
       self.state.setCurrentIndex(0)
       self.city.setCurrentIndex(0) 
    
    def set_data_in_table(self):
        result = self.db.loadData()
        self.viewTable.setRowCount(len(result))
        tablerow = 0
        for row in result:
            self.viewTable.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(row["studentId"])))
            self.viewTable.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row["firstName"]))
            self.viewTable.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row["lastName"]))
            self.viewTable.setItem(tablerow,3,QtWidgets.QTableWidgetItem(row["state"]))
            self.viewTable.setItem(tablerow,4,QtWidgets.QTableWidgetItem(row["city"]))
            self.viewTable.setItem(tablerow,5,QtWidgets.QTableWidgetItem(row["emailAddress"]))
         
            tablerow +=1
    def select_info(self):
        # function to select student and populate info in the form
        
        select_row = self.viewTable.currentRow()
        if select_row != -1:
            self.student_id.setEnabled(False)
            student_id = self.viewTable.item(select_row,0).text().strip()
            first_name = self.viewTable.item(select_row,1).text().strip()
            last_name = self.viewTable.item(select_row,2).text().strip()
            email_address = self.viewTable.item(select_row,5).text().strip()
            state = self.viewTable.item(select_row,4).text().strip()
            city = self.viewTable.item(select_row,3).text().strip()
            
            
            self.student_id.setText(student_id)
            self.first_name.setText(first_name)
            self.last_name.setText(last_name)
            self.email_address.setText(email_address)
            self.state.setCurrentText(state)
            self.city.setCurrentText(city)
            
            
        else:
            QMessageBox.information(self, "Error", "Select a student from table!", QMessageBox.StandardButton.Yes)
    
    def delete_info(self):
        # function for delete student information from table
        
        select_row = self.viewTable.currentRow()
        if select_row!= -1:
            select_option = QMessageBox.warning(self, "Warning", "Are you sure to delete it?", 
                                    QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            
            if select_option == QMessageBox.StandardButton.Ok:
                student_id = self.viewTable.item(select_row,0).text().strip()
                print(f" id = {student_id}")
                delete_result = self.db.delete_info(student_id=student_id)
                
                if not delete_result:
                    self.set_data_in_table()
                else:
                    QMessageBox.information(self, "Warning", f"Student deleted Failll : {delete_result} try again", QMessageBox.StandardButton.Yes)
                
        else:
            QMessageBox.information(self, "Error", "Select a student from table!", QMessageBox.StandardButton.Yes)

    def disable_buttons(self):
        for button in self.buttons_list:
            button.setDisabled(True)

    def enable_buttons(self):
        for button in self.buttons_list:
            button.setDisabled(False)

    def get_student_info(self):
        # function to retrive student information from the form
        student_id = self.student_id.text().strip()
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        email_address = self.email_address.text().strip()
        state = self.state.currentText()
        city = self.city.currentText()

        student_info = {
            "student_id": student_id,
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "state": state,
            "city": city,
        }
        return student_info

    def check_student_id(self, student_id):
        # function to check if a student id already exists
        result = self.db.search_info(student_id=student_id)
        print(result)
        return result
    
    
    def show_data(self, student_reslut):
        # Clear the table first
        self.viewTable.setRowCount(0)

        if student_reslut:
            self.viewTable.setRowCount(len(student_reslut))  # Set the number of rows
            for row, info in enumerate(student_reslut):
                # If info is a tuple (e.g., returned by MySQL or SQLite)
                # Convert tuple elements to strings
                info_list = [
                    str(info["studentId"]),  # student_id
                    info["firstName"],       # first_name
                    info["lastName"],       # last_name
                    info["emailAddress"],       # email_address
                    info["state"],       # state
                    info["city"],       # city
                ]

                # Populate each cell in the row
                for col, item in enumerate(info_list):
                    call_item = QTableWidgetItem(str(item))
                    self.viewTable.setItem(row, col, call_item)
        else:
            QMessageBox.information(self, "Not Found", "Student ID not exists!", QMessageBox.StandardButton.Yes)
            self.set_data_in_table()

# Application Entry
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
