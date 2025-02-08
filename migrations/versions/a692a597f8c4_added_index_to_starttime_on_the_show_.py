"""added index to starttime on the show model

Revision ID: a692a597f8c4
Revises: 9e2fbbb87173
Create Date: 2025-02-08 15:22:00.428638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a692a597f8c4'
down_revision = '9e2fbbb87173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_shows_start_time'), ['start_time'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shows', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_shows_start_time'))

    # ### end Alembic commands ###
