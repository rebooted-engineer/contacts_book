import json
import re


# ─── Utilities (standalone functions) ────────────────
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


# ─── Core (class) ────────────────────────────────────
class ContactsBook:
    def __init__(self, file_name):
        self.file_name = file_name
        self.contacts = self.load()

    def load(self):
        try:
            with open(self.file_name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: contacts file is corrupted. Starting fresh.")
            return []

    def save(self):
        with open(self.file_name, "w") as f:
            json.dump(self.contacts, f)

    def add(self, name, phone, email):
        if self.search(name):
            print("contact already exist")
            return
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save()
        print("✅ Contact saved successfully.")

    def search(self, name):
        return [
            contact
            for contact in self.contacts
            if contact["name"].lower() == name.lower()
        ]

    def delete(self, name):
        matches = [c for c in self.contacts if c["name"].lower() == name.lower()]
        if not matches:
            print(f"No contact named '{name}' found.")
            return
        self.contacts = [c for c in self.contacts if c["name"].lower() != name.lower()]
        self.save()
        print(f"Contact '{name}' deleted successfully.")

    def list_all(self, contacts=None):
        data = contacts if contacts is not None else self.contacts
        if not data:
            print("No contacts found.")
            return
        for i, contact in enumerate(data, start=1):
            print(
                f"{i}. Name: {contact['name']} | Phone: {contact['phone']} | Email: {contact['email']}"
            )


def main():
    book = ContactsBook("contacts.json")
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
                book.add(name, phone, email)
            case "2":
                name = get_valid_input("Enter your name: ")
                results = book.search(name)
                if not results:
                    print(f"No contact named '{name}' found.")
                else:
                    book.list_all_from(results)
            case "3":
                name = get_valid_input("Contact name to delete: ")
                book.delete(name)
            case "4":
                book.list_all()
            case "5":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 5.")


main()
