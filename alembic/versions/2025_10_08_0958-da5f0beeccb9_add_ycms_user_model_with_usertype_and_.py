"""Add YCMS user model with UserType and UserRole enums

Revision ID: da5f0beeccb9
Revises: 
Create Date: 2025-10-08 09:58:54.548572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da5f0beeccb9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Create UserType enum
    user_type_enum = sa.Enum('aladdin', 'supplier', name='user_type_enum', create_type=True)
    user_type_enum.create(op.get_bind(), checkfirst=True)
    
    # Create UserRole enum
    user_role_enum = sa.Enum(
        'super_admin', 'aladdin_admin', 'aladdin_staff',
        'supplier_admin', 'supplier_staff',
        name='user_role_enum', create_type=True
    )
    user_role_enum.create(op.get_bind(), checkfirst=True)
    
    # Create users table with FastAPI-Users fields + YCMS extensions
    op.create_table(
        'users',
        # FastAPI-Users standard fields
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        
        # YCMS-specific fields
        sa.Column('user_type', user_type_enum, nullable=False, comment='Type of user: aladdin or supplier'),
        sa.Column('role', user_role_enum, nullable=False, comment='User role with specific permissions'),
        sa.Column('first_name', sa.String(length=100), nullable=False, comment="User's first name"),
        sa.Column('last_name', sa.String(length=100), nullable=False, comment="User's last name"),
        sa.Column('phone_number', sa.String(length=20), nullable=True, comment='Contact phone number'),
        sa.Column('avatar_url', sa.String(length=500), nullable=True, comment='Profile picture URL'),
        sa.Column('supplier_id', sa.Integer(), nullable=True, comment='Foreign key to supplier (required for supplier users)'),
        
        # Timestamp fields from TimestampMixin
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'], ondelete='SET NULL'),
        sa.UniqueConstraint('email')
    )
    
    # Create indexes for better query performance
    op.create_index('ix_users_email', 'users', ['email'])
    op.create_index('ix_users_user_type', 'users', ['user_type'])
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_index('ix_users_supplier_id', 'users', ['supplier_id'])


def downgrade() -> None:
    """Downgrade database schema."""
    # Drop indexes
    op.drop_index('ix_users_supplier_id', table_name='users')
    op.drop_index('ix_users_role', table_name='users')
    op.drop_index('ix_users_user_type', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    
    # Drop table
    op.drop_table('users')
    
    # Drop enums
    sa.Enum(name='user_role_enum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='user_type_enum').drop(op.get_bind(), checkfirst=True)
