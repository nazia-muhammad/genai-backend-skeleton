"""add org_id workspace_id to notes

Revision ID: 9098926a203c
Revises: 6d6c5af8f647
Create Date: 2026-01-27 21:28:07.269456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "9098926a203c"
down_revision: Union[str, None] = "6d6c5af8f647"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Step 1: add columns + indexes (no foreign keys yet)
    with op.batch_alter_table("notes", schema=None) as batch_op:
        batch_op.add_column(sa.Column("org_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("workspace_id", sa.Integer(), nullable=True))

        batch_op.create_index("ix_notes_org_id", ["org_id"], unique=False)
        batch_op.create_index("ix_notes_workspace_id", ["workspace_id"], unique=False)

    # Step 2: add foreign keys in a separate batch block (avoids circular dependency error)
    with op.batch_alter_table("notes", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_notes_org_id_organizations",
            "organizations",
            ["org_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "fk_notes_workspace_id_workspaces",
            "workspaces",
            ["workspace_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("notes", schema=None) as batch_op:
        batch_op.drop_constraint("fk_notes_workspace_id_workspaces", type_="foreignkey")
        batch_op.drop_constraint("fk_notes_org_id_organizations", type_="foreignkey")

        batch_op.drop_index("ix_notes_workspace_id")
        batch_op.drop_index("ix_notes_org_id")

        batch_op.drop_column("workspace_id")
        batch_op.drop_column("org_id")
