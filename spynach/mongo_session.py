from ming import Session
from ming.odm import ThreadLocalODMSession, Mapper

mainsession = Session()
DBSession = ThreadLocalODMSession(mainsession)

def init_model(engine):
    mainsession.bind = engine

    Mapper.compile_all()

    for mapper in Mapper.all_mappers():
        mainsession.ensure_indexes(mapper.collection)
