"""user, order, test models work

Revision ID: 5fe2ff8986d7
Revises: 2530e177d0c6
Create Date: 2024-03-24 22:03:35.512934

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5fe2ff8986d7"
down_revision = "2530e177d0c6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "biological_test",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column(
            "test_type",
            sa.Enum("BLOOD_TEST", "DNA_TEST", name="testtype"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_biological_test_test_type"),
        "biological_test",
        ["test_type"],
        unique=False,
    )
    op.create_table(
        "blood_test",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("glucose", sa.Float(), nullable=True),
        sa.Column("cholesterol", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["biological_test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "dna_test",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("gene1", sa.String(length=50), nullable=True),
        sa.Column("gene2", sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"],
            ["biological_test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "order",
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("user_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("test_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["biological_test.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_test_id"), "order", ["test_id"], unique=False)
    op.create_index(op.f("ix_order_user_id"), "order", ["user_id"], unique=False)
    op.add_column("user", sa.Column("name", sa.String(length=254), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "name")
    op.drop_index(op.f("ix_order_user_id"), table_name="order")
    op.drop_index(op.f("ix_order_test_id"), table_name="order")
    op.drop_table("order")
    op.drop_table("dna_test")
    op.drop_table("blood_test")
    op.drop_index(op.f("ix_biological_test_test_type"), table_name="biological_test")
    op.drop_table("biological_test")
    op.execute("DROP TYPE IF EXISTS testtype")
    # ### end Alembic commands ###
