"""remove description from tests

Revision ID: 53a51aae539d
Revises: df93bf4dcb1a
Create Date: 2024-04-01 00:31:02.038420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "53a51aae539d"
down_revision = "df93bf4dcb1a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("biological_test", "description")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "biological_test",
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###