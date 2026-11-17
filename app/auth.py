from db import get_user, add_user

def auth(user: str | None, pw: str | None) -> tuple[bool, str]:
  if user is None:
    return False, "USEREMPTY"

  if pw is None:
    return False, "PASSEMPTY"

  entry = get_user(user)
  if entry is None or len(entry) == 0:
    return False, "USERNOTFOUND"

  if len(entry) > 1:
    raise Exception("DB ERROR: Multiple users with same username found")

  if entry[0]["password"] == pw: # TODO add hashing
    return True, "SUCCESS"

  if entry[0]["password"] != pw:
    return False, "INCORRECTPW"

  raise Exception("FATAL ERROR: This exception shouldn't happen")

def auth_signup(user: str | None, pw: str | None):
  if user is None:
    return False, "USEREMPTY"

  if pw is None:
    return False, "PASSEMPTY"

  entry = get_user(user)
  if len(entry) != 0:
    return False, "USEREXIST"

  add_user(user, pw)
  return True, "SUCCESS"
