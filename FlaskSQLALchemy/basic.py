# Create Entries into the tables

from models import db, Puppy, Owner, Toy

# Create 2 puppies
rufus = Puppy("Rufus")
fido = Puppy("Fido")

## Add puppies to the DB
db.session.add_all([rufus, fido])
db.session.commit()

# Check
print(Puppy.query.all())

rufus = Puppy.query.filter_by(name='Rufus').first()
print(rufus)

# Create an Owner
kairi = Owner("Kairi", rufus.id)

# Give rufus some toys
toy1 = Toy("Chew Toy", rufus.id)
toy2 = Toy("Ball", rufus.id)

db.session.add_all([kairi, toy1, toy2])
db.session.commit()

# Grab rufus again
rufus = Puppy.query.filter_by(name="Rufus").first()
print(rufus)

rufus.report_toys

db.session.close()
