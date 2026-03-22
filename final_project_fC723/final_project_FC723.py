from random import randint 
import random
import string

existing_references = []

def generate_reference():
    while True:
        refrence = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if refrence not in existing_references:
            existing_references.append(refrence)
            return refrence

class Customer:
    test_user = {"name": "test", "email": "test@gmail.com", "password": "testing", "status": "passive"}
    existing_users = {}
    existing_ids = []

    def __init__(self, name, email, password, status = "passive"):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.id = self._generate_unique_id()
        self.bookings = {}

    def _generate_unique_id(self):
        while True:
            new_id = randint(100000000, 999999999)
            if new_id not in Customer.existing_ids:
                Customer.existing_ids.append(new_id)
                return new_id
            
    def launch (self):
        while True:
            start = input("welcome to ... airline, are you registered with us (yes/no)").strip().lower()
            if start == "yes":
                self.login()
                break

            elif start == "no":
                self.sign_up()
                break
            else:
                print("error, try agian")

    def sign_up(self):
        new_name = ((input("what is your first name").strip())+" "+input("what is your last name").strip())
        new_email = (input("what is your email username")+"@"+input("what is your email service provider")+".com").strip()
        new_password = input("password:").strip()
        session = Customer(new_name, new_email, new_password, "active")
        Customer.existing_users[new_email] = session
        global app
        app = session
        flight.menu()

    def logout(self):
        self.status = "passive"
        print("Logged out successfully.")
        app.launch()


    def login(self):
        while True: 
            old_email = input("email: ").strip()
            old_password = input("password: ").strip()
            if self.test_user["email"] == old_email and self.test_user["password"] == old_password:
                session = Customer(self.test_user["name"], old_email, old_password, "active")
                global app
                app = session
                flight.menu()
                break
            else:
                print("incorrect email or password, try again")

    def __repr__(self):
        return f"Customer({self.name}, ID: {self.id})"


class Seat :
    def __init__(self, sit_number, seat_type = "F"):
        self.status = seat_type
        self.sit_number = sit_number
        self.sit_user =  None

    def check_seat(self): #just to check if its available, not also reserve it 
        if self.status == "F":
            return "F"
        elif self.status == "R":
            return "R"
        elif self.status == "S":
            return "S"
        elif self.status == "X":
            return "X"

    def reserve(self, user, refrence):
        self.status = "R"
        self.sit_user = user
        self.refrence = refrence

    def __repr__(self):
        return self.sit_number +":"+ self.status 

class Plane:   
    def __init__(self, destination, time):
        self.seats = [] #list of lists, where each sublist is a row of the plane
        self. destination = destination
        self.time = time
        self.seat_rows = ["A","B","C","X","D","E","F"]
        self.create_seats()

    def create_seats(self):
        #create storage seats
        #fills in self.seats with all rows of plane
        for row in range(1,81):
            row_list=[]
            row_list_id = []
            storage_column = range(77, 80)  # 77, 78, 79
            storage_rows = ["D", "E", "F"]
            for unique_seat in self.seat_rows:
                if unique_seat == "X" or unique_seat == "S":
                    seat=Seat(f"{row}{unique_seat}", "X")
                elif unique_seat in storage_rows and row in storage_column:
                    seat = Seat(f"{row}{unique_seat}", "S")
                else:
                    seat=Seat(f"{row}{unique_seat}") #instances of the seat class with given sit_number
                    #print(seat.sit_number)
                row_list.append(seat)
                row_list_id.append(seat.sit_number)
            self.seats.append(row_list)
    
    def find_seat(self, seat_label):
        for row in self.seats:
            for seat in row:
                if seat.sit_number == seat_label.upper():
                    return seat
        return None
    
    def check_availability(self):
        for row in self.seats:
            for seat in row:
                if seat.status == "F":
                    print(seat)

    def book(self):
        chance = 3
        while chance > 0:
            requested_seat = input("which seat will you like to book. e.g, 10C ").strip().upper()
            result_seat = self.find_seat(requested_seat)
            if result_seat == None:
                print("seat doesn't exist, try again")
                chance -= 1
            elif result_seat.check_seat() == "R": 
                print("seat is reserved, try again")
                chance -=1
            elif result_seat.check_seat() == "X" or result_seat.check_seat() == "S" : 
                print("seat is inassesible, try again")
                chance -=1
            elif result_seat.check_seat() == "F": #elif for F seat, another elif for storage seats
                free_seat = input("the seat you seek is currently free, would you like to proceed with booking(yes/no)").strip().lower()
                if free_seat == "yes":
                    passport = input("Enter your passport number: ").strip()
                    refrence = generate_reference()
                    result_seat.reserve(app, refrence)
                    print(f"{result_seat.sit_number} booked. Your reference is: {refrence}")
                    app.bookings[refrence] = result_seat
                elif free_seat == "no":
                    print("Booking cancelled.")
                break
        if chance == 0:
            print("too many attempts")

    def cancel(self):
        seat_label = input("Which seat to cancel? e.g. 10C: ").strip().upper()
        result_seat = self.find_seat(seat_label)
        if result_seat is None:
            print("Seat not found.")
        elif result_seat.status == "F":
            print("That seat isn't booked.")
        elif result_seat.sit_user != app:
            print("That seat belongs to someone else.")
        else:
            result_seat.status = "F"
            result_seat.sit_user = None
            result_seat.refrence = None
            print(f"{seat_label} cancelled successfully.")

    def display_seats(self):
        for row in self.seats:
            print(row)
    def check_for_seat(self):
        seat_name = input("Enter seat e.g. 10C: ").strip().upper()
        result = self.find_seat(seat_name)
        if result is None:
            print("Seat not found.")
        else:
            print(result)

    def menu (self):
        while True:
            request = input('''welcome to what would you like to do:
    book a seat(1), 
    cancel reservation(2), 
    display seats(3), 
    show only available seats(4), 
    check status of a specific seat(5), 
    logout(6),
    exit(7).
    type the title or number: ''').lower()
            if request == "book a seat" or request == "1":
                self.book()
            elif request == "cancel reservation" or request == "2":
                self.cancel()
            elif request == "display seats" or request == "3":
                self.display_seats()
            elif request == "show only available seats" or request == "4":
                self.check_availability()
            elif request == "check status of a specific seat" or request == "5":
                self.check_for_seat()
            elif request == "logout" or request == "6":
                app.logout()
                break
            elif request == "exit" or request == "7":
                app.status = "passive"
                break
            else:
                print("error, try again")

flight = Plane("New York", "14:00")
app = Customer("","","","passive")
app.launch()