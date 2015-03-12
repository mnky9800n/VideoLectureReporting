
## TODO
## 1) make this work for any database.
##
## 2) check for [Video Views] in active db
##
## 3) build each graph separately
##
## 4) create new branch for this

def do():
    import pandas as pd
    import numpy as np
    import sqlalchemy
    import matplotlib.pyplot as plt
    from GraphingUtilities import GraphingUtilities
    from DatabaseConnection import DatabaseConnection

    GU = GraphingUtilities()
    db = DatabaseConnection()


    engine = sqlalchemy.create_engine('mssql://WIN-2TMF2VILQ8A/spring_2014_blended?trusted_connection=yes')

    Spring_data = pd.read_sql("SELECT * FROM [Video Views]", engine)

    def get_pivot_date_range(dataframe, semester_day_count):
        """
        We need a full date range for the pivot 
        table in SQL to create the date columns.
    
        NOTE: the date range is truncated based
        on the semester days. This is due to
        students sometimes watching videos much
        later than the end of the semester.
        """

        daterange = '('
        for d in pd.date_range(dataframe['Submission Date'].min(), dataframe['Submission Date'].max()):
            daterange += '[' + str(d).split(' ')[0] + '],'
    
        return daterange[:semester_day_count*13] +')'

    def pivot_query(labs):
        """
        Videos have a 'Lab Number' designation.
        Videos with (Lab Number = -1) are not
        associated with a lab and generally
        referred to as 'Lecture Videos'. Videos
        with (Lab Number > -1) are either associated
        with lab practices (Lab Number == 0) or with 
        specific labs (Lab Number == [1,2,3,4]) where
        the number indicates the specific lab.
        """
    
        query = """
        SET NOCOUNT ON
        select *
        from
        (
        SELECT [Submission Date]
        , [session_user_id]
          FROM [spring_2014_blended].[dbo].[Video Views]
          WHERE [Lab Number] {0}
        ) as srctable
        PIVOT
        (
        count([Submission Date])
        FOR [Submission Date] in {1}
        ) as pivottable""".format(labs, get_pivot_date_range(Spring_data, 119))
        return query




    # Get Data, create single dataframe
    Spring_Date_pivot_labs = pd.read_sql(pivot_query('=-1'), engine).transpose()[1:119].transpose()
    Spring_Date_pivot_lect = pd.read_sql(pivot_query('>-1'), engine).transpose()[1:119].transpose()
    Spring_timeline = pd.DataFrame({'Lecture':Spring_Date_pivot_labs.sum()
                                    ,'Laboratory':Spring_Date_pivot_lect.sum()})
    def get_xlabels(weeks):
        """
        generates x labels for the
        number of weeks in the 
        semester.
        """
    
        x = []
        for n,i in enumerate(np.zeros(weeks*7)):
            if n%7==0:
                x.append('week '+str(int(n/7.0+1)))
            else:
                x.append('')
    
        return x

    x = get_xlabels(15)

    def savefigure(figureobj, name, filetype='.png'):
        fig = figureobj #plt.gcf()
        #fig.savefig('/images/'+name)
        fig.savefig("C:\Users\Administrator\Google Drive\code learning\VideoLectureReporting\VideoLectureReporting\images\\" + name + filetype)
    

    # plot video accesses
    timeline_df = Spring_timeline[1:]

    # get total number of videos accessed
    N_video = timeline_df.sum()[0]+timeline_df.sum()[1]

    ax = timeline_df.plot(kind='bar', figsize=(18,5), color=('crimson','0.75'), grid=False, width=1.0, edgecolor='white')
    fig = ax.get_figure()
    ax.set_xticklabels(x)
    ax.set_title(r'Fall 2013 Video Accesses ($N_{Accesses}$='+str(N_video)+')')
    ax.set_ylabel('N Accesses')
    #ax.plot(labs, 'v', markersize=50, color='yellow')
    ax.legend( loc='upper right')
    #ax.plot(exams, 'v', markersize=25, color='black')

    #ax.set_ylim(0,600)
    #ax.text(54.5, 50, 'Fall\nBreak', bbox={'facecolor':'white', 'alpha':1.0, 'pad':5})
    ax.set_title(r'Fall 2013 Video Accesses ($N_{Accesses}$='+str(int(N_video))+')')
    ax.set_ylabel('N Accesses')
    savefigure(plt.gcf(),'timeline')#,'.svg')
    plt.close(fig)


    # In[5]:

    Spring_data = pd.read_sql("SELECT * FROM [Video Views]", engine)
    lect = (1,4,5,6,7,8,9,10,11,13,14,21
            ,22,23,24,25,26,27,29,30,31
            ,32,33,34,35,36,37,38,39,40
            ,43,44,45,46,47,48,49,50,51,
            52,55,56,57,58,59,60,61,62,63
            ,64,65,66,67,68,69,70,71,72,73
            ,74,75,76,77,78)
    labs = (2,3,17,18,19,20,12,15,16,28,41,42,53,54)

    color = ['0.75' for n in range(1,79)]

    for l in labs:
        color[l-1] = 'crimson'
    #####
    # Count by video order
    #####
    #
    # These are equivalent queries
    # the SQL query is more readable so I have 
    # included it as documentation
    #
    #""" ****** Calculating the fraction of the class who watched the video ******
    #SELECT [Video Order]
    #, count(distinct session_user_id)*1.0/367
    #  FROM [spring_2014_blended].[dbo].[Video Views]
    #  group by [Video Order]
    #"""

    cnt_by_video_order = pd.DataFrame({'Count':Spring_data.groupby('Video Order').size()
                                       ,'Fraction':Spring_data.groupby('Video Order').session_user_id.nunique()/367})

    # Plot the figure

    fig = plt.figure(figsize=(32,10))
    fig.subplots_adjust(hspace=0)

    plt.subplot(2,1,1)
    ax1 = cnt_by_video_order['Count'].plot(kind='bar'
                                           , sharex=True
                                           , color=color
                                           , grid=False
                                           , figsize=[32,10]
                                           , fontsize=25
                                           , edgecolor='white')
    ax1.set_title('Video Accesses', fontsize=25)
    ax1.set_xticklabels([])
    ax1.set_xlabel('Videos in Assigned Order (78 videos)', fontsize=25)
    ax1.set_ylabel('N Accesses', fontsize=25)

    plt.subplot(2,1,2)
    ax2 = cnt_by_video_order['Fraction'].plot(kind='bar'
                                           , sharex=True
                                           , color=color
                                           , grid=False
                                           , figsize=[32,10]
                                           , fontsize=25
                                           , edgecolor='white')
    ax2.set_xticklabels([])
    ax2.set_xlabel('Videos in Assigned Order (78 videos)', fontsize=25)
    ax2.set_ylabel('Fraction of Class Accessing', fontsize=20)

    savefigure(plt.gcf(),'fractionAccessing')#,'.svg')
    plt.close()

    # In[59]:

    """
    This query counts the number of accesses,
    the number of unique accesses, and splits
    the counts based on lab videos and lecture
    videos. It then unions this data to the data
    for students who watched zero videos in the
    video type (lab or lecture).
    """

    query = """
    SET NOCOUNT ON

    /****** create table variables to store queries ******/
    declare @cnt_lect table (id varchar(max), cnt int)
    declare @cnt_labs table (id varchar(max), cnt int)
    declare @cnt_unq_lect table (id varchar(max), cnt int)
    declare @cnt_unq_labs table (id varchar(max), cnt int)

    /****** count number of accesses of lecture videos ******/
    insert into @cnt_lect
    SELECT session_user_id
    , count(v.Title)
      FROM [spring_2014_blended].[dbo].[Video Views] v
      where [Lab Number] = -1
      group by session_user_id

    /****** count number of accesses of laboratory videos ******/
    insert into @cnt_labs
    SELECT session_user_id
    , count(v.Title)
      FROM [spring_2014_blended].[dbo].[Video Views] v
      where [Lab Number] > -1
      group by session_user_id

    /****** count number of distinct accesses of lecture videos ******/
    insert into @cnt_unq_lect
    SELECT session_user_id
    , count(distinct v.Title)
      FROM [spring_2014_blended].[dbo].[Video Views] v
      where [Lab Number] = -1
      group by session_user_id

    /****** count number of distinct accesses of laboratory videos ******/
    insert into @cnt_unq_labs
    SELECT session_user_id
    , count(distinct v.Title)
      FROM [spring_2014_blended].[dbo].[Video Views] v
      where [Lab Number] > -1
      group by session_user_id




    /****** ALL USERS ******/
    declare @all_users table (id varchar(max))
    insert into @all_users
    select distinct session_user_id
    from [Video Views]

    /****** EXCEPT USERS OF LECTURES ******/
    declare @no_lectures table (id varchar(max))
    insert into @no_lectures
    select *
    from @all_users

    EXCEPT

    select distinct session_user_id
    from [Video Views]
    where [Lab Number] = -1

    /****** USERS OF LABS ******/
    declare @no_labs table (id varchar(max))
    insert into @no_labs
    select *
    from @all_users

    EXCEPT

    select distinct session_user_id
    from [Video Views]
    where [Lab Number] > -1


    /****** select all count data for all students ******/

    select session_user_id
    , 0 cnt_labs
    , count(v.title) cnt_lect
    , 0 cnt_unq_labs
    , count(distinct v.title) cnt_unq_lect
    from [Video Views] v
    where v.session_user_id in (
    select *
    from @no_labs)
    group by session_user_id

    UNION

    select session_user_id
    , count(v.title) cnt_labs
    , 0 cnt_lect
    , count(distinct v.title) cnt_unq_labs
    , 0 cnt_unq_lect
    from [Video Views] v
    where v.session_user_id in (
    select *
    from @no_lectures)
    group by session_user_id


    UNION

      select cnt_labs.id
      , cnt_labs.cnt cnt_labs
      , cnt_lect.cnt cnt_lect
      , cnt_unq_labs.cnt cnt_unq_labs
      , cnt_unq_lect.cnt cnt_unq_lect
      from @cnt_lect cnt_lect
      join @cnt_labs cnt_labs
      on cnt_lect.id = cnt_labs.id
      join @cnt_unq_lect cnt_unq_lect
      on cnt_lect.id = cnt_unq_lect.id
      join @cnt_unq_labs cnt_unq_labs
      on cnt_lect.id = cnt_unq_labs.id
    """

    # get data
    cnt_unq_df = pd.read_sql(query, engine)
    cnt_unq_df = cnt_unq_df.set_index('session_user_id')
    cnt_unq_df.columns = ('Count Accesses - Laboratory'
                          , 'Count Accesses - Lecture'
                          , 'Unique Accesses - Laboratory'
                          , 'Unique Accesses - Lecture')

    # Using the raw data from the query, we get fractions and densities for the graph 
    cnt_unq_df['Unique Access Fraction - Lecture'] = cnt_unq_df['Unique Accesses - Lecture']/cnt_unq_df['Unique Accesses - Lecture'].max()
    cnt_unq_df['Unique Access Fraction - Laboratory'] = cnt_unq_df['Unique Accesses - Laboratory']/cnt_unq_df['Unique Accesses - Laboratory'].max()
    cnt_unq_df['Count Access Density - Lecture'] = cnt_unq_df['Count Accesses - Lecture']/64.0
    cnt_unq_df['Count Access Density - Laboratory'] = cnt_unq_df['Count Accesses - Laboratory']/14.0


    #####
    # Plot the figure
    #####

    plt.rcParams['figure.figsize'] = (15,15)

    fig = plt.figure()

    weights = np.ones_like(range(367))/367.0


    plt.subplot(2,2,1)
    ax = cnt_unq_df['Count Access Density - Lecture'].hist(range=(0,7), bins=28, weights=weights, color='0.75',edgecolor='white')
    ax.set_title('Count Access Density - Lecture (64 videos)')
    ax.set_xlim(0,7)
    ax.set_ylim(0,0.2)
    ax.set_ylabel(r'Class Fraction (N='+str(cnt_unq_df.shape[0])+')')
    ax.set_xlabel(r'Access Density (N='+str(cnt_unq_df['Count Accesses - Lecture'].sum())
                  +', Access AVG=' + str(round(cnt_unq_df.mean()[6],2)) +')')


    plt.subplot(2,2,2)
    ax = cnt_unq_df['Count Access Density - Laboratory'].hist(range=(0,7), bins=28, weights=weights, color='crimson',edgecolor='white')
    ax.set_title('Count Access Density - Laboratory (14 videos)')
    ax.set_xlim(0,7)
    ax.set_ylim(0,0.2)
    ax.set_ylabel(r'Class Fraction (N='+str(cnt_unq_df.shape[0])+')')
    ax.set_xlabel(r'Access Density (N='+str(cnt_unq_df['Count Accesses - Laboratory'].sum())
                                +', Access AVG=' + str(round(cnt_unq_df.mean()[7],2)) +')')
    plt.subplot(2,2,3)
    ax = cnt_unq_df['Unique Access Fraction - Lecture'].hist(range=(0,1), bins=10, weights=weights, color='0.75',edgecolor='white')
    ax.set_title('Lecture Access Fraction (64 Videos)')
    ax.set_ylim(0,1)
    ax.set_xlim(0,1)
    ax.set_ylabel(r'Class Fraction (N='+str(cnt_unq_df.shape[0])+')')
    ax.set_xlabel(r'Access Fraction (N='+str(cnt_unq_df['Count Accesses - Lecture'].sum())+')')

    plt.subplot(2,2,4)
    ax = cnt_unq_df['Unique Access Fraction - Laboratory'].hist(range=(0,1), bins=10, weights=weights, color='crimson',edgecolor='white')
    ax.set_title('Laboratory Access Fraction (14 Videos)')
    ax.set_ylim(0,1)
    ax.set_xlim(0,1)
    ax.set_ylabel(r'Class Fraction (N='+str(cnt_unq_df.shape[0])+')')
    ax.set_xlabel(r'Access Fraction (N='+str(cnt_unq_df['Count Accesses - Laboratory'].sum())+')')

    savefigure(plt.gcf(),'fourbyfour')#,'.svg')
    plt.close()

    # In[312]:

    def get_video_order_range():
        """
        SQL Server does not support dynamic
        pivots in a straight forward way. This
        function creates the list of video
        column names for the pivot.
        """
    
        videoOrder = '('
        for n in range(1,79):
            videoOrder += '[' + str(n) + '],'

        videoOrder = videoOrder[:-1]+')'
        return videoOrder


    query = """
    SET NOCOUNT ON
    select *
    from
    (
    SELECT distinct [session_user_id]
    , [Video Order]
      FROM [spring_2014_blended].[dbo].[Video Views]
    ) as srctable
    PIVOT
    (
    count([Video Order])
    FOR [Video Order] in {0}
    ) as pivottable""".format(get_video_order_range())
    videoOrderHM = pd.read_sql(query, engine)
    videoOrderHM = videoOrderHM.set_index('session_user_id')

    videoOrderHM['Count'] = videoOrderHM.transpose().sum()
    videoOrderHM = videoOrderHM.sort('Count')
    cols_a = videoOrderHM[videoOrderHM.columns - ['Count',]].columns
    data_a = videoOrderHM[[str(c) for c in sorted([int(c) for c in cols_a])]].values
    from matplotlib import colors

    fig = plt.figure(figsize=(12,12))


    p = plt.pcolor(data_a, cmap='gray_r')

    plt.xlim(0,78)
    plt.ylim(0,videoOrderHM.count()[0])

    plt.xlabel('Video Order')
    plt.ylabel('Student ID')
    plt.title('Student Unique Access')

    ####### uncomment here to add lab markers
    #######
    #for l in labs:
    #    plt.plot([l-0.5]*2, [159, 159], marker='v', linestyle='', color='white', markersize=16)
    #    plt.plot([l-0.5]*2, [2, 2], marker='^', linestyle='', color='white', markersize=16)
 
    plt.bar([0],[0],color='black')
    plt.bar([0],[0],color='white')
    plt.legend(['Access', 'No Access'], loc='lower right')

    savefigure(plt.gcf(),'binarymap')#,'.svg')
    plt.close()


    # In[212]:

    #####
    # Heat map of unique accesses
    #####

    query = """
    SET NOCOUNT ON
    select *
    from
    (
    SELECT [Submission Date]
    , [Video Order]
      FROM [spring_2014_blended].[dbo].[Video Views]
    ) as srctable
    PIVOT
    (
    count([Submission Date])
    FOR [Submission Date] in {0}
    ) as pivottable""".format(get_pivot_date_range(Spring_data, 119))

    Spring_views = pd.read_sql(query, engine)
    Spring_views = Spring_views.set_index('Video Order')
    from matplotlib.colors import LogNorm
    plt.rcParams['figure.figsize'] = (15,8)

    plt.imshow(Spring_views
                , cmap='gnuplot'
                , interpolation='nearest'
                ,origin='lower'
                ,norm=LogNorm())
    plt.ylim(0,78)
    plt.xlim(0,116)
    plt.xlabel('Semester Timeline')
    plt.ylabel('Videos in Assigned Order')
    plt.title('Video Accesses Per Video For Semester (log-scale)')
    plt.xticks(np.arange(0,117,7))
    plt.gca().set_xticklabels(['week '+str(n) for n in range(1,16)], rotation=90)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Access Count')

    #labn = pervid_time[pervid_time['Lab_number'] > -1]['Lab_number'].index

    #plt.plot(np.zeros_like(labn), labn, marker='>', markersize=25, linestyle='')

    # plot the midterm date
    #plt.plot((63,)*2, [0,78], linewidth=5, linestyle='--', color='red')

    # plot the lab due dates
    #labs = [19,35,47,68,96]
    #for l in labs:
    #    plt.plot((l,)*2, (0,)*2, marker='^', markersize=30, color='yellow', linestyle='')

    #plt.legend(['Lab Video', 'Midterm Exam', 'Lab Due Date'], loc='upper left')#,bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    savefigure(plt.gcf(),'heatmap')#,'.svg')


if __name__ == "__main__":
    do()