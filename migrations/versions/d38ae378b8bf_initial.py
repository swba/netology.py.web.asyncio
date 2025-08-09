"""initial

Revision ID: d38ae378b8bf
Revises: 
Create Date: 2025-08-08 23:38:52.262137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd38ae378b8bf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('planet',
    sa.Column('climate', sa.String(length=30), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('terrain', sa.String(length=100), nullable=True),
    sa.Column('gravity', sa.String(length=100), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('population', sa.BigInteger(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('person',
    sa.Column('birth_year', sa.String(length=10), nullable=True),
    sa.Column('eye_color', sa.String(length=30), nullable=True),
    sa.Column('gender', sa.String(length=30), nullable=True),
    sa.Column('hair_color', sa.String(length=30), nullable=True),
    sa.Column('homeworld_id', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('skin_color', sa.String(length=30), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['homeworld_id'], ['planet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('person')
    op.drop_table('planet')
