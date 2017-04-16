# A Happy Union
#### Writeup by intelagent

* **Web**
* *110 points*
* I really need access to [website](http://shell2017.picoctf.com:41558/), but I forgot my password and there is no reset. Can you help? I like lite sql :)


Upon entering the website we are asked to login or register. After registering with any name and logging in, we can figure out that the site is querying based upon our username. We only see posts made by ourselves. 

Using this information the query probably looks something like this: 

`select * from TABlE_NAME where username = 'OUR_USERNAME'`

Knowing this we can view all posts! 

If we change OUR_USERNAME to `' or 1=1 -- ` it would return all the rows in the database and print our flag! Two dashes (--) is a comment in SQLite.

Hmm... It did show all the current posts but the flag wasn't included. Maybe the flag is the admin's password?

To begin querying for the admin password we need to know all the table and column names. A very nice way of doing this is using the `UNION` command as the problem title suggests.

`UNION` gets information from multiple tables and combines it into one result. The only caveat of using `UNION` is that both queries – on either side of the `UNION` – must be returning the same number of columns. 

To begin testing we can make our username equal to `' union select 1,2 -- `. After logging in we receive an error and the sql query that ran! 

`select id, user, post from posts where user = '' union select 1,2 -- ';`

This error occured because the query on the right (`union select 1,2 --`) returned two columns (1,2) while the query on the left returned a different amount. 

After registeting and loggin in with `' union select 1,2,3 -- ` we are no longer greeted with a error. Now instead of selecting arbitrary numbers let's select the admin's username and password.

The query to do so will look like this:

`' union select `. Oh crap what are the column names we are supposed to select? 

We can get all the information about the database in just one query.

`' union select 1,name,sql from sqlite_master --`

This query tells us there is a table called users with the columns name and pass. 

Great, now let's finish writing the query we started before:

`' union select 1,user,pass from users -- `

We still need to select an arbitrary 1 in order to return 3 columns.

The original query plus our crafted injection looks like this:

`select id, user, post from posts where user = '' union select 1,user,pass from users -- `.

Bam. After logging in with the username `' union select 1,user,pass from users -- ` we are greeted with the flag:

flag{union?_why_not_onion_b6e6a3cd8e3f1fe5f6109d1618bddbd1}	
