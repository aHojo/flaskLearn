from task import db, Puppy

# Creates all of the tables from models
db.create_all()

sam = Puppy("Sammy", 3)
frank = Puppy("Frank", 4)

print(sam.id)
print(frank.id)

db.session.add_all([sam, frank])
db.session.commit()

print(sam.id)
print(frank.id)

