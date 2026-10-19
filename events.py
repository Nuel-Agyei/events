# These dictionaries and list keep the program's information in memory.
# Each event and attendee is stored under a unique ID so it can be found quickly.
events = {
    "EV001": {
        "name": "Python Beginners Workshop",
        "category": "Workshop",
        "venue": "Accra",
        "ticket_price": 50.00,
        "capacity": 100,
        "booked_tickets": 0,
        "date": "2026-05-10"
    }
}

# Each attendee record stores the person's name and contact details.
attendees = {
    "AT001": {
        "name": "Ama Mensah",
        "contact": "ama@example.com"
    }
}

# Each booking connects one attendee to one event and saves its cost and status.
bookings = [
    {
        "booking_id": "BK001",
        "attendee_id": "AT001",
        "event_id": "EV001",
        "quantity": 5,
        "subtotal": 250.00,
        "discount": 12.50,
        "final_cost": 237.50,
        "status": "active"
    }
]

# The example booking already includes five tickets, so match the event's count.
events["EV001"]["booked_tickets"] = 5



def create_event():
    # Ask for the information needed to add an event to the events dictionary.
    print("\nCreate a New Event")
    event_id = input("Enter unique Event ID (e.g., EV002): ").strip().upper()
    
    # Do not replace an event that already uses this ID.
    if event_id in events:
        print("Error: An event with this ID already exists.")
        return

    # Remove extra spaces and require a name.
    name = input("Enter Event Name: ").strip()
    if name == "":
        print("Error: Event name cannot be blank.")
        return

    category = input("Enter Category (e.g., Workshop, Show): ").strip()
    venue = input("Enter Venue: ").strip()

    # Convert the price text into a number and reject invalid or non-positive values.
    try:
        ticket_price = float(input("Enter Ticket Price (greater than 0): "))
        if ticket_price <= 0:
            print("Error: Ticket price must be greater than zero.")
            return
    except ValueError:
        print("Error: Invalid number format for ticket price.")
        return

    # Capacity is a whole number because it counts tickets.
    try:
        capacity = int(input("Enter Capacity (positive whole number): "))
        if capacity <= 0:
            print("Error: Capacity must be a positive whole number.")
            return
    except ValueError:
        print("Error: Invalid number format for capacity.")
        return

    # Save the date as text after checking that the user entered something.
    date = input("Enter Event Date (e.g., 2026-06-15): ").strip()
    if date == "":
        print("Error: Date cannot be blank.")
        return

    # Store the new event, starting with no tickets booked.
    events[event_id] = {
        "name": name,
        "category": category,
        "venue": venue,
        "ticket_price": ticket_price,
        "capacity": capacity,
        "booked_tickets": 0,
        "date": date
    }
    print(f"Success! Event '{name}' created successfully with ID {event_id}.")


def view_all_events():
    # Show every event and calculate how many tickets are still available.
    print("\nAll Events ")
    if events == {}:
        print("No events available.")
        return

    for event_id, info in events.items():
        # Available tickets are the capacity minus tickets already booked.
        available_tickets = info["capacity"] - info["booked_tickets"]
        print(f"\nID: {event_id}")
        print(f"Name: {info['name']}")
        print(f"Category: {info['category']}")
        print(f"Venue: {info['venue']}")
        print(f"Date: {info['date']}")
        print(f"Ticket Price: ${info['ticket_price']:.2f}")
        print(f"Capacity: {info['capacity']}")
        print(f"Booked Tickets: {info['booked_tickets']}")
        
        # Display sold-out events clearly instead of showing a negative count.
        if available_tickets <= 0:
            print("Available Tickets: 0 *** SOLD OUT ***")
        else:
            print(f"Available Tickets: {available_tickets}")
        print("-" * 30)



def search_event():
    # Search event IDs and text fields without caring about letter case.
    print("\nSearch for an Event")
    keyword = input("Enter search keyword (ID, name, category, or venue): ").strip().lower()
    
    found = False
    for event_id, info in events.items():
        # A match can be the full ID or part of the name, category, or venue.
        if (keyword == event_id.lower() or 
            keyword in info["name"].lower() or 
            keyword in info["category"].lower() or 
            keyword in info["venue"].lower()):
            
            available = info["capacity"] - info["booked_tickets"]
            print(f"\nFound Event:")
            print(f"ID: {event_id} | Name: {info['name']} | Category: {info['category']} | Venue: {info['venue']}")
            print(f"Price: ${info['ticket_price']:.2f} | Capacity: {info['capacity']} | Booked: {info['booked_tickets']} | Available: {available}")
            if available <= 0:
                print("*** SOLD OUT ***")
            print("-" * 30)
            found = True

    # Let the user know when no event matched the search.
    if not found:
        print("No matching events found.")


def register_attendee():
    # Collect an attendee's details and save them under a unique ID.
    print("\n--- Register Attendee ---")
    attendee_id = input("Enter unique Attendee ID (e.g., AT002): ").strip().upper()
    
    # Prevent a new attendee from overwriting an existing attendee.
    if attendee_id in attendees:
        print("Error: Attendee ID already exists.")
        return

    name = input("Enter Full Name: ").strip()
    if name == "":
        print("Error: Name cannot be blank.")
        return

    contact = input("Enter Contact Info (Email or Phone): ").strip()
    if contact == "":
        print("Error: Contact information cannot be blank.")
        return

    # Store the attendee only after the required details have been checked.
    attendees[attendee_id] = {
        "name": name,
        "contact": contact
    }
    print(f"Success! Attendee {name} registered with ID {attendee_id}.")


def book_tickets():
    # A booking needs both an existing event and a registered attendee.
    print("\n--- Book Tickets ---")
    event_id = input("Enter Event ID: ").strip().upper()
    if event_id not in events:
        print("Error: Event does not exist.")
        return

    attendee_id = input("Enter Attendee ID: ").strip().upper()
    if attendee_id not in attendees:
        print("Error: Attendee must be registered before booking.")
        return

    # Ticket quantity must be a positive whole number.
    try:
        quantity = int(input("Enter number of tickets to book: "))
        if quantity <= 0:
            print("Error: Quantity must be a positive whole number.")
            return
    except ValueError:
        print("Error: Invalid number format.")
        return

    # Look up the event and make sure it has enough tickets left.
    event = events[event_id]
    available_tickets = event["capacity"] - event["booked_tickets"]

    if quantity > available_tickets:
        print(f"Error: Not enough tickets available. Only {available_tickets} left.")
        return

    # Multiply the ticket price by the quantity to get the cost before discounts.
    subtotal = event["ticket_price"] * quantity
    
    # Larger bookings receive a higher discount rate.
    if quantity >= 10:
        discount_rate = 0.10
    elif quantity >= 5:
        discount_rate = 0.05
    else:
        discount_rate = 0.00

    # Subtract the discount from the subtotal to get the amount to pay.
    discount_amount = subtotal * discount_rate
    final_cost = subtotal - discount_amount

    # Confirmation step
    print("\n--- Booking Summary ---")
    print(f"Event: {event['name']}")
    print(f"Attendee: {attendees[attendee_id]['name']}")
    print(f"Quantity: {quantity}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount ({int(discount_rate * 100)}%): ${discount_amount:.2f}")
    print(f"Final Cost: ${final_cost:.2f}")

    # Change the stored data only if the user confirms the booking.
    confirm = input("Confirm booking? (y/n): ").strip().lower()
    if confirm == 'y':
        # Create the next booking ID using a three-digit number, such as BK002.
        new_booking_num = len(bookings) + 1
        booking_id = f"BK{new_booking_num:03d}"

        # Save the booking details and update the event's booked-ticket count.
        booking_record = {
            "booking_id": booking_id,
            "attendee_id": attendee_id,
            "event_id": event_id,
            "quantity": quantity,
            "subtotal": subtotal,
            "discount": discount_amount,
            "final_cost": final_cost,
            "status": "active"
        }
        bookings.append(booking_record)

        event["booked_tickets"] += quantity
        print(f"Success! Booking confirmed. Your Booking ID is {booking_id}.")
    else:
        print("Booking cancelled by user. No changes made.")


def view_booking_details():
    # Find a booking by ID, then show its attendee, event, and price details.
    print("\n View Booking Details")
    booking_id = input("Enter Booking ID (e.g., BK001): ").strip().upper()

    # Start with no match; the loop will fill this in if it finds the ID.
    found_booking = None
    for b in bookings:
        if b["booking_id"] == booking_id:
            found_booking = b
            break

    if not found_booking:
        print("Error: Booking ID not found.")
        return

    # Use the IDs saved in the booking to look up the related records.
    event = events[found_booking["event_id"]]
    attendee = attendees[found_booking["attendee_id"]]

    print(f"\nBooking ID: {found_booking['booking_id']}")
    print(f"Status: {found_booking['status'].capitalize()}")
    print(f"Attendee Name: {attendee['name']}")
    print(f"Event Name: {event['name']}")
    print(f"Venue: {event['venue']}")
    print(f"Ticket Quantity: {found_booking['quantity']}")
    print(f"Ticket Price: ${event['ticket_price']:.2f}")
    print(f"Subtotal: ${found_booking['subtotal']:.2f}")
    print(f"Discount: ${found_booking['discount']:.2f}")
    print(f"Final Cost: ${found_booking['final_cost']:.2f}")
    print("-" * 30)


def cancel_booking():
    # Cancel a booking once and return its tickets to the event's available stock.
    print("\nCancel a Booking")
    booking_id = input("Enter Booking ID to cancel: ").strip().upper()

    # Find the booking before trying to change its status.
    found_booking = None
    for b in bookings:
        if b["booking_id"] == booking_id:
            found_booking = b
            break

    if not found_booking:
        print("Error: Booking ID not found.")
        return

    # Do not release tickets twice if the booking was already cancelled.
    if found_booking["status"] == "cancelled":
        print("Error: This booking has already been cancelled.")
        return

    # Mark the booking cancelled and make its tickets available again.
    found_booking["status"] = "cancelled"

    event_id = found_booking["event_id"]
    events[event_id]["booked_tickets"] -= found_booking["quantity"]

    print(f"Booking {booking_id} has been cancelled and {found_booking['quantity']} tickets have been released.")



def view_all_bookings():
    # List bookings, with an optional filter for active or cancelled bookings.
    print("\nAll Bookings")
    if bookings == []:
        print("No bookings found.")
        return

    # An empty answer means no status filter, so show every booking.
    filter_choice = input("Filter by status? (1: Active only, 2: Cancelled only, Enter: Show all): ").strip()

    for b in bookings:
        # Skip records that do not match the selected status.
        if filter_choice == "1" and b["status"] != "active":
            continue
        if filter_choice == "2" and b["status"] != "cancelled":
            continue

        # Use "Unknown" if a related attendee or event record cannot be found.
        attendee_name = attendees.get(b["attendee_id"], {}).get("name", "Unknown")
        event_name = events.get(b["event_id"], {}).get("name", "Unknown")

        print(f"\nBooking ID: {b['booking_id']}")
        print(f"Attendee: {attendee_name}")
        print(f"Event: {event_name}")
        print(f"Quantity: {b['quantity']}")
        print(f"Final Cost: ${b['final_cost']:.2f}")
        print(f"Status: {b['status'].capitalize()}")
        print("-" * 30)


def generate_event_report():
    # Summarize ticket sales and booking revenue for each event.
    print("\nEvent Report & Analytics")
    if events == {}:
        print("No events available to report.")
        return

    # Keep track of which event has the most and fewest active tickets sold.
    highest_sales = -1
    lowest_sales = float('inf')
    highest_event = "None"
    lowest_event = "None"
    any_active_bookings = False

    for event_id, info in events.items():
        # Calculate availability and the percentage of the event's capacity sold.
        capacity = info["capacity"]
        active_tickets = info["booked_tickets"]
        available = capacity - active_tickets
        
        if capacity > 0:
            pct_sold = (active_tickets / capacity) * 100
        else:
            pct_sold = 0.0

        # Start each event's totals at zero before counting its bookings.
        active_bookings_count = 0
        active_revenue = 0.0
        active_discounts = 0.0
        cancelled_bookings_count = 0

        for b in bookings:
            # Count active bookings as revenue; cancelled bookings are counted separately.
            if b["event_id"] == event_id:
                if b["status"] == "active":
                    active_bookings_count += 1
                    active_revenue += b["final_cost"]
                    active_discounts += b["discount"]
                    any_active_bookings = True
                elif b["status"] == "cancelled":
                    cancelled_bookings_count += 1

        print(f"\nEvent ID: {event_id} ({info['name']})")
        print(f"  - Total Capacity: {capacity}")
        print(f"  - Active Tickets Booked: {active_tickets}")
        print(f"  - Available Tickets: {available}")
        print(f"  - Percentage Sold: {pct_sold:.1f}%")
        print(f"  - Active Bookings Count: {active_bookings_count}")
        print(f"  - Revenue from Active Bookings: ${active_revenue:.2f}")
        print(f"  - Discounts Given: ${active_discounts:.2f}")
        print(f"  - Cancelled Bookings Count: {cancelled_bookings_count}")
        print("-" * 40)

        # Compare this event with the current highest and lowest ticket counts.
        if active_tickets > highest_sales:
            highest_sales = active_tickets
            highest_event = info['name']

        if active_tickets < lowest_sales:
            lowest_sales = active_tickets
            lowest_event = info['name']

    print("\n=== Overall Sales Highlights ===")
    # Only show sales highlights when at least one booking is still active.
    if any_active_bookings:
        print(f"Event with Highest Active Ticket Sales: {highest_event} ({highest_sales} tickets)")
        print(f"Event with Lowest Active Ticket Sales: {lowest_event} ({lowest_sales} tickets)")
    else:
        print("Tickets no dey")



def main():
    # Keep showing the menu until the user chooses to exit.
    while True:
        print("EVENT MANAGEMENT SYSTEM")
        print(" ")
        print("1. Create an event")
        print("2. View all events")
        print("3. Search for an event")
        print("4. Register an attendee")
        print("5. Book tickets")
        print("6. View booking details")
        print("7. Cancel a booking")
        print("8. View all bookings")
        print("9. Generate an event report")
        print("10. Exit")

        # Read the menu selection and run the matching function.
        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            create_event()
        elif choice == "2":
            view_all_events()
        elif choice == "3":
            search_event()
        elif choice == "4":
            register_attendee()
        elif choice == "5":
            book_tickets()
        elif choice == "6":
            view_booking_details()
        elif choice == "7":
            cancel_booking()
        elif choice == "8":
            view_all_bookings()
        elif choice == "9":
            generate_event_report()
        elif choice == "10":
            print("\nThe system dey be ehh")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 10.")


# Run the program
if __name__ == "__main__":
    main()