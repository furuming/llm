"""create user table

Revision ID: 51379f61ab67
Revises: 
Create Date: 2026-05-24 08:26:33.628945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51379f61ab67'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=26), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("password", sa.Text(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "email_verified_at",
            sa.DateTime(),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True
        ),
        sa.Column(
            "deleted_at",
            sa.DateTime(),
            nullable=True
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")