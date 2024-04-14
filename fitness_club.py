import psycopg2
from datetime import date

# Function to establish connection to PostgreSQL
def connect_to_postgresql():
    try:
        # PostgreSQL connection configuration
        global conn
        conn = psycopg2.connect(
            dbname='project',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        print('Connected to PostgreSQL database\n')
        return conn
    except psycopg2.Error as e:
        print('Error connecting to PostgreSQL database:', e)
        return None

# Bad design but for the purposes of testing atm I will call the function here 

# Main page login
def main_hub():
    pass

#--------------------- User/ Member functions ----------------------

#adds account and iits password before registering

""" DONE """
def add_account(new_mem_eid , conf_pass):
    try: 
        curr= conn.cursor()
        curr.execute("INSERT INTO members (email_id , password) VALUES ( %s , %s)",(new_mem_eid , conf_pass))
        conn.commit()
        curr.close()
        
    except psycopg2.Error as e:
        conn.rollback()
        print("Error adding account:", e)
        return False
    

#  --- Member registration ---
#  This function should just full register the member fully

""" DONE """
def member_registration(email_id):
    #This populates the whole member table
    
    #This stage should take you to the payment function as well
    print("\n PERSONAL  INFO ")
    f_name=input("\nWhat is your first name ? ")
    l_name=input("\nWhat is your last name ? ")
    dob= input("\nWhat is your date of birth  (YYYY-MM-DD)? ")
    address =input("\nAddress:")
    phone_no= input ("\nPhone Number (XXX-XXX-XXXX):")
    print("\n\n  HEALTH METRICS")
    weight= input ("Weight in pounds : ")
    height = input ("Height in inches : ")
    
    # Payment for membership plan has to get approved so call payment function
    
    print("\nYou will now be redirected to payment by one of our admin staff")
    
    # //might delete this section later due to project requirements
    if billing():
        
        # Run query for adding the member record only after the payment function returns true.
        
        # Open a cursor to perform database operations
        cur = conn.cursor()

        cur.execute("INSERT INTO personal_info (email_id , first_name, last_name, date_of_birth, address, phone_number, weight, height) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (email_id, f_name, l_name, dob, address, phone_no, weight, height))
        conn.commit()
        cur.close()
        
        # Setup error checking to see if the member record was created then print success message
        
        #Using returning clause as the factor in deciding 
        print("\nYou're are all set up , You will be redirected to the main page !")
        
    # User added by admin staff based on the transaction number
    
    else:
        print("\nHead to our admin staff desk to finalize your registration")
        return  # Return to main menu

# This function cross checks users email with their password
# from here is where the chain block of events happen (Will need to fix this in the future)

""" DONE """
def verify_member_login():
    #This function should just call the member check up function or sth of the sort
    ver_stat=False
    print("\nWELCOME TO THE MEMBER LOGIN PAGE")
    
    while not ver_stat:
        member_email=input("\nPlease enter your member email inorder to proceed: ")
        mem_password= input("\n\nPlease enter your password: ")

        # Query to cross check password for this email from the members database
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM members WHERE email_id = %s AND password = %s", (member_email, mem_password))

            result = cur.fetchone()[0]
            print(result)
            if(result==1):
                mem_dashboard_dis(member_email)
                ver_stat=True
            else:
                print("\nPassword was incorrect or email does not exist , \nPlease try again\n")
    
        except psycopg2.Error as e:
        
            print("Error adding session:", e)
            return False
            

# Member uses this to change their details using their email as the lookup id , email should come from previous function


""" DONE """
def profile_management(mem_id):
    #First display member details
    cur = conn.cursor()
    cur.execute("SELECT * FROM personal_info WHERE email_id = %s", (mem_id,))
    
    
    member_details = cur.fetchone()
    print("Your current profile details:")
    print("First Name:", member_details[1])
    print("Last Name:", member_details[2])
    print("Date of Birth:", member_details[3])
    print("Address:", member_details[4])
    print("Phone Number:", member_details[5])
    print("Weight:", member_details[6])
    print("Height:", member_details[7])
    
    choice = input("\n What would you like to change regarding your profile\n1.)First_name\n2.)Last name\n.3) Date of Birth\n.4) Address\n.5) Phone Number\n.6) Weight\n.7) Height\n.8) Back to menu")
    
    
    if choice == "1":
        new_first_name = input("Enter new first name: ")
        cur.execute("UPDATE personal_info SET first_name = %s WHERE email_id = %s", (new_first_name, mem_id))
    elif choice == "2":
        new_last_name = input("Enter new last name: ")
        cur.execute("UPDATE personal_info SET last_name = %s WHERE email_id = %s", (new_last_name, mem_id))
    elif choice == "3":
        new_dob = input("Enter new date of birth (YYYY-MM-DD): ")
        cur.execute("UPDATE personal_info SET date_of_birth = %s WHERE email_id = %s", (new_dob, mem_id))
    elif choice == "4":
        new_address = input("Enter new address: ")
        cur.execute("UPDATE personal_info SET address = %s WHERE email_id = %s", (new_address, mem_id))
    elif choice == "5":
        new_phone_number = input("Enter new phone number: ")
        cur.execute("UPDATE personal_info SET phone_number = %s WHERE email_id = %s", (new_phone_number, mem_id))
    elif choice == "6":
        new_weight = input("Enter new weight (in pounds): ")
        cur.execute("UPDATE personal_info SET weight = %s WHERE email_id = %s", (new_weight, mem_id))
    elif choice == "7":
        new_height = input("Enter new height (in cm): ")
        cur.execute("UPDATE personal_info SET height = %s WHERE email_id = %s", (new_height, mem_id))
    elif choice == "8":
        return  # Return to main menu
    else:
        print("Invalid choice")

    conn.commit()
    print("Profile updated successfully")
     
    
    cur.close()


 


""" DONE """
#Should also contain the functions that members can do such as schedule or enroll for a class. also show te scheuled classes for the day.Enroll for a class , schedule a session with a trainer.

def mem_dashboard_dis(mem_id):
    # Prints for the statements on the details obtained from the member table
    run=True
    while( run):
        # Retrieve personal information
        curr= conn.cursor()
        curr.execute("SELECT * FROM personal_info WHERE email_id = %s ;", (mem_id,))
        result = curr.fetchall()
        
        print("\n\nYOUR PERSONAL INFO:\n\n ")
        for i in result:
            print(i)
        #Access details from the result records and just print them
        
        
        # Retrieve fitness goals
        curr.execute("SELECT * FROM fitness_goals WHERE email_id = %s;", (mem_id,))
        fitness_goals = curr.fetchall()
        
        print("\n\nYOUR FITNESS GOALS:\n\n")
        for goal in fitness_goals:
            print(goal)
        
        
        #Retrieve scheduled times
        curr.execute("SELECT * FROM main_schedule WHERE email_id = %s;", (mem_id,))
        scheduled_times = curr.fetchall()
        
        print("\n\nYOUR SCHEDULED TIMES:\n\n")
        for time in scheduled_times:
            print(time)
        
        #Retrive classes in which the member has signed up for
        #Retrieve scheduled times
        curr.execute("SELECT * FROM member_class_booking WHERE member_email = %s;", (mem_id,))
        classes = curr.fetchall()
        
        print("\n\nYOUR CLASSES:\n\n")
        for darasa in classes:
            print(darasa)
        
        
        print("\nWhat would you like to do today?")
        print("1.) Add a session")
        print("2.) Cancel a session")
        print("3.) Change something on your profile")
        print("4.) Add some fitness goals")
        print("5.) Logout")
        print("6.) Book a class")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_session(mem_id)
        elif choice == "2":
            cancel_session(mem_id)
        elif choice == "3":
            profile_management(mem_id)
        elif choice == "4" :
            add_fitgoals(mem_id)
        elif choice == "5" :
            print(" \n Have a great day !")
            run=False
            return  # Return to main menu
        elif choice == "6" :
            book_class(mem_id)
        else:
            print("Invalid choice")
        
        
        
    curr.close()



# To be used by both the user side and server side
# Used to print the main schedule

"""" DONE """
def schedule_management(email_id):
   
    # So it uses the member email_id to filter out the schedule to return only classes by the member.
    print("\nThis is your current schedule : ")
    
    # Fetch sessions scheduled for the member with the given email_id
    cur = conn.cursor()
    cur.execute("SELECT * FROM main_schedule WHERE email_id = %s", (email_id,))
    sessions = cur.fetchall()
    
    print(sessions)
    
    print("\nOptions: \n1.)Add a session \n2.)Cancel a session \n3.)Back ")
    
    choice = input("\nEnter your choice: ")
    
    if choice == "1":
        # Add a new session for the member
        add_session(email_id)
    elif choice == "2":
        # Cancel a session
        cancel_session(email_id)
    elif choice == "3":
        # Go back to the previous menu
        print("Back to main menu")
        pass
    else:
        print("Invalid choice")
    
    #If choices for options , Add for session by asking for details needed , cancel session by asking for id of session and back goes back to previous session

""" DONE """
def display_available_trainers_and_rooms():
    try:
        cur = conn.cursor()
        
        # Query to retrieve available trainers and their times
        cur.execute("""
        SELECT t.trainer_id, t.first_name, t.last_name, ts.time_slot 
        FROM trainers_schedule ts JOIN trainers t ON ts.trainer_id = t.trainer_id
        WHERE ts.availability = 'available';""")
        trainers = cur.fetchall()

        print("\nTRAINERS AVAILABLE:")
        for trainer in trainers:
            print(f"{trainer[0]} - {trainer[1]} {trainer[2]} - Available at: {trainer[3]}")
        
        
         # Query to retrieve available rooms
        cur.execute("""
        SELECT r.room_id, r.room_name, rs.time_slot
        FROM rooms_schedule rs
        JOIN rooms r ON rs.room_id = r.room_id
        WHERE rs.status = 'available';""")
        rooms = cur.fetchall()
        
        print("\nROOMS AVAILABLE:")
        for room in rooms:
            print(f"Room {room[0]} - {room[1]} - Available at: {room[2]}")
        
        cur.close()
    except psycopg2.Error as e:
        print("Error displaying available trainers and rooms:", e)




"""" DONE """
def add_session(email_id):
    # Setup cursor
    
    cur = conn.cursor()
    
    #First of all display available trainers and their times available along with rooms available as well to facilitate user ease to setup a schedule
    
    display_available_trainers_and_rooms()
    
    
    # Get input for the session details (trainer_id, room_id, time_slot, etc.)
    trainer_id = input("Enter the trainer ID: ")
    room_id = input("Enter the room ID: ")
    time_slot = input("Enter the time slot: ")
    
    
    # Check if a trainer is available at the specified time slot
    cur.execute("SELECT * FROM trainers_schedule WHERE trainer_id = %s AND time_slot = %s AND availability = 'available'", (trainer_id, time_slot))
    available_trainer = cur.fetchone()
    if not available_trainer:
        print("Selected trainer is not available at the specified time slot.")
        return False
    
    # Check if the room is available at the specified time slot
    cur.execute("SELECT * FROM main_schedule WHERE room_id = %s AND time_slot = %s", (room_id, time_slot))
    booked_room = cur.fetchone()
    if booked_room:
        print("Selected room is already booked at the specified time slot.")
        return False
    
 
    try:
        # Insert the session into the main_schedule table
        cur.execute("INSERT INTO main_schedule (email_id, trainer_id, room_id, time_slot) VALUES (%s, %s, %s, %s)", (email_id, trainer_id, room_id, time_slot))
        
        # Update trainers_schedule table
        cur.execute("UPDATE trainers_schedule SET availability = 'booked' WHERE trainer_id = %s AND time_slot = %s", (trainer_id, time_slot))
        
        # Update rooms_schedule table
        cur.execute("UPDATE rooms_schedule SET status = 'booked' WHERE room_id = %s AND time_slot = %s", (room_id, time_slot))
        
        cur.execute
        conn.commit()
        print("Session added successfully.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print("Error adding session:", e)
        return False

"""" DONE """
def cancel_session(email_id):
    try:
        booking_id = input("\nEnter the booking ID number of the session you wish to cancel: ")
        
        # Check if the session exists and belongs to the specified email_id
        cur = conn.cursor()
        cur.execute("SELECT * FROM main_schedule WHERE booking_id = %s AND email_id = %s", (booking_id, email_id))
        session = cur.fetchone()
        if not session:
            print("Session with the specified booking ID does not exist or does not belong to you.")
            return False
        
        # If the session exists and belongs to the specified email_id, UPDATE ROOM AND TRAINER SCHEDULES THEN DELETE FROM MAIN SCHEDULE 
        
        """ UPDATING THE ROOM SCHEDULE ACCORDINGLY """
        
        # Retrieve session details including room_id and time_slot
        cur.execute("SELECT room_id, time_slot FROM main_schedule WHERE booking_id = %s AND email_id = %s", (booking_id, email_id))
        session = cur.fetchone()
        if not session:
            print("Session with the specified booking ID does not exist or does not belong to you.")
            return False
        
        # Extract room_id and time_slot from the session
        room_id, time_slot = session
        
        # Update rooms_schedule table to mark the room as available for the cancelled session's time_slot
        cur.execute("UPDATE rooms_schedule SET status = 'available' WHERE room_id = %s AND time_slot = %s", (room_id, time_slot))
        
        """ UPDATING THE TRAINERS SCHEDULE ACCORDINGLY """
        
        # Retrieve session details including trainer_id and time_slot
        cur.execute("SELECT trainer_id, time_slot FROM main_schedule WHERE booking_id = %s AND email_id = %s", (booking_id, email_id))
        session = cur.fetchone()
        if not session:
            print("Session with the specified booking ID does not exist or does not belong to you.")
            return False
        
        # Extract trainer_id and time_slot from the session
        trainer_id, time_slot = session
        
        
        # Update trainers_schedule table to mark the trainer as available for the canceled session's time_slot
        cur.execute("UPDATE trainers_schedule SET availability = 'available' WHERE trainer_id = %s AND time_slot = %s", (trainer_id, time_slot))
        
        
        
        # DELETE BOOKING FROM THE MAIN SCHEDULE
        cur.execute("DELETE FROM main_schedule WHERE booking_id = %s", (booking_id,))
        
        
        conn.commit()
        print("Session canceled successfully.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print("Error canceling session:", e)
        return False

""" DONE """
def add_fitgoals(mem_id):
    try:
        goal_description = input("Enter your fitness goal: ")
        target_date = input("Enter the target date (YYYY-MM-DD): ")
        
        cur = conn.cursor()
        cur.execute("INSERT INTO fitness_goals (email_id, goal_description, target_date) VALUES (%s, %s, %s)", (mem_id, goal_description, target_date))
        conn.commit()
        cur.close()
        print("Fitness goal added successfully.")
        return True
    except psycopg2.Error as e:
        conn.rollback()
        print("Error adding fitness goal:", e)
        return False

def display_exrcise_routines(mem_id):
    
    pass

def book_class(mem_email):
    try:
        cur = conn.cursor()
        # Fetch available classes
        cur.execute("SELECT * FROM class_schedule WHERE availability = 'available';")
        available_classes = cur.fetchall()
        
        if not available_classes:
            print("No classes available for booking at the moment.")
            return False
        
        # Display available classes to the member
        print("Available Classes:")
        for c in available_classes:
            print(f"Class ID: {c[0]}, Class Name: {c[1]}, Time: {c[2]}")
        
        # Prompt member to choose a class to book
        class_id = input("Enter the ID of the class you want to book: ")
        
        # Check if the chosen class exists
        cur.execute("SELECT * FROM class_schedule WHERE class_id = %s AND availability = 'available';", (class_id,))
        chosen_class = cur.fetchone()
        if not chosen_class:
            print("Error: The selected class is not available for booking.")
            return False
        
        # Get the current date
        booking_date = date.today()
        
        # Book the class for the member
        cur.execute("INSERT INTO member_class_booking (member_email, class_id, booking_date) VALUES (%s, %s, %s);", (mem_email, class_id, booking_date))
        conn.commit()
        print("Class successfully booked.")
        return True
    
    except psycopg2.Error as e:
        conn.rollback()
        print("Error booking class:", e)
        return False

# Trainer functions
"""" DONE """
def trainer_schedule_management(trainer_id):
    try:
        # Display the trainer's current schedule
        print("\nThis is your current schedule:")
        
        # Fetch the trainer's schedule from the database
        cur = conn.cursor()
        cur.execute("SELECT * FROM trainers_schedule WHERE trainer_id = %s", (trainer_id,))
        schedule = cur.fetchall()
        
        # Check if the trainer has any schedule
        if not schedule:
            print("You don't have any scheduled sessions at the moment.")
            return False
        
        # Print the schedule
        for session in schedule:
            print(f"Session ID: {session[0]}, Time Slot: {session[2]}, Availability: {session[3]}")
        
        # Ask the trainer if they want to change availability
        session_id = input("\nTo change availability, enter the ID of the session you want to modify, or press Enter to go back: ")
        
        if session_id:
            new_availability = input("Enter new availability (booked/available/unavailable): ")
            
            # Update the availability of the session in the database
            cur.execute("UPDATE trainers_schedule SET availability = %s WHERE schedule_id = %s", (new_availability, session_id))
            conn.commit()
            
        print("Your schedule has been successfully updated!")
        return True
    
    except psycopg2.Error as e:
        conn.rollback()
        print("Error displaying trainer's schedule:", e)
        return False
    
# Dashboard for trainers 
""" DONE """
def trainer_dashboard(trainer_id):
    try:
        cur = conn.cursor()
        
        # Retrieve trainer's schedule
        cur.execute("SELECT * FROM trainers_schedule WHERE trainer_id = %s", (trainer_id,))
        schedule = cur.fetchall()
        
        print("TRAINER'S SCHEDULE:")
        for slot in schedule:
            print(f"Time Slot: {slot[2]} - Availability: {slot[3]}")
        
        # Give options to manage schedule or search for a member
        choice='0'
        while choice!='3':
            print("\nOptions:")
            print("1. Manage Schedule")
            print("2. Search Member")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")
            if choice == '1':
                trainer_schedule_management(trainer_id)
                
            elif choice == '2':
                view_member_detail()
            elif choice == '3':
                return True
            else:
                print("Invalid choice. Please select a valid option.")
                
        
    except psycopg2.Error as e:
        print("Error accessing trainer dashboard:", e)
        return False


""" DONE """
def verify_trainer_login():
    
    ver_stat=False
    print("\nWELCOME TO THE TRAINER LOGIN PAGE")
    
    while not ver_stat:
        trainer_id=input("\nPlease enter your trainer id inorder to proceed: ")
        tra_password= input("\n\nPlease enter your password: ")

        # Query to cross check password for this email from the members database
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM trainers WHERE trainer_id = %s AND password = %s", (trainer_id, tra_password))

            result = cur.fetchone()[0]
            print(result)
            if(result==1):
                ver_stat=True
                trainer_dashboard(trainer_id)
                
            else:
                print("\nPassword was incorrect or email does not exist , \nPlease try again\n")
    
        except psycopg2.Error as e:
        
            print("Error adding session:", e)
            return False
            
""" DONE """
# Capable of searching member by name
def view_member_detail():
    m_fname= input("\nTo search for a member\nPlease enter the members first name ")
    m_lname= input("\nPlease enter the members last name ")
    
    try:
        # Execute query to find the member by first name and last name
        cur = conn.cursor()
        cur.execute("SELECT * FROM personal_info WHERE first_name = %s AND last_name = %s", (m_fname, m_lname))
        member_info = cur.fetchall()

        if not member_info:
            print("No member found with the given name.")
        else:
            print("\nMember Details:")
            for member in member_info:
                print(f"First Name: {member[1]}")
                print(f"Last Name: {member[2]}")
                print(f"Phone Number: {member[5]}")
                print(f"Weight: {member[6]} pounds")
                print(f"Height: {member[7]} inches")

    except psycopg2.Error as e:
        print("Error retrieving member details:", e)
        return False
    
    
""" DONE """
# Admin staff functions

def verify_admin_login():
    ver_stat=False
    print("\nWELCOME TO THE ADMIN LOGIN PAGE")
    
    while not ver_stat:
        admin_id=input("\nPlease enter your admin id inorder to proceed: ")
        adm_password= input("\n\nPlease enter your password: ")

        # Query to cross check password for this email from the members database
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM admin_staff WHERE staff_id = %s AND password = %s", (admin_id, adm_password))

            result = cur.fetchone()[0]
            print(result)
            if(result==1):
                ver_stat=True
                admin_dashboard()
                
            else:
                print("\nPassword was incorrect or email does not exist , \nPlease try again\n")
    
        except psycopg2.Error as e:
        
            print("Error adding session:", e)
            return False

def admin_dashboard():
    try:
        while True:
            print("\nADMIN DASHBOARD")
            print("1. Room Booking Management")
            print("2. Equipment Maintenance")
            print("3. Class Schedule Management")
            print("4. Billing")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                room_booking_management()
            elif choice == '2':
                equipment_maintenance()
            elif choice == '3':
                class_schedule_updating()
            elif choice == '4':
                billing()
            elif choice == '5':
                print("Exiting admin dashboard.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    except psycopg2.Error as e:
        print("Error:", e)
        return False

def room_booking_management():
    
    try:
        # Retrieve and display all available rooms
        print("\nAvailable Rooms:")
        cur = conn.cursor()
        cur.execute("""
            SELECT rs.room_id, r.room_name , rs.time_slot
            FROM rooms_schedule rs
            JOIN rooms r ON rs.room_id = r.room_id
            WHERE rs.status = 'available';
        """)
        rooms = cur.fetchall()
        
        if not rooms:
            print("No rooms available for booking.")
            return False
        
        for room in rooms:
            print(f"Room ID: {room[0]}, Room Name: {room[1]} , Time Slot: {room[2]}")
        
        # Ask the user to choose a room
        room_id = input("\nEnter the ID of the room you want to book: ")
        time_slot= input("\nEnter the time you would like to book the room: ")
        
        # Check if the room is available
        cur.execute("SELECT * FROM rooms_schedule WHERE room_id = %s AND time_slot = %s AND status = 'available';", (room_id,time_slot))
        available_room = cur.fetchone()
        
        if not available_room:
            print("Error: The selected room is not available for booking.")
            return False
        
        # Book the room
        cur.execute("UPDATE rooms_schedule SET status = 'booked' WHERE room_id = %s AND time_slot= %s;", (room_id,time_slot))
        conn.commit()
        print("Room has been successfully booked.")
        return True
    
    except psycopg2.Error as e:
        conn.rollback()
        print("Error booking room:", e)
        return False

def equipment_maintenance():
    
    # Assumption , admin staff uses this page to add or change the status of existing piece of equipment
    
    option = input("\n1.) Add equipment \n2.) Change the status of existing equipment\n\n choice: ")
    
    
    cur=conn.cursor()
    
    if(option =="1"):
        e_id=input ("\nEnter the equipment uid :")
        e_name = input("\nEnter the name of the equipment :")
        e_status = input ("\nEnter the status of the equipment ( working / under maintenance )")
        
        # Check if equipment with the given UID already exists
        cur.execute("SELECT * FROM equipments WHERE equipment_id = %s;", (e_id,))
        existing_equipment = cur.fetchone()
        if existing_equipment:
            print("Equipment with the same UID already exists.")
            return False
        
        # Insert new equipment into the table
        cur.execute("INSERT INTO equipments (equipment_id, equipment_name, condition) VALUES (%s, %s, %s);",
                    (e_id, e_name, e_status))
        conn.commit()
        print("Equipment successfully added.")

    elif(option =="2"):
        display_all_equipment()
        # Change the status of existing equipment
        e_id = input("\nEnter the UID of the equipment you would like to change: ")
        new_status = input("Enter the new status of the equipment (working / under maintenance): ")
        
        # Check if equipment with the given UID exists
        try:
            cur.execute("SELECT * FROM equipments WHERE equipment_id = %s;", (e_id,))
            existing_equipment = cur.fetchone()
            if not existing_equipment:
                print("Equipment with the specified UID does not exist.")
                
        except psycopg2.Error as e:
            conn.rollback()
            print("Error finding equipment with that UID :", e)
            return False
        
        # Update the status of the equipment
        cur.execute("UPDATE equipments SET condition = %s WHERE equipment_id = %s;", (new_status, e_id))
        conn.commit()
        print("Equipment status successfully changed.")
    else: 
        print("Invalid option")
    pass

def display_all_equipment():
    try:
        # Retrieve and display all equipment
        print("\nAll Equipment:")
        cur = conn.cursor()
        cur.execute("SELECT * FROM equipments;")
        equipment = cur.fetchall()
        
        if not equipment:
            print("No equipment available.")
            return False
        
        for item in equipment:
            print(f"Equipment ID: {item[0]}, Equipment Name: {item[1]}, Status: {item[2]}")
        
        return True
    
    except psycopg2.Error as e:
        print("Error displaying equipment:", e)
        return False

""" DONE """
def show_available_rooms_with_slots():
    try:
        # Display all available rooms along with their available time slots
        print("\nAvailable Rooms:")
        cur = conn.cursor()
        cur.execute("""
            SELECT r.room_id, r.room_name, rs.time_slot
            FROM rooms r
            JOIN rooms_schedule rs ON r.room_id = rs.room_id
            WHERE rs.status = 'available';
        """)
        available_rooms = cur.fetchall()
        
        if not available_rooms:
            print("No rooms available at the moment.")
            return False
        
        current_room = None
        for room in available_rooms:
            if room[0] != current_room:
                if current_room:
                    print()  # Add a newline to separate rooms
                print(f"Room ID: {room[0]}, Room Name: {room[1]}")
                print("Available Time Slots:")
                current_room = room[0]
            print(f"- {room[2]}")
        
        return True
    
    except psycopg2.Error as e:
        print("Error fetching available rooms with slots:", e)
        return False

# Used to update the class schedule
def class_schedule_updating():
    try:
        print("\nThese are the current available classes ")
        cur=conn.cursor()
        # RUN QUERY TO RETURN ALL EXISTING CLASSES
        cur.execute("SELECT * FROM class_schedule;")
        existing_classes = cur.fetchall()
        print("Existing classes:")
        for row in existing_classes:
            print(row)
        
        option = input("\n1.) Add a class \n2.) Update a class time \n3.) Cancel an existing class: ")
        
        
        if option == "1":
            show_available_rooms_with_slots()
            
            c_name = input("\nEnter the class name: ")
            c_time = input("Enter the class time (morning , afternoon , evening ): ")
            c_room = input("Enter the class room id: ")
            
            # Check if room is available at the specified time
            cur.execute("SELECT * FROM rooms_schedule WHERE room_id = %s AND time_slot = %s AND status != 'available' ;", (c_room, c_time))
            existing_booking = cur.fetchone()
            if existing_booking:
                print("Room is already booked at the specified time.")
                return False
            
            # Add the new class to the class_schedule table
            cur.execute("INSERT INTO class_schedule (class_name, time_slot, room_id , availability) VALUES (%s, %s, %s, 'available');",
                        (c_name, c_time, c_room))
            
            # Update room schedule to reflect booked status
            cur.execute("UPDATE rooms_schedule SET status = 'booked' WHERE room_id = %s AND time_slot = %s;", (c_room, c_time))
            
            
            conn.commit()
            print("\nClass was successfully added.")

        elif option == "2":
            c_id = input("\nEnter the UID of the class you want to update: ")
            new_time = input("Enter the new time for the class:(morning , afternoon , evening ):  ")
            
            # Check if class with the given UID exists
            cur.execute("SELECT * FROM class_schedule WHERE class_id = %s;", (c_id,))
            existing_class = cur.fetchone()
            if not existing_class:
                print("Class with the specified UID does not exist.")
                return False
            
            # Update the time of the class
            cur.execute("UPDATE class_schedule SET time_slot = %s WHERE class_id = %s;", (new_time, c_id))
            conn.commit()
            print("\nClass time was successfully updated.")
        
        elif option == "3":
            c_id = input("\nEnter the UID of the class you would like to cancel: ")

            # Check if class with the given UID exists
            cur.execute("SELECT * FROM class_schedule WHERE class_id = %s;", (c_id,))
            existing_class = cur.fetchone()
            if not existing_class:
                print("Class with the specified UID does not exist.")
                return False
            
            # Get room ID and time slot of the class to be canceled
            cur.execute("SELECT room_id, time_slot FROM class_schedule WHERE class_id = %s;", (c_id,))
            class_info = cur.fetchone()
            room_id, time_slot = class_info
            
            # Update room schedule to reflect available status
            cur.execute("UPDATE rooms_schedule SET status = 'available' WHERE room_id = %s AND time_slot = %s;", (room_id, time_slot))
            
            
            # Delete the class from the class_schedule table
            cur.execute("DELETE FROM class_schedule WHERE class_id = %s;", (c_id,))
            conn.commit()
            print("\nClass was successfully cancelled.")
            
            
        
        else:
            print("\nPlease enter a valid option.")
    
    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)
        return False
    


def billing():
    # Just implement a fake billing process and state approved
    print("\n\n PAYMENT AND INFORMATION ")
    
    p_choice = input("\nHow would you like to pay \n1.)Credit/Debit\n2.)Cash :\n")
    if p_choice=='1':
        
        p_creds = input("Enter your credentials :")
        
        print("Transaction approved")
        return True
    elif p_choice=='2':
        #could create some sort of system whereby a transaction number is linked to the current details and yada yada
        print("This is your transaction number "".  Please provide to one of our admin staff who will kindly assist you.")
        return False
        
# Main function program starter
def main():
    # Establish connection to PostgreSQL and initiate the global variable conn
    connect_to_postgresql()
    
    # Command line interface Login page 
    
    # Every individual page should have an option for returning back to the main page
    
    
    print(" WELCOME TO CLUB FITNESS ")
    option = input("LOGIN PAGE\n1.) Member Login\n2.) New member registration\n3.) Trainer Login\n4.) Admin Login\nEnter option: ")
    
    if(option == "1"):
        
        verify_member_login()
        
        pass    
    
    elif(option=="2"):
        
        #Just pass all this in to the member registration function TO MAKE THE MAIN FUNCTION LESS crowded.
        
        new_mem_eid=input("\nPlease provide your email account for registration: ")
        new_pass=input("\nType in a password for your account :")
        conf_pass=input("\nRe-type in the password:")
        
        if(new_pass == conf_pass):
            # Pass in conf pass and all other details in to the member function
            add_account(new_mem_eid , conf_pass)  
            member_registration(new_mem_eid)
            pass    
    
    elif(option=="3"):
        verify_trainer_login()
    
        
    elif(option=="4"):
        verify_admin_login()
        
    else:
        pass
    
    
    print(option)

    #Option determines the login function to call
    
    # # Close PostgreSQL connection
    # if conn:
    #     conn.close()

if __name__ == "__main__":
    main()
