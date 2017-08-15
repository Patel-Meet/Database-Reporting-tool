#!/usr/bin/env python
'''This Code accesses news database and query's it to generate
   a report which draws business conclusions from the data
'''
import psycopg2


'''
   This function takes a query as parameter, uses that query to access
   the database and returns the result
'''


def execute_query(query):
    conn = psycopg2.connect("dbname = news")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


'''
   This function takes query result and query title as parameter and
   prints it to a text file names 'newsdata.txt' to generate the report.
'''


def print_query(results, Query_title, Query_no):
    txtfile = open('news_report.txt', 'a')
    txtfile.write(Query_title)
    txtfile.write('\n')
    if Query_no == 1:
        for result in results:
            txtfile.write(
                '   "{}" -- {} Views\n' .format(result[0], result[1]))
    elif Query_no == 2:
        for result in results:
            txtfile.write('   {} -- {} Views\n' .format(result[0], result[1]))
    elif Query_no == 3:
        for result in results:
            txtfile.write(
                '   {} -- {}% ERROR \n' .format(result[0], result[1]))
    elif Query_no == 4:
        for result in results:
            txtfile.write(
                '   Average Views per day is -- {} Views\n' .format(result[0]))
    elif Query_no == 5:
        for result in results:
            txtfile.write(
                '   The best time for maintenance is at {}\n' .format(result[0]))
    else:
        print(results)
    txtfile.write('\n' '\n')
    txtfile.close()


# below are the queries which needs to be processed
Query1_title = "1. What are the most popular three articles of all time?"
Query1 = ''' SELECT A.title, COUNT(*) AS views
             FROM articles A, log L
             WHERE L.path LIKE concat('%', A.slug)
             GROUP BY A.title
             ORDER BY views DESC LIMIT 3;
         '''
Query2_title = "2. Who are the most popular article authors of all time?"
Query2 = '''SELECT A.name, COUNT(*) as views
            FROM articles AR, authors A, log L
            WHERE A.id = AR.author AND L.path LIKE concat('%', AR.slug)
            GROUP BY A.name
            ORDER BY views DESC;
         '''
Query3_title = "3. On which days did more than 1%  of requests lead to errors?"
# ERROR_PCT is a view, for more details please refer to the ReadMe
Query3 = '''SELECT * FROM ERROR_PCT;
         '''
#  THE FOLLOWING TWO QUERIES ARE DONE AS EXTRA CREDIT ###
Query4_title = "4. What is the average load of the website per day?"
Query4 = '''SELECT CAST(AVG(Nested.total) as INTEGER) AS Average_per_day
            FROM (SELECT count(*) AS total
                      FROM log L
                      GROUP BY EXTRACT(DAY FROM L.time)
                 ) AS Nested;
         '''
Query5_title = "5. What is the best time to do website maintenance?"
Query5 = '''SELECT CONCAT(EXTRACT(HOUR FROM L.time), ':00:00') AS Maintainance_Time
            FROM log L
            GROUP BY Maintainance_Time
            ORDER BY COUNT(*) LIMIT 1;
         '''


'''
   This function creates the report by calling all the other functions
'''


def create_report():
    print ("Please wait for the queries to execute.")
    print_query(execute_query(Query1), Query1_title, 1)
    print_query(execute_query(Query2), Query2_title, 2)
    print_query(execute_query(Query3), Query3_title, 3)
    print_query(execute_query(Query4), Query4_title, 4)
    print_query(execute_query(Query5), Query5_title, 5)
    print ("Thank you for waiting, the results are in news_report.txt.")


# The main function call to create the report
create_report()
