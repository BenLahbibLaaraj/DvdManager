import os
from Database import Database, DVDMod, ActorMod, CharacterMod
from Export import export

def clear():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_main_menu():
    """Display the main menu."""
    print("1. Add DVD")
    print("2. Delete DVD")
    print("3. Update DVD")
    print("4. List DVD's")
    print("5. Add Actor")
    print("6. List Actors")
    print("7. Add Character")
    print("8. List Characters")
    print("9. Export to CSV")
    print("10. Exit")

def display_export_menu():
    """Display the export menu."""
    print("1. DVD Table")
    print("2. Actor Table")
    print("3. Character Table")

def get_option(prompt, valid_options):
    """Get a valid option from the user."""
    while True:
        option = input(prompt)
        if option in valid_options:
            return option
        else:
            print(f"Invalid option. Please choose from {', '.join(valid_options)}.")

# Initialize instances
database = Database()
dvd = DVDMod()
actor = ActorMod()
character = CharacterMod()
export = export()

# Create the database tables
database.create()

while True:
    clear()
    display_main_menu()
    option = get_option("Select an option: ", [str(i) for i in range(1, 11)])

    match option:
        case "1":
            clear()
            title = input("Title of DVD: ")
            release_date = input("Release date of DVD: ")
            language = input("Original language of DVD: ")
            barcode = input("Barcode of DVD (Optional): ")
            dvd.insertdvd(title, release_date, language, barcode)
        case "2":
            clear()
            title = input("Title of DVD: ")
            dvd.removedvd(title)
        case "3":
            clear()
            orgtitle = input("(old) Title of DVD: ")
            title = input("New Title of DVD (Optional): ")
            barcode = input("New Barcode of DVD (Optional): ")
            dvd.updatedvd(orgtitle, title, barcode)
        case "4":
            clear()
            dvd.listDVD()
            input("Press Enter to continue...")
        case "5":
            clear()
            name = input("Name of actor: ")
            title = input("Title of dvd: ")
            actor.addActor(name, title)
        case "6":
            clear()
            actor.listActor()
            input("Press Enter to continue...")
        case "7":
            clear()
            name = input("Name of character: ")
            actorname = input("Name of Actor: ")
            character.addCharacter(name, actorname)
        case "8":
            clear()
            character.listCharacters()
            input("Press Enter to continue...")
        case "9":
            clear()
            display_export_menu()
            option2 = get_option("Select an option: ", ["1", "2", "3"])
            match option2:
                case "1":
                    export.export_to_csv('DVD', 'dvd_data.csv')
                case "2":
                    export.export_to_csv('Actor', 'actor_data.csv')
                case "3":
                    export.export_to_csv('Character', 'character_data.csv')
            input("Press Enter to continue...")
        case "10":
            break
