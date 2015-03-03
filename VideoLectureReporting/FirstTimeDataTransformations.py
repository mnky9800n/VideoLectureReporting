
import sqlalchemy


class VideoViewTable:

    """
    The raw production database from Coursera is not setup
    to do analytics out of the box easily. This class checks 
    for an existing table called '[Video Views]' with
    CreateVideoViewTable(), if it exists, drops the table and
    then creates a new table populated by data from student
    views and video lecture meta data.

    This class requires that the Coursera SQL dumps already be
    migrated to SQL Server. This can easily be handled with 
    SQL Server Migration Assistant. You can learn more about
    SSMA  at:
    https://msdn.microsoft.com/en-us/library/hh313129(v=sql.110).aspx

    // TODO

    1) make sure this works for any database from Coursera (see below since this isn't an action item)

    1.5) make it get all database names and give user option to use databases

    2) create start up query for new version of 
    [fall_2013_blended].[dbo].[SY_published_lecture_metadata_combined]

    3) test of fall_2013_blended, mooc data

    4) create version for mysql

    """

    #def __init__(self, database_name):
    def __init__(self):
        self._database_name = ''
        self._conn_str = 'mssql://WIN-2TMF2VILQ8A/spring_2014_blended?trusted_connection=yes'#.format(self._database_name)
        self._engine = sqlalchemy.create_engine(self._conn_str)
        self._conn = self._engine.raw_connection()
    
    def choose_database(self):
        print ''
        for db in self._engine.execute("select name from master.sys.sysdatabases"):
            print db[0]
        print ''
        self._database_name = raw_input("\nChoose a database to use: ")
        self._conn_str = 'mssql://WIN-2TMF2VILQ8A/{0}?trusted_connection=yes'.format(self._database_name)
        self._engine = sqlalchemy.create_engine(self._conn_str)
        self._conn = self._engine.raw_connection()

    def Creator(self, debug=False):
        
        """
        Executes the Creation query that drops [Video Views]
        if it exists, then creates a new table called 
        [Video Views]. This table is populated with the
        accesses from the relevant semester database.
        """
        _Create_Video_View_Table_Query = """
        
        SET NOCOUNT ON

        /****** Object:  Table [dbo].[Video Views]    Script Date: 2/27/2015 10:21:52 AM ******/
        SET ANSI_NULLS ON

        SET QUOTED_IDENTIFIER ON

        SET ANSI_PADDING ON

        /****** Script for Dropping [Video Views] if it exists  ******/
        IF OBJECT_ID('[dbo].[Video Views]', 'U') IS NOT NULL
	        DROP TABLE [dbo].[Video Views]


        CREATE TABLE [dbo].[Video Views](
	        [Video Order] int NULL,
	        [Title] varchar(max) NULL,
	        [Video Length (s)] float NULL,
	        [Lab Number] int NULL,
	        [session_user_id] varchar(max) NULL,
	        [Submission Date] date NULL
        ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

        SET ANSI_PADDING OFF


        /****** Script for Create Table Variable for video order ******/
        declare @vidorder table (original_item_id int, video_order int)

        insert into @vidorder
        SELECT distinct original_item_id
        , video_order
            FROM [fall_2013_blended].[dbo].[SY_lec_submission_metadata_161students_78videos]

        /****** Script for shape Data for Video Views table and INSERT  ******/
        INSERT INTO [Video Views]
        SELECT vidorder.video_order
        , meta.title_mooc
        , meta.video_length_SY
        ,meta.Lab_number
        , data.session_user_id
        , cast(dateadd(ss, data.submission_time, '1970-01-01') as date) [submission date]
            FROM {0}.[dbo].[lecture_submission_metadata] data
            join [fall_2013_blended].[dbo].[SY_published_lecture_metadata_combined] meta
            on meta.id_blended = data.item_id
            join [dbo].[users] u
            on u.session_user_id = data.session_user_id
            join @vidorder vidorder
            on vidorder.original_item_id = meta.id_blended
            where u.access_group_id = 4

        """.format('[' + str(self._database_name) + ']')

        if debug == True:
            print Create_Video_View_Table_Query
            print ''
            print ''

        self._conn.execute(_Create_Video_View_Table_Query)
        self._conn.commit()

    def CreateVideoViewTable(self):

        """
        Checks if the table [Video Views] exists,
        if it does prompts the user to continue.
        If it doesn't it immediately executes
        Creator().

        This is to keep people from doing something
        they don't know about. It probably won't
        work.
        """

        if self._engine.has_table(u'Video Views') is True:
            print "First time operations have already been performed.\n"
            
            if raw_input("Would you like to continue first time operations? (y/n) ") == "y":
                self.Creator()
                
                print "\nFirst time operations have been repeated.\n"
            
            else:
                print "\nGoodbye.\n"
    
        else:
            self.Creator()
            print "\nFirst time operations have been completed.\n"
            print "\nGoodbye.\n"
            
if __name__ == "__main__":
    v = VideoViewTable('spring_2014_blended')
    v.CreateVideoViewTable()
