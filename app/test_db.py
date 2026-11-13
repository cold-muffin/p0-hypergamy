from db import __reset, add_user

if __name__ == "__main__":
    __reset()
    add_user("JohnDoe", "password123")