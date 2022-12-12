"""All database related things goes here"""

from configparser import ConfigParser
from psycopg import connect
from psycopg.sql import Identifier, SQL
from psycopg.rows import class_row
from uuid import UUID

from models import ArenaModel, CharacterModel, PartyModel

def read_config(filename='database.ini', section='postgresql'):
    """Read the provided .ini file with the database connection information."""
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

class Database:

    DB_CONFIG = None
    DB_SCHEMA = "arena"

    def __init__(self):
        if Database.DB_CONFIG is None:
            Database.DB_CONFIG = read_config()

    def test_connection(self):
        """Test the conection the to database by querying the database version."""
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version()")
                version = cursor.fetchone()
                connection.commit()
                return version

    def execute(self, sql_query:str):
        """Execute a SQL command."""
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                connection.commit()

    def get_one_object(self, obj_class, table:str, uuid:UUID):
        """Get one entry from the database and return it as an object."""
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor(row_factory=class_row(obj_class)) as cursor:
                result = cursor.execute(SQL("SELECT * FROM {} WHERE uuid = %s").format(Identifier(Database.DB_SCHEMA, table)), (uuid, )).fetchone()
                connection.commit()
                return result

    def insert_one_object(self, table:str, data):
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL("INSERT INTO {} VALUES %s").format(Identifier(Database.DB_SCHEMA, table)), data)
                connection.commit()
                return cursor.rowcount == 1

    def insert_simulation(self, simulation:ArenaModel):
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                table = Identifier(Database.DB_SCHEMA, "simulation")
                query = SQL("INSERT INTO {} VALUES (%(uuid)s, %(number_of_fighters)s, %(number_of_years)s, %(fights_per_year)s)").format(table)
                cursor.execute(query, simulation.__dict__)
                connection.commit()
                return cursor.rowcount == 1

    def insert_fighter(self, fighter:CharacterModel) -> int:
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                table = Identifier(Database.DB_SCHEMA, "fighter")
                query = SQL("INSERT INTO {} VALUES (%(uuid)s, %(simulation)s, %(name)s, %(hit_dice)s, %(max_hit_points)s, %(rolled_hit_points)s, %(strength)s, %(dexterity)s, %(constitution)s, %(wisdom)s, %(intelligence)s, %(charisma)s, %(experience)s, %(age)s)").format(table)
                cursor.execute(query, fighter.__dict__)
                connection.commit()
                return cursor.rowcount

    def insert_many_fighters(self, data:list) -> int:
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                table = Identifier(Database.DB_SCHEMA, "fighter")
                query = SQL("INSERT INTO {} VALUES (%(uuid)s, %(simulation)s, %(name)s, %(hit_dice)s, %(max_hit_points)s, %(rolled_hit_points)s, %(strength)s, %(dexterity)s, %(constitution)s, %(wisdom)s, %(intelligence)s, %(charisma)s, %(experience)s, %(age)s)").format(table)
                cursor.executemany(query, data)
                connection.commit()
                return cursor.rowcount

    def insert_party(self, party:list[PartyModel]):
        pass

    def insert_many(self, table:str, data_set:list):
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                with cursor.copy(SQL("COPY {} FROM STDIN").format(Identifier(Database.DB_SCHEMA, table))) as copy:
                    for data in data_set:
                        copy.write_row(data)

    def delete_one_entry(self, table:str, uuid:UUID) -> bool:
        """Delete one entry from the database and return it as an object."""
        with connect(**Database.DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(SQL("DELETE FROM {} WHERE uuid = %s").format(Identifier(Database.DB_SCHEMA, table)), (uuid, ))
                connection.commit()
                return cursor.rowcount == 1

def create_table_simulation():
    db = Database()
    db.execute('''
-- Table: arena.simulation
DROP TABLE IF EXISTS arena.simulation;
CREATE TABLE IF NOT EXISTS arena.simulation
(
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    number_of_fighters integer NOT NULL,
    number_of_years integer NOT NULL,
    fights_per_year integer NOT NULL,
    CONSTRAINT pk_simulation PRIMARY KEY (uuid)
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS arena.simulation OWNER to postgres;
''')

def create_table_fighter():
    db = Database()
    db.execute('''
-- Table: arena.fighter
DROP TABLE IF EXISTS arena.fighter;
CREATE TABLE IF NOT EXISTS arena.fighter
(
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    simulation uuid NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    hit_dice smallint NOT NULL,
    max_hit_points smallint NOT NULL,
    rolled_hit_points smallint NOT NULL,
    strength smallint NOT NULL,
    dexterity smallint NOT NULL,
    constitution smallint NOT NULL,
    wisdom smallint NOT NULL,
    intelligence smallint NOT NULL,
    charisma smallint NOT NULL,
    experience integer NOT NULL,
    age smallint NOT NULL,
    CONSTRAINT pk_fighter PRIMARY KEY (uuid, simulation),
    CONSTRAINT fk_simulation FOREIGN KEY (simulation)
        REFERENCES arena.simulation (uuid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS arena.fighter OWNER to postgres;
''')

def create_table_party():
    db = Database()
    db.execute('''
-- Table: arena.party
DROP TABLE IF EXISTS arena.party
CREATE TABLE IF NOT EXISTS arena.party
(
    uuid uuid NOT NULL DEFAULT uuid_generate_v4(),
    number_of_fighters integer NOT NULL,
    number_of_years integer NOT NULL,
    fights_per_year integer NOT NULL,
    CONSTRAINT sim_uuid PRIMARY KEY (uuid)
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS arena.simulation OWNER to postgres;
''')

if __name__ == '__main__':
    testing = False
    if testing:
        print("Testing database connection by retrieving the DB version.")
        db = Database()
        print(db.test_connection()[0])
    else:
        create_table_simulation()
        create_table_fighter()