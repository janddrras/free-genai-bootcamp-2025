"""Initial migration

Revision ID: 0001
Revises: 
Create Date: 2024-02-13 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create words table
    op.create_table('words',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hungarian', sa.String(), nullable=False),
        sa.Column('english', sa.String(), nullable=False),
        sa.Column('parts', sqlite.JSON, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_words_hungarian'), 'words', ['hungarian'], unique=False)
    op.create_index(op.f('ix_words_english'), 'words', ['english'], unique=False)

    # Create groups table
    op.create_table('groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_groups_name'), 'groups', ['name'], unique=True)

    # Create words_groups table
    op.create_table('words_groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create study_activities table
    op.create_table('study_activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('thumbnail_url', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create study_sessions table
    op.create_table('study_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('study_activity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
        sa.ForeignKeyConstraint(['study_activity_id'], ['study_activities.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create word_review_items table
    op.create_table('word_review_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('word_id', sa.Integer(), nullable=False),
        sa.Column('study_session_id', sa.Integer(), nullable=False),
        sa.Column('correct', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['study_session_id'], ['study_sessions.id'], ),
        sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('word_review_items')
    op.drop_table('study_sessions')
    op.drop_table('study_activities')
    op.drop_table('words_groups')
    op.drop_table('groups')
    op.drop_table('words') 