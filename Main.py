import mysql.connector as M

# Connect to MySQL
def connect_db():
    return M.connect(user="root", password="f1racerford", host="localhost")

# Fetch Movies from Database
def get_movies():
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    C.execute("SELECT * FROM Movies")
    movies = C.fetchall()
    con.close()
    return movies

# Fetch Screens from Database
def get_screens():
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    C.execute("SELECT * FROM Screens")
    screens = C.fetchall()
    con.close()
    return screens

# Fetch Seats from Database
def get_seats(screen_number):
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    C.execute("SELECT Morning, Noon, Night FROM Tickets WHERE Screen = %s", (screen_number,))
    seats = C.fetchone()
    con.close()
    return seats

# Book Seats in Database
def book_seats(screen_number, seats_to_book, movie_code, show_time):
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    for seat in seats_to_book:
        C.execute("UPDATE Tickets SET %s = %s WHERE Screen = %s AND %s IS NULL", 
                  (show_time, seat, screen_number, show_time))
    C.execute("INSERT INTO Bookings (MovieCode, Screen, ShowTime, Seats) VALUES (%s, %s, %s, %s)", 
              (movie_code, screen_number, show_time, ','.join(seats_to_book)))
    con.commit()
    con.close()

# Update Ticket in Database
def update_ticket(ticket_id, new_seats):
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    C.execute("SELECT Seats FROM Bookings WHERE TicketID = %s", (ticket_id,))
    old_seats = C.fetchone()[0].split(',')
    for seat in old_seats:
        C.execute("UPDATE Tickets SET Morning = NULL WHERE Morning = %s", (seat,))
    for seat in new_seats:
        C.execute("UPDATE Tickets SET Morning = %s WHERE Screen = %s AND Morning IS NULL", (seat, ticket_id))
    C.execute("UPDATE Bookings SET Seats = %s WHERE TicketID = %s", (','.join(new_seats), ticket_id))
    con.commit()
    con.close()

# Delete Ticket from Database
def delete_ticket(ticket_id):
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    C.execute("SELECT Seats, Screen FROM Bookings WHERE TicketID = %s", (ticket_id,))
    seats, screen = C.fetchone()
    for seat in seats.split(','):
        C.execute("UPDATE Tickets SET Morning = NULL WHERE Morning = %s AND Screen = %s", (seat, screen))
    C.execute("DELETE FROM Bookings WHERE TicketID = %s", (ticket_id,))
    con.commit()
    con.close()

# Display Seating
def display_seats(seats, screen_number, show_time, movie_name):
    print(f"\nScreen {screen_number} - {show_time} - Movie: {movie_name}")
    print(f"Available seats:")
    for row in range(4):
        print(" ".join(seats[row * 10:(row + 1) * 10]))
    print("____________________\n")

# View Ticket
def view_ticket(ticket_id):
    con = connect_db()
    C = con.cursor()
    C.execute("USE THEATRE")
    C.execute("SELECT MovieCode, Screen, ShowTime, Seats FROM Bookings WHERE TicketID = %s", (ticket_id,))
    ticket = C.fetchone()
    if ticket:
        movie_code, screen, show_time, seats = ticket
        seats_list = seats.split(',')
        movie_name = [m[1] for m in get_movies() if m[0] == movie_code][0]
        display_seats(get_seats(screen), screen, show_time, movie_name)
        print(f"Your ticket details:\nMovie: {movie_name}\nScreen: {screen}\nShow Time: {show_time}\nSeats: {', '.join(seats_list)}")
    else:
        print("Ticket ID not found.")
    con.close()

# Main Menu
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Book Ticket")
        print("2. Update Ticket")
        print("3. Delete Ticket")
        print("4. View Ticket")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            book_ticket()
        elif choice == '2':
            update_ticket()
        elif choice == '3':
            delete_ticket()
        elif choice == '4':
            view_ticket()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

        continue_choice = input("Do you want to continue with the application? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print("Exiting...")
            break

def book_ticket():
    # Get and display available movies
    movies = get_movies()
    print("Available Movies:")
    for movie in movies:
        print(f"Code: {movie[0]}, Name: {movie[1]}")
    
    # User selects a movie
    movie_code = int(input("Enter the code of the movie you want to watch: "))
    movie_name = None
    for movie in movies:
        if movie[0] == movie_code:
            movie_name = movie[1]
            break
    
    if not movie_name:
        print("Invalid movie code.")
        return
    
    # Get and display available screens
    screens = get_screens()
    print("Available Screens:")
    for screen in screens:
        print(f"Screen Number: {screen[0]}")
    
    # User selects a screen
    screen_number = int(input("Enter the screen number you want to use: "))
    if screen_number not in [s[0] for s in screens]:
        print("Invalid screen number.")
        return
    
    # User selects a show time
    show_time = input("Enter show time (Morning, Noon, Night): ").strip().capitalize()
    if show_time not in ["Morning", "Noon", "Night"]:
        print("Invalid show time.")
        return
    
    # Fetch seat availability
    seats = get_seats(screen_number)
    if not seats:
        print("No seat information available for this screen.")
        return
    
    SEATS = ['D10', 'D09', 'D08', 'D07', 'D06', 'D05', 'D04', 'D03', 'D02', 'D01',
             'C10', 'C09', 'C08', 'C07', 'C06', 'C05', 'C04', 'C03', 'C02', 'C01',
             'B10', 'B09', 'B08', 'B07', 'B06', 'B05', 'B04', 'B03', 'B02', 'B01',
             'A10', 'A09', 'A08', 'A07', 'A06', 'A05', 'A04', 'A03', 'A02', 'A01']
    
    seat_status = [' ' if seat is None else 'X' for seat in seats]
    SEATS[:len(seat_status)] = seat_status
    
    # Display seats
    display_seats(SEATS, screen_number, show_time, movie_name)
    
    # User selects number of seats
    num_seats = int(input("How many seats do you want to book? "))
    available_seats = [seat for seat in SEATS if seat.strip() != 'X']
    
    if num_seats > len(available_seats):
        print("Not enough available seats.")
        return
    
    # Book selected seats
    selected_seats = []
    for _ in range(num_seats):
        seat = input("Enter the seat you want to book (e.g., D10): ").strip()
        if seat in available_seats:
            selected_seats.append(seat)
            available_seats.remove(seat)
        else:
            print(f"Seat {seat} is not available. Try again.")
            return
    
    book_seats(screen_number, selected_seats, movie_code, show_time)
    print("Booking successful!")

def update_ticket():
    ticket_id = int(input("Enter the ticket ID to update: "))
    new_seats = input("Enter the new seats, separated by commas: ").split(',')
    new_seats = [seat.strip() for seat in new_seats]
    
    update_ticket(ticket_id, new_seats)
    print("Ticket updated successfully!")

def delete_ticket():
    ticket_id = int(input("Enter the ticket ID to delete: "))
    delete_ticket(ticket_id)
    print("Ticket deleted successfully!")

if __name__ == "__main__":
    main_menu()
