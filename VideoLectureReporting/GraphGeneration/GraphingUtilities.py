
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

class GraphingUtilities:

    """
    This class is a collection of utility methods and attributes that help with plotting.

    This class is mostly specific to Physics courses at GT.
    """

    def __init__(self):

        """
        The order implies the order a video was assigned in during the Fall 2013 semester.
        """
        self.lecture_order = (1,4,5,6,7,8,9,10,11,13,14,21,22,23,24,25,26,27,29,30,31,32,33,34
                              ,35,36,37,38,39,40,43,44,45,46,47,48,49,50,51, 52,55,56,57,58,59
                              ,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78)
        self.lab_order = (2,3,17,18,19,20,12,15,16,28,41,42,53,54)

    def ColorMapGenerator(self):

        """
        The color designation for bar graphs indicates whether a video is lab or lecture.

        This method creates a color map for bar graphs that assigns lecture graphs as grey (0.75)
        and laboratory graphs as crismon.
        """

        color = ['0.75' for n in range(1,79)]

        for l in self.lab_order:
            color[l-1] = 'crimson'

        return color

    def XLabelGenerator(self, weeks):

        """
        generates x labels for the number of weeks in the semester.
        """
    
        x = []
        for n,i in enumerate(np.zeros(weeks*7)):
            if n%7==0:
                x.append('week '+str(int(n/7.0+1)))
            else:
                x.append('')
    
        return x

#x = get_xlabels(15)

