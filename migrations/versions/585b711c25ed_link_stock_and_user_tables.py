"""link stock and user tables

Revision ID: 585b711c25ed
Revises: d39c44c1e83c
Create Date: 2023-02-01 08:46:39.674873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '585b711c25ed'
down_revision = 'd39c44c1e83c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_user_stocks", 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.drop_constraint("fk_user_stocks", type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
