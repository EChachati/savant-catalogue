"""add fields to purchase

Revision ID: f1be87d5cf1e
Revises: 80abfa89620b
Create Date: 2023-12-24 18:31:41.426469

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "f1be87d5cf1e"
down_revision: Union[str, None] = "80abfa89620b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("purchase", "company_id",
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.add_column("purchaseproductlink", sa.Column("quantity", sa.Integer(), nullable=False))
    op.add_column("purchaseproductlink", sa.Column("amount", sa.Numeric(scale=2), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("purchaseproductlink", "amount")
    op.drop_column("purchaseproductlink", "quantity")
    op.alter_column("purchase", "company_id",
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###
