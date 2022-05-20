# Notes for the course
## Alembic
### Start the migrations
`alembic init migrations`

### Generate the migration files
`alembic revision --autogenerate -m "Initial"` 
### Apply the changes
`alembic upgrade head`