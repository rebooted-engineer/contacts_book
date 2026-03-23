import json
import re


def is_valid_phone(phone):
    pattern = r"^(03|\+92)\d{9}$"
    return bool(re.match(pattern, phone))


def is_valid_email(email):
    pattern = r"^[^@]+@[^@]+\.[^@]{2,}$"
    return bool(re.match(pattern, email))


def get_valid_input(prompt, field_type=""):
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty. Please try again.")
            continue
        if field_type == "phone":
            if not is_valid_phone(value):
                print("Phone number can only contain digits, dashes, + or spaces.")
                continue
        if field_type == "email":
            if not is_valid_email(value):
                print("Please enter a valid email address.")
                continue
        return value


def load_contacts(file_name):
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: contacts file is corrupted. Starting fresh.")
        return []


def save_contacts(file_name, contacts):
    with open(file_name, "w") as f:
        json.dump(contacts, f)


def add_contact(contacts, name, phone, email):
    if search_contact(contacts, name):
        print("contact already exist")
        return contacts
    contacts.append({"name": name, "phone": phone, "email": email})
    print("✅ Contact saved successfully.")
    return contacts


def search_contact(contacts, name):
    return [contact for contact in contacts if contact["name"].lower() == name.lower()]


def delete_contact(contacts, name):
    matches = [c for c in contacts if c["name"].lower() == name.lower()]
    if not matches:
        print(f"No contact named '{name}' found.")
        return contacts  # return unchanged

    return [c for c in contacts if c["name"].lower() != name.lower()]


def list_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return
    for i, contact in enumerate(contacts, start=1):
        print(
            f"{i}. Name: {contact['name']} | Phone: {contact['phone']} | Email: {contact['email']}"
        )


def main():
    contacts = load_contacts("contacts.json")

    while True:
        # ✅ Clean and readable
        print("\n==== Contacts Book ====")
        print("choose the option 1-5")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Delete Contact")
        print("4. List All Contacts")
        print("5. Exit")
        option = get_valid_input("Enter your number: ")
        match option:
            case "1":
                name = get_valid_input("Enter your name: ")
                phone = get_valid_input("Enter your phone number: ", "phone")
                email = get_valid_input("Enter your email: ", "email")
                contacts = add_contact(contacts, name, phone, email)
                save_contacts("contacts.json", contacts)
            case "2":
                name = get_valid_input("Enter your name: ")
                results = search_contact(contacts, name)
                if not results:
                    print(f"No contact named '{name}' found.")
                else:
                    list_contacts(results)
            case "3":
                name = get_valid_input("Contact name to delete: ")
                contacts = delete_contact(contacts, name)
                save_contacts("contacts.json", contacts)
                print("contact deleted successfully")
            case "4":
                list_contacts(contacts)
            case "5":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 5.")


main()
