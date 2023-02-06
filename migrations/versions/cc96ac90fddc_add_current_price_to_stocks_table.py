"""add current price to stocks table

Revision ID: cc96ac90fddc
Revises: 75d5f29e3790
Create Date: 2023-02-05 09:45:59.516822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc96ac90fddc'
down_revision = '75d5f29e3790'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password_hashed', sa.String(length=128), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('email_confirmation_sent_on', sa.DateTime(), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
    sa.Column('email_confirmed_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stock_symbol', sa.String(), nullable=False),
    sa.Column('number_of_shares', sa.Integer(), nullable=False),
    sa.Column('purchase_price', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('purchase_date', sa.DateTime(), nullable=True),
    sa.Column('current_price', sa.Integer(), nullable=True),
    sa.Column('current_price_date', sa.DateTime(), nullable=True),
    sa.Column('position_value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stocks')
    op.drop_table('users')
    # ### end Alembic commands ###
