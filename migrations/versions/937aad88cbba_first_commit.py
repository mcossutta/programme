"""First commit

Revision ID: 937aad88cbba
Revises: 
Create Date: 2022-07-24 10:33:43.936190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '937aad88cbba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('liste',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nom')
    )
    op.create_table('professeur',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=True),
    sa.Column('prenom', sa.String(length=100), nullable=True),
    sa.Column('trigramme', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nom')
    )
    op.create_table('abonnement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_professeur', sa.Integer(), nullable=True),
    sa.Column('id_liste', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_liste'], ['liste.id'], ),
    sa.ForeignKeyConstraint(['id_professeur'], ['professeur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('eleve',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=100), nullable=True),
    sa.Column('prenom', sa.String(length=100), nullable=True),
    sa.Column('classe', sa.String(length=10), nullable=True),
    sa.Column('id_professeur', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_professeur'], ['professeur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(length=128), nullable=True),
    sa.Column('id_theme', sa.Integer(), nullable=True),
    sa.Column('id_liste', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_liste'], ['liste.id'], ),
    sa.ForeignKeyConstraint(['id_theme'], ['theme.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('niveau', sa.Integer(), nullable=True),
    sa.Column('note', sa.Integer(), nullable=True),
    sa.Column('id_item', sa.Integer(), nullable=True),
    sa.Column('id_eleve', sa.Integer(), nullable=True),
    sa.Column('id_professeur', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_eleve'], ['eleve.id'], ),
    sa.ForeignKeyConstraint(['id_item'], ['item.id'], ),
    sa.ForeignKeyConstraint(['id_professeur'], ['professeur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('note')
    op.drop_table('item')
    op.drop_table('eleve')
    op.drop_table('abonnement')
    op.drop_table('theme')
    op.drop_table('professeur')
    op.drop_table('liste')
    # ### end Alembic commands ###
