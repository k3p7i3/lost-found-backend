import hashlib


def check_password_content(password: str) -> bool:
    if len(password) < 8:
        return False

    # use triple-quotes due to both kinds of quotes in str
    special_symbols = r"""!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"""

    for sym in password:
        if sym.isalnum() or sym in special_symbols:
            continue
        return False

    return True


def hash_password(password: str) -> str:
    database_password = password + "lostfound"  # add static salt
    hashed = hashlib.md5(database_password.encode()).hexdigest()
    return hashed


def check_password_match(password: str, hashed_password: str):
    return password == hashed_password
