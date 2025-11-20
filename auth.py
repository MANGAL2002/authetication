import bcrypt
import os

USER_DATA_FILE = "users.txt"


def hash_password(plain_text_pass):
    pass_bytes = plain_text_pass.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pass_bytes, salt)
    return hashed_pass.decode('utf-8')

def verify_password(plain_text_pass, stored_hash):
    return bcrypt.checkpw(
        plain_text_pass.encode('utf-8'),
        stored_hash.encode('utf-8')
    )


def ensure_user_file():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8"):
            pass


def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            stored_user, _ = line.strip().split(",")
            if stored_user == username:
                return True
    return False


def retrieve_pass_hash(username):
    with open(USER_DATA_FILE, "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(",")
            if stored_user == username:
                return stored_hash
    return None


def register_user(username, password):
    ensure_user_file()

    if user_exists(username):
        print(f"Error: Username '{username}' already exists.")
        return False

    hashed = hash_password(password)

    with open(USER_DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{hashed}\n")

    print(f"Success: User '{username}' registered successfully!")
    return True


def login_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        print("No users registered yet.")
        return False

    stored_hash = retrieve_pass_hash(username)

    if stored_hash is None:
        print("Error: Username not found.")
        return False

    if verify_password(password, stored_hash):
        print(f"Success: Welcome, {username}!")
        return True
    else:
        print("Error: Invalid password.")
        return False


def main():
    ensure_user_file()
    print("\nWelcome to the Secure Authentication System!")

    while True:
        print("\n[1] Register")
        print("[2] Login")
        print("[3] Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            register_user(username, password)

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            login_user(username, password)

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()