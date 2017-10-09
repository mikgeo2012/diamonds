from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
diamond = Table('diamond', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('price', Float),
    Column('carat', Float),
    Column('color', String(length=1)),
    Column('clarity', String(length=4)),
    Column('url', String(length=2048)),
    Column('gia_num', Integer),
    Column('depth', Float),
    Column('table', Float),
    Column('crown', Float),
    Column('pavilion', Float),
    Column('culet', Integer),
    Column('diameter', Float),
    Column('cut_score', Float),
    Column('hca_score', Float),
    Column('dim', String(length=15)),
    Column('cut', String(length=15)),
    Column('shape', String(length=15)),
    Column('dia_carat', Float),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['diamond'].columns['dia_carat'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['diamond'].columns['dia_carat'].drop()
