from __future__ import print_function, division, absolute_import

"""
Results will be returned for each of several trait types: mRNA assays, phenotypes, genotypes, and
(maybe later) genes

For each trait type, the results for each species should be given; for example, have a "Mouse" tab
with the mouse traits in a table inside it

This table will then list each trait, its dataset, and several columns determined by its trait type
(phenotype, genotype, etc)

"""


import sys
sys.path.append("../../..")

import simplejson as json

import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

from BeautifulSoup import UnicodeDammit

import zach_settings as settings

Engine = sa.create_engine(settings.SQLALCHEMY_DATABASE_URI,
                       #encoding='utf-8',
                       #client_encoding='utf-8',
                       #echo="debug",
                       )

Session = scoped_session(sessionmaker(bind=Engine)) #, extension=VersionedListener()))
#Xsession = Session()

Base = declarative_base(bind=Engine)
Metadata = sa.MetaData()
Metadata.bind = Engine


class ProbeSetXRef(Base):
    __tablename__ = 'ProbeSetXRef'
    
    ProbeSetFreezeId = sa.Column(sa.Integer, primary_key=True)
    ProbeSetId = sa.Column(sa.Integer, primary_key=True)
    DataId = sa.Column(sa.Integer, unique=True)
    Locus_old = sa.Column(sa.Text)
    LRS_old = sa.Column(sa.Float)
    pValue_old = sa.Column(sa.Float)
    mean = sa.Column(sa.Float)
    se = sa.Column(sa.Float)
    Locus = sa.Column(sa.Text)
    LRS = sa.Column(sa.Float)
    pValue = sa.Column(sa.Float)
    additive = sa.Column(sa.Float)
    h2 = sa.Column(sa.Float)

    #__mapper_args__ = {'primary_key':[ProbeSetXRef.ProbeSetId, ProbeSetXRef.ProbeSetFreezeId]}

    @classmethod
    def run(cls):
        conn = Engine.connect()
        counter = 0
        for ps in page_query(Session.query(cls)):   #all()
            values = {}
            values['table_name'] = cls.__tablename__
            values['the_key'] = json.dumps([ps.ProbeSetId, ps.ProbeSetFreezeId])
            values['terms'] = cls.get_unique_terms(ps.ProbeSetId)
            print("terms is:", values['terms'])
            #values['species'] = get_species("ProbeSet", ps.Id)
            values['result_fields'] = cls.get_result_fields(ps.ProbeSetId, ps.ProbeSetFreezeId)
            ins = QuickSearch.insert().values(**values)
            conn.execute(ins)
            counter += 1
            print("Done:", counter)        
    
    @staticmethod
    def get_unique_terms(probeset_id):
        results = Session.query(
                "name",
                "symbol",
                "description",
                "alias"
            ).from_statement(
                "SELECT ProbeSet.Name as name, "
                "ProbeSet.Symbol as symbol, "
                "ProbeSet.description as description, "
                "ProbeSet.alias as alias "
                "FROM ProbeSet "
                "WHERE ProbeSet.Id = :probeset_id ").params(probeset_id=probeset_id).all()
        
        unique = set()
        for item in results[0]:
            #print("locals:", locals())
            if not item:
                continue
            for token in item.split():
                if token.startswith(('(','[')):
                    token = token[1:]
                if token.endswith((')', ']')):
                    token = token[:-1]
                if token.endswith(';'):
                    token = token[:-1]
                if len(token) > 2:
                    try:
                        # This hopefully ensures that the token is utf-8
                        token = token.encode('utf-8')
                        print(" ->", token)
                    except UnicodeDecodeError:
                        print("\n-- UDE \n")
                        # Can't get it into utf-8, we won't use it
                        continue 
                    
                    unique.add(token)
        print("\nUnique terms are: {}\n".format(unique))
        return " ".join(unique)

    #def get_species(dataset_id):
    #    print("Before species query")
    #    results = Session.query("Name").from_statement("SELECT Species.Name "
    #                "FROM ProbeSetXRef, "
    #                "ProbeSetFreeze, "
    #                "ProbeFreeze, "
    #                "InbredSet, "
    #                "Species "
    #                "WHERE ProbeSetFreeze.Id =:probeset_freeze_id and "
    #                "ProbeSetFreeze.ProbeFreezeId = ProbeFreeze.Id and "
    #                "ProbeFreeze.InbredSetId = InbredSet.Id and "
    #                "InbredSet.SpeciesId = Species.Id").params(probeset_freeze_id=dataset_id).all()
    #    print("After query")
    #
    #    assert len(set([result.Name for result in results])) == 1, "Multiple names?"
    #
    #    print("species is:", results[0].Name)
    #
    #    return results[0].Name

    @staticmethod
    def get_result_fields(probeset_id, dataset_id):
        results = Session.query(
                "name",
                "species",
                "dataset",
                "dataset_name",
                "symbol",
                "description",
                "chr", "mb",
                "lrs",
                "genbank_id",
                "gene_id",
                "chip_id",
                "chip_name"
            ).from_statement(
                "SELECT ProbeSet.Name as name, "
                "Species.Name as species, "
                "ProbeSetFreeze.Name as dataset, "
                "ProbeSetFreeze.FullName as dataset_name, "
                "ProbeSet.Symbol as symbol, "
                "ProbeSet.description as description, "
                "ProbeSet.Chr as chr, "
                "ProbeSet.Mb as mb, "
                "ProbeSetXRef.LRS as lrs, "
                "ProbeSet.GenbankId as genbank_id, "
                "ProbeSet.GeneId as gene_id, "
                "ProbeSet.ChipId as chip_id, "
                "GeneChip.Name as chip_name "
                "FROM ProbeSet, "
                "ProbeSetXRef, "
                "ProbeSetFreeze, "
                "ProbeFreeze, "
                "InbredSet, "
                "Species, "
                "GeneChip "
                "WHERE ProbeSetXRef.ProbeSetId = :probeset_id and "
                "ProbeSetXRef.ProbeSetFreezeId = :dataset_id and "
                "ProbeSetXRef.ProbeSetId = ProbeSet.Id and "
                "ProbeSet.ChipId = GeneChip.Id and "
                "ProbeSetXRef.ProbeSetFreezeId = ProbeSetFreeze.Id and "
                "ProbeSetFreeze.ProbeFreezeId = ProbeFreeze.Id and "
                "ProbeFreeze.InbredSetId = InbredSet.Id and "
                "InbredSet.SpeciesId = Species.Id ").params(probeset_id=probeset_id,
                                                                    dataset_id=dataset_id).all()
        for result in results:
            print(result)
        assert len(set(result for result in results)) == 1, "Different results"
        
        print("results are:", results)
        result = results[0]
        result = row2dict(result)
        try:
            json_results = json.dumps(result, sort_keys=True)
        except UnicodeDecodeError:
            print("\n\nTrying to massage unicode\n\n")
            for key, value in result.iteritems():
                print("\tkey is:", key)
                print("\tvalue is:", value)
                if isinstance(value, basestring):
                    result[key] = value.decode('utf-8', errors='ignore')
            json_results = json.dumps(result, sort_keys=True)
        
        #print("json is: ", json_results)
        
        return json_results    

QuickSearch = sa.Table("QuickSearch", Metadata,
        sa.Column('table_name', sa.String(15),
                  primary_key=True, nullable=False, autoincrement=False), # table that item is inserted from
        sa.Column('the_key', sa.String(30),
                  primary_key=True, nullable=False, autoincrement=False), # key in database table
        sa.Column('terms', sa.Text), # terms to compare search string with
        #sa.Column('species', sa.Text),
        sa.Column('result_fields', sa.Text)  # json
                    )

QuickSearch.drop(Engine, checkfirst=True)
Metadata.create_all(Engine)

#class QuickSearch(Base):
#    table_name = Column(String)
#    the_key = Column(String)
#    terms = Column(String)
#    
#    def __init__(self, table_name, the_key, terms, category, species, result_fields):
#        self.table_name = table_name
#        self.the_key = the_key
#        self.terms = terms
#        self.species = species
#        self.category = category
#        self.result_fields = json.dumps(sort_keys=True)


def get_unique_terms(trait_type, trait_id):
    #if not args:
    #    return None
    
    if trait_type=="ProbeSet":
        results = Session.query(
                "name",
                "symbol",
                "description",
                "alias"
            ).from_statement(
                "SELECT ProbeSet.Name as name, "
                "ProbeSet.Symbol as symbol, "
                "ProbeSet.description as description, "
                "ProbeSet.alias as alias "
                "FROM ProbeSet"
                "WHERE ProbeSet.Id = :probeset_id ").params(probeset_id=trait_id).all()
    
    unique = set()
    for item in results[0]:
        #print("locals:", locals())
        if not item:
            continue
        for token in item.split():
            if token.startswith(('(','[')):
                token = token[1:]
            if token.endswith((')', ']')):
                token = token[:-1]
            if token.endswith(';'):
                token = token[:-1]
            if len(token) > 2:
                try:
                    # This hopefully ensures that the token is utf-8
                    token = token.encode('utf-8')
                    print(" ->", token)
                except UnicodeDecodeError:
                    print("\n-- UDE \n")
                    # Can't get it into utf-8, we won't use it
                    continue 
                
                unique.add(token)
    print("\nUnique terms are: {}\n".format(unique))
    return " ".join(unique)

def main():
    conn = Engine.connect()
    counter = 0
    
    ProbeSetXRef.run()
    
    #for ps in page_query(Session.query(ProbeSet)):   #all()
    #    values = {}
    #    values['table_name'] = "ProbeSetXRef"
    #    values['the_key'] = json.dumps([ps.ProbeSetId, ps.ProbeSetFreezeId])
    #    values['terms'] = get_unique_terms("ProbeSet", ps.ProbeSetId)
    #    print("terms is:", values['terms'])
    #    #values['species'] = get_species("ProbeSet", ps.Id)
    #    values['result_fields'] = get_result_fields("ProbeSet", ps.ProbeSetId, ps.ProbeSetFreezeId)
    #    ins = QuickSearch.insert().values(**values)
    #    conn.execute(ins)
    #    counter += 1
    #    print("Done:", counter)


def get_species(trait_type, trait_id):
    if trait_type == "ProbeSet":
        print("Before species query")
        results = Session.query("Name").from_statement("SELECT Species.Name "
                    "FROM ProbeSetXRef, "
                    "ProbeSetFreeze, "
                    "ProbeFreeze, "
                    "InbredSet, "
                    "Species "
                    "WHERE ProbeSetXRef.ProbeSetId =:probeset_id and "
                    "ProbeSetXRef.ProbeSetFreezeId = ProbeSetFreeze.Id and "
                    "ProbeSetFreeze.ProbeFreezeId = ProbeFreeze.Id and "
                    "ProbeFreeze.InbredSetId = InbredSet.Id and "
                    "InbredSet.SpeciesId = Species.Id").params(probeset_id=trait_id).all()
        print("After query")
        
        assert len(set([result.Name for result in results])) == 1, "Multiple names?"

    print("species is:", results[0].Name)

    return results[0].Name

#def get_result_fields(trait_type, *args):
#    if trait_type == "ProbeSet":
#        print("qs1")
#        results = Session.query(
#                "name",
#                "symbol",
#                "description",
#                "chr", "mb",
#                "genbank_id",
#                "gene_id",
#                "chip_id",
#                "chip_name"
#            ).from_statement(
#                "SELECT ProbeSet.Name as name, "
#                "ProbeSet.Symbol as symbol, "
#                "ProbeSet.description as description, "
#                "ProbeSet.Chr as chr, "
#                "ProbeSet.Mb as mb, "
#                "ProbeSet.GenbankId as genbank_id, "
#                "ProbeSet.GeneId as gene_id, "
#                "ProbeSet.ChipId as chip_id, "
#                "GeneChip.Name as chip_name "
#                "FROM ProbeSet, GeneChip "
#                "WHERE ProbeSet.ChipId = GeneChip.Id and "
#                "ProbeSet.Id = :probeset_id ").params(probeset_id=*args[0], dataset_id=*args[1]).all()
#        print("qs2")
#        for result in results:
#            print(result)
#        assert len(set(result for result in results)) == 1, "Different results"
#    
#    print("results are:", results)
#    result = results[0]
#    result = row2dict(result)
#    try:
#        json_results = json.dumps(result, sort_keys=True)
#    except UnicodeDecodeError:
#        print("\n\nTrying to massage unicode\n\n")
#        #print("result.__dict__ is [{}]: {}".format(type(result.__dict__), result.__dict__))
#        #resultd = dict(**result.__dict__)
#        for key, value in result.iteritems():
#            print("   key is:", key)
#            print("   value is:", value)
#            if isinstance(value, basestring):
#                result[key] = value.decode('utf-8', errors='ignore')
#        json_results = json.dumps(result, sort_keys=True)
#    
#    #print("json is: ", json_results)
#    
#    return json_results


def row2dict(row):
    return dict(zip(row.keys(), row))  # http://stackoverflow.com/a/2848519/1175849
    #"""http://stackoverflow.com/a/1960546/1175849"""
    #d = {}
    #for column in row.__table__.columns:
    #    d[column.name] = getattr(row, column.name)
    #
    #return d

def page_query(q):
    """http://stackoverflow.com/a/1217947/1175849"""
    offset = 0
    while True:
        r = False
        for elem in q.limit(1000).offset(offset):
           r = True
           yield elem
        offset += 1000
        if not r:
            break

if __name__ == "__main__":
    main()