import tkinter as tk
import mysql.connector as sql
from datetime import datetime
import pyfiglet

class ParkingManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Area Management System")
        self.canvas = tk.Canvas(root, bg='alice blue', width=1000, height=1000, relief='raised')
        self.canvas.pack()

        self.db = sql.connect(host='localhost', user='root', passwd="2003", database="pams", use_pure=True)
        self.cursor = self.db.cursor()

        self.create_table()
        self.last_assigned_slot = self.get_last_slot()

        self.display_welcome()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS CARS (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            NAME CHAR(30),
            PASSWORD CHAR(20),
            CARDETAILS CHAR(30),
            COLOUR CHAR(20),
            SLOT INT(20),
            ARRIVALTIME DATETIME,
            DEPARTURETIME DATETIME,
            TIMEDIFFERENCE CHAR(30),
            BILL CHAR(30)
        );
        """)
        self.db.commit()

    def get_last_slot(self):
        self.cursor.execute("SELECT MAX(SLOT) FROM CARS")
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def display_welcome(self):
        self.canvas.delete("all")
        welcome_text = pyfiglet.figlet_format("PAMS", font="big")
        self.canvas.create_text(500, 100, text=welcome_text, font=('Courier', 14))
        
        self.canvas.create_text(500, 200, text="PARKING AREA MANAGEMENT SYSTEM", font=('Helvetica', 24, 'bold'))
        self.canvas.create_text(500, 250, text="1. Enter Parking Lot", font=('Helvetica', 14))
        self.canvas.create_text(500, 280, text="2. Exit Parking Lot", font=('Helvetica', 14))

        self.choice_entry = tk.Entry(self.root)
        self.canvas.create_window(500, 320, window=self.choice_entry)

        enter_button = tk.Button(self.root, text="Submit", command=self.process_choice, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.canvas.create_window(500, 360, window=enter_button)

    def process_choice(self):
        choice = self.choice_entry.get()
        if choice == '1':
            self.enter_parking()
        elif choice == '2':
            self.exit_parking()
        else:
            self.show_error("Invalid choice. Please enter 1 or 2.")

    def enter_parking(self):
        self.canvas.delete("all")
        self.canvas.create_text(500, 60, text="ENTER YOUR DETAILS", font=('Helvetica', 18, 'bold'))

        fields = [("Name:", 100), ("Password:", 150), ("Car Details:", 200), ("Car Colour:", 250)]
        self.entries = {}

        for (field, y) in fields:
            self.canvas.create_text(400, y, text=field, font=('Helvetica', 14))
            entry = tk.Entry(self.root)
            self.canvas.create_window(515, y, window=entry)
            self.entries[field] = entry

        enter_button = tk.Button(self.root, text="Park Car", command=self.park_car, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.canvas.create_window(515, 300, window=enter_button)

    def park_car(self):
        self.last_assigned_slot += 1
        name = self.entries["Name:"].get()
        password = self.entries["Password:"].get()
        car_details = self.entries["Car Details:"].get()
        car_colour = self.entries["Car Colour:"].get()
        arrival_time = datetime.now()

        self.cursor.execute("""
        INSERT INTO CARS (NAME, PASSWORD, CARDETAILS, COLOUR, SLOT, ARRIVALTIME)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, password, car_details, car_colour, self.last_assigned_slot, arrival_time))
        self.db.commit()

        self.show_parking_info(self.last_assigned_slot)

    def show_parking_info(self, slot):
        self.canvas.delete("all")
        self.canvas.create_text(500, 100, text=f"Your assigned parking slot is: {slot}", font=('Helvetica', 18, 'bold'))
        self.canvas.create_text(500, 150, text="Please remember your slot number!", font=('Helvetica', 14))
        
        back_button = tk.Button(self.root, text="Back to Main Menu", command=self.display_welcome, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.canvas.create_window(500, 200, window=back_button)

    def exit_parking(self):
        self.canvas.delete("all")
        self.canvas.create_text(500, 60, text="EXIT PARKING", font=('Helvetica', 18, 'bold'))

        self.canvas.create_text(400, 120, text="Password:", font=('Helvetica', 14))
        self.password_entry = tk.Entry(self.root)
        self.canvas.create_window(515, 120, window=self.password_entry)

        self.canvas.create_text(400, 170, text="Car Details:", font=('Helvetica', 14))
        self.car_details_entry = tk.Entry(self.root)
        self.canvas.create_window(515, 170, window=self.car_details_entry)

        exit_button = tk.Button(self.root, text="Exit Parking", command=self.process_exit, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.canvas.create_window(515, 220, window=exit_button)

    def process_exit(self):
        password = self.password_entry.get()
        car_details = self.car_details_entry.get()

        self.cursor.execute("""
        SELECT * FROM CARS 
        WHERE PASSWORD = %s AND CARDETAILS = %s AND DEPARTURETIME IS NULL
        """, (password, car_details))
        
        car = self.cursor.fetchone()
        if car:
            self.show_bill(car)
        else:
            self.show_error("Car not found or already exited. Please check your details.")

    def show_bill(self, car):
        departure_time = datetime.now()
        duration = departure_time - car[6]  # car[6] is ARRIVALTIME
        minutes = duration.total_seconds() / 60

        bill = self.calculate_bill(minutes)

        self.cursor.execute("""
        UPDATE CARS 
        SET DEPARTURETIME = %s, TIMEDIFFERENCE = %s, BILL = %s 
        WHERE ID = %s
        """, (departure_time, str(duration), str(bill), car[0]))
        self.db.commit()

        self.canvas.delete("all")
        self.canvas.create_text(500, 60, text="PARKING BILL", font=('Helvetica', 18, 'bold'))
        self.canvas.create_text(500, 100, text=f"Name: {car[1]}", font=('Helvetica', 14))
        self.canvas.create_text(500, 130, text=f"Car Details: {car[3]}", font=('Helvetica', 14))
        self.canvas.create_text(500, 160, text=f"Slot: {car[5]}", font=('Helvetica', 14))
        self.canvas.create_text(500, 190, text=f"Duration: {duration}", font=('Helvetica', 14))
        self.canvas.create_text(500, 220, text=f"Total Bill: ₹{bill}", font=('Helvetica', 14, 'bold'))

        back_button = tk.Button(self.root, text="Back to Main Menu", command=self.display_welcome, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.canvas.create_window(500, 260, window=back_button)

    def calculate_bill(self, minutes):
        if minutes < 60:
            return 15
        elif minutes < 180:
            return 20
        elif minutes < 360:
            return 30
        elif minutes < 720:
            return 55
        else:
            return 65

    def show_error(self, message):
        self.canvas.delete("all")
        self.canvas.create_text(500, 100, text="Error", font=('Helvetica', 18, 'bold'))
        self.canvas.create_text(500, 150, text=message, font=('Helvetica', 14))
        
        back_button = tk.Button(self.root, text="Back to Main Menu", command=self.display_welcome, bg='brown', fg='white', font=('Helvetica', 9, 'bold'))
        self.canvas.create_window(500, 200, window=back_button)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingManagementSystem(root)
    root.mainloop()

