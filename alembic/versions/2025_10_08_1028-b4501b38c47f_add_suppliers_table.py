"""Add suppliers table

Revision ID: b4501b38c47f
Revises: da5f0beeccb9
Create Date: 2025-10-08 10:28:50.843030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4501b38c47f'
down_revision: Union[str, None] = 'da5f0beeccb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database schema."""
    # Create suppliers table
    op.create_table(
        'suppliers',
        # Primary key
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        
        # Basic information
        sa.Column('code', sa.String(length=50), nullable=False, comment='Mã nhà cung cấp (VD: SUP001)'),
        sa.Column('name', sa.String(length=200), nullable=False, comment='Tên nhà cung cấp'),
        sa.Column('name_en', sa.String(length=200), nullable=True, comment='Tên tiếng Anh'),
        sa.Column('tax_code', sa.String(length=50), nullable=True, comment='Mã số thuế'),
        
        # Contact information
        sa.Column('email', sa.String(length=320), nullable=False, comment='Email liên hệ chính'),
        sa.Column('phone', sa.String(length=20), nullable=True, comment='Số điện thoại liên hệ'),
        sa.Column('address', sa.Text(), nullable=True, comment='Địa chỉ đầy đủ'),
        
        # Contact person
        sa.Column('contact_person', sa.String(length=100), nullable=True, comment='Tên người liên hệ'),
        sa.Column('contact_phone', sa.String(length=20), nullable=True, comment='SĐT người liên hệ'),
        sa.Column('contact_email', sa.String(length=320), nullable=True, comment='Email người liên hệ'),
        
        # Additional info
        sa.Column('description', sa.Text(), nullable=True, comment='Mô tả về nhà cung cấp'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true'), comment='Trạng thái hoạt động'),
        
        # Audit fields
        sa.Column('created_by', sa.Integer(), nullable=True, comment='User ID who created'),
        sa.Column('updated_by', sa.Integer(), nullable=True, comment='User ID who last updated'),
        
        # Soft delete fields
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.text('false'), comment='Soft delete flag'),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True, comment='Deletion timestamp'),
        sa.Column('deleted_by', sa.Integer(), nullable=True, comment='User ID who deleted'),
        
        # Timestamp fields
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        
        # Constraints
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('tax_code')
    )
    
    # Create indexes for better query performance
    op.create_index('ix_suppliers_code', 'suppliers', ['code'])
    op.create_index('ix_suppliers_name', 'suppliers', ['name'])
    op.create_index('ix_suppliers_email', 'suppliers', ['email'])
    op.create_index('ix_suppliers_tax_code', 'suppliers', ['tax_code'])
    op.create_index('ix_suppliers_is_active', 'suppliers', ['is_active'])
    op.create_index('ix_suppliers_is_deleted', 'suppliers', ['is_deleted'])


def downgrade() -> None:
    """Downgrade database schema."""
    # Drop indexes
    op.drop_index('ix_suppliers_is_deleted', table_name='suppliers')
    op.drop_index('ix_suppliers_is_active', table_name='suppliers')
    op.drop_index('ix_suppliers_tax_code', table_name='suppliers')
    op.drop_index('ix_suppliers_email', table_name='suppliers')
    op.drop_index('ix_suppliers_name', table_name='suppliers')
    op.drop_index('ix_suppliers_code', table_name='suppliers')
    
    # Drop table
    op.drop_table('suppliers')
