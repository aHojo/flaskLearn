"""mirror many to many

Revision ID: f0fa17fde978
Revises: 2a9591d3a830
Create Date: 2022-05-19 22:43:02.239735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0fa17fde978'
down_revision = '2a9591d3a830'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('reader_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['reader_id'], ['readers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('ix_books_reader_id', table_name='books')
    op.drop_constraint('books_reader_id_fkey', 'books', type_='foreignkey')
    op.drop_column('books', 'reader_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('reader_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('books_reader_id_fkey', 'books', 'readers', ['reader_id'], ['id'])
    op.create_index('ix_books_reader_id', 'books', ['reader_id'], unique=False)
    op.drop_table('readers_books')
    # ### end Alembic commands ###
