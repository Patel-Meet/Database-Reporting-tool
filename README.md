# News Database Reporting tool
> BY- MEET PATEL

## About
This project interacts with a live database both by the command line and by the python code. The project deals with a very large database with over one and a half million rows of logs. It uses complex PostgreSQL queries, and generates a report to draw business conclusions from the data.

### Set up:
## Necessary installation:
* Python
* Vagrant
* VirtualBox
* PostgreSQL

## Installation steps:
* Install VirtualBox.
* Install Vagrant.
* Clone this repo, unzip `newsdata.zip` and move all the contents to the vagrant folder i.e. the shared folder.
* In the command line go to the vagrant folder and type `vagrant up` then type `vagrant ssh` to log into the virtual machine.

## Running the project:
* Go to the shared vagrant folder by typing `cd /vagrant`.
* Then Type `psql -d news -f newsdata.sql`
* Running the previous command will connect to your installed database and execute the SQL queries in `newsdata.sql` and creates the table and populates it with data.
* type the command `python newsdata.py`
* Wait for the Queries to execute.
* After the program finishes executing, open news_report.txt.

## The queries answered in news_report.txt
* Query 1, What are the most popular three articles of all time?
* Query 2, Who are the most popular article authors of all time?
* Query 3, On which days did more than 1%  of requests lead to errors?
  - This Query uses the following View named ERROR_PCT.
  ```CREATE VIEW ERROR_PCT AS
     WITH error_per_day AS (
     SELECT date(time) AS day, count(*) AS errorpd
     FROM log WHERE status LIKE '%4%' OR status LIKE '%5%'
     GROUP BY date(time)
     ),
     total_per_day AS (
     SELECT date(time) AS dayt, count(*) AS total
     FROM log
     GROUP BY date(time)
     )
     SELECT day, round(errorpd*100.0/total, 2) AS pct
     FROM error_per_day, total_per_day
     WHERE day=dayt AND errorpd*100.0/total >1.0;
  ```

### **EXTRA CREDIT**
* Query 4, What is the average load of the website per day?
  - This Query finds the average number of visitors per day so it is easy to track the websites' popularity.
* Query 5, What is the best time to do website maintenance?
  - This Query finds the hour of the day when the least amount of HTTP requests are received by the website, therefore suggesting the best time to do website maintenance.
  
** Below is the snapshot of the ouptut file
![Image of output](https://github.com/Patel-Meet/Database-Reporting-tool/blob/master/Capture.PNG)
