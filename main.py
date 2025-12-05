from auth import login, register_user
from vault import upload_file, download_file, view_files


def dashboard(username, key):
    print(f"\n=== Welcome, {username}! ===\n")
    while True:
        print("Dashboard:")
        print("  [V] View files")
        print("  [U] Upload file")
        print("  [D] Download file")
        print("  [L] Logout")
        choice = input("Choose an option [V/U/D/L]: ").strip().upper()
        
        if choice == "V":
            view_files(username)
        elif choice == "U":
            upload_file(username, key)
        elif choice == "D":
            download_file(username, key)
        elif choice == "L":
            print("Logging out...")
            return
        else:
            print("Invalid choice. Enter V, U, D, or L.")


def main():
    print("=== Secure File Vault ===\n")
    while True:
        print("menu:")
        print("  [L] login")
        print("  [C] create new account")
        print("  [Q] quit")
        choice = input("Choose an option [L/C/Q]: ").strip().upper()

        if choice == "L":
            while True:
                username, key, err = login()
                if err is None:
                    print("Authenticated!")
                    dashboard(username, key)
                    break

                if err == "user_not_found":
                    print("User not found.")
                    create = input("Would you like to create a new account now? (y/n): ").strip().lower()
                    if create.startswith("y"):
                        if register_user():
                            print("Account created. Please login with your new credentials.")
                            continue
                    else:
                        break

                elif err == "wrong_password":
                    retry = input("Wrong password. Try again? (y/n): ").strip().lower()
                    if retry.startswith("y"):
                        continue
                    else:
                        break

                else:
                    print("Authentication error:", err)
                    break

        elif choice == "C":
            success = register_user()
            if success:
                print("User registered successfully!")
            continue 

        elif choice == "Q":
            print("Goodbye!")
            exit()

        else:
            print("Invalid choice. Enter L, C, or Q.")


if __name__ == "__main__":
    main()
