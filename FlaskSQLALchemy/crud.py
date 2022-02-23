from task import db, Puppy


## CREATE ##
my_puppy = Puppy("Rufus", 5)
db.session.add(my_puppy)
db.session.commit()

## READ ##
all_puppies = Puppy.query.all() # list of pupppies objects in the tables
print(all_puppies)

puppy_one = Puppy.query.get(1)
print(puppy_one.name)

# Filters #
puppy_frankie = Puppy.query.filter_by(name="frank")
print(puppy_frankie.all())

#### UPDATE
first_puppy = Puppy.query.get(1)
first_puppy.age = 10
db.session.add(first_puppy)
db.session.commit()

#### Delete ###
second_pup = Puppy.query.get(2)
db.session.delete(second_pup)
db.session.commit()

all_puppies = Puppy.query.all()
print(all_puppies)


