
import sqlalchemy

class DatabaseConnection:

    """
    This class provides a connection to the SQL Server Database.

    TODO : ADD MYSQL SUPPORT
    """

    def __init__(self):
        self.database_name = ''
        self._conn_str = 'mssql://WIN-2TMF2VILQ8A/spring_2014_blended?trusted_connection=yes'#.format(self._database_name)
        self.engine = sqlalchemy.create_engine(self._conn_str)
        self.conn = self.engine.raw_connection()
    
    def choose_database(self):

        """
        We need the ability to generate these graphs for any database from Coursera.

        Thus the user needs the ability to choose any database available.
        """
        
        print ''
        for db in self.engine.execute("select name from master.sys.sysdatabases"):
            print db[0]
        print ''
        self.database_name = raw_input("\nChoose a database to use: ")
        self._conn_str = 'mssql://WIN-2TMF2VILQ8A/{0}?trusted_connection=yes'.format(self.database_name)
        self.engine = sqlalchemy.create_engine(self._conn_str)
        self.conn = self.engine.raw_connection()

if __name__=="__main__":
    db = DatabaseConnection()
    db.choose_database()

