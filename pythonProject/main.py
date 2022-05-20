import databases
import sqlalchemy
from fastapi import FastAPI
from decouple import config


# db url
from starlette.requests import Request

DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:{config('PORT')}/store"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()



books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
    # sqlalchemy.Column("reader_id", sqlalchemy.ForeignKey("readers.id"), nullable=False, index=True) #make sure to use the table name -- for one to many
)

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
)

# junction table
readers_books = readers = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey("books.id"), nullable=False),
    sqlalchemy.Column("reader_id", sqlalchemy.ForeignKey("readers.id"), nullable=False),
)


# engine = sqlalchemy.create_engine(DATABASE_URL)
#creates all of our tables
# metadata.create_all(engine)

app = FastAPI()

# interceptors or middlewares
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/books/")
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query) # returns a list of dictionaries

@app.post("/books/")
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(**data) #unpack the dictionary title=data["title"], author=data["author"]
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@app.post("/readers/")
async def create_book(request: Request):
    data = await request.json()
    query = readers.insert().values(**data) #unpack the dictionary title=data["title"], author=data["author"]
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

@app.post("/read/")
async def read_book(request: Request):
    data = await request.json()
    query = readers_books.insert().values(**data)  # unpack the dictionary title=data["title"], author=data["author"]
    last_record_id = await database.execute(query)
    return {"id": last_record_id}
