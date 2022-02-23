from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash


bcrypt = Bcrypt()


password = 'kairiisthebest'

hashed_pw = bcrypt.generate_password_hash(password=password)

print(hashed_pw)

check = bcrypt.check_password_hash(hashed_pw, password)
print(check)
check = bcrypt.check_password_hash(hashed_pw, 'not my pw')
print(check)


hashed_w = generate_password_hash(password)
print(hashed_w)


check = check_password_hash(hashed_w, 'not my pw')
print(check)

check = check_password_hash(hashed_w, password=password)
print(check)



