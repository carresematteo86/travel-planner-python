# Travel Planner App

Travel Planner App is a desktop application developed in Python that allows users to search for travel suggestions, view available reservation options, and confirm bookings.

The application includes a user area and an administrator area. Users can enter their personal information, search for destinations, reserve available options, and view their confirmed reservations. Administrators can add new travel suggestions, view saved suggestions, and check all reservations made by users.

## Features

* Desktop interface built with Tkinter
* User registration with basic input validation
* Destination search with partial matching
* Travel suggestion system
* Reservation confirmation
* User area to view personal reservations
* Administrator area protected by password
* Admin option to add new travel suggestions
* Admin option to view all user reservations
* SQLite database for persistent data storage
* Automatic migration support from an older JSON-based data system

## Technologies Used

* Python
* Tkinter
* SQLite
* Object-Oriented Programming
* File handling
* JSON migration

## Project Structure

```text
travel-planner-python/
│
├── main.py          # Main application and Tkinter interface
├── database.py      # SQLite database functions
├── planeador.py     # Travel suggestion class
├── utilizador.py    # User class
├── Ficheiros2.py    # Previous JSON-based storage system
└── README.md
```

## How It Works

When the application starts, it creates the necessary SQLite database tables if they do not already exist.

The user can enter their name, age, and email before searching for a destination. The application then displays matching travel suggestions and allows the user to confirm a reservation.

The administrator can log in to add new travel suggestions, load existing suggestions, and view all confirmed reservations.

## Database

The project uses SQLite to store:

* Users
* Travel suggestions
* Search records
* Confirmed reservations

The database file is automatically created when the application runs.

## How to Run

1. Make sure Python is installed on your computer.

2. Clone this repository:

```bash
git clone https://github.com/your-username/travel-planner-python.git
```

3. Open the project folder:

```bash
cd travel-planner-python
```

4. Run the application:

```bash
python main.py
```

## What I Learned

Through this project, I practiced:

* Creating graphical interfaces with Tkinter
* Working with SQLite databases
* Organizing code into multiple Python files
* Creating and using classes
* Validating user input
* Managing user reservations
* Building an administrator section
* Migrating data from JSON to a database

## Project Status

This project was developed as part of one of my university classes, where I practiced Python programming, graphical interfaces, database management, and object-oriented programming.

Future improvements could include a more modern interface design, stronger administrator authentication, search filters, and the option to edit or cancel reservations.
