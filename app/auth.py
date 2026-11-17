from db import get_user, add_user

def auth(user: str | None, pw: str | None) -> tuple[bool, str]:
  if user is None:
    return False, "USERNAME EMPTY"

  if pw is None:
    return False, "PASSWORD EMPTY"

  entry = get_user(user)
  if entry is None or len(entry) == 0:
    return False, "USER NOT FOUND"

  if len(entry) > 1:
    raise Exception("DB ERROR: Multiple users with same username found")

  if entry[0]["password"] == pw: # TODO add hashing
    return True, "SUCCESS"

  if entry[0]["password"] != pw:
    return False, "INCORRECT PASSWORD"

  raise Exception("FATAL ERROR: This exception shouldn't happen")

def auth_signup(user: str | None, pw: str | None):
  if user is None:
    return False, "USERNAME EMPTY"

  if pw is None:
    return False, "PASSWORD EMPTY"

  entry = get_user(user)
  if len(entry) != 0:
    return False, "USERNAME ALREADY EXISTS"

  add_user(user, pw)
  return True, "SUCCESS"
