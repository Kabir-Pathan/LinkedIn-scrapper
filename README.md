LinkedIn scrapper

Process of 'linkedin.py'

This is an online scrapper made using selenium automation software in python with the help of SQL. 
The first step is to log into company server. After logging into the server the program gets a list of company URLs already stored in the database. This is done with use of MSSQL.
The next step is to log into a LinkedIn premium account provided by company. This is done using Selenium.
The URLs found are tested and if a valid one is found it is entered into google and the company site is opened.
Next step is to find a LinkedIn link on the website. Selenium software is used for this step, it scrolls through the home page, if it is not found there program searches for a 'contact' page or 'about' page on company website.
'Contact' page and 'about' page is also scrapped through and if no LinkedIn URL is found it breaks and goes to next URL.
If a LinkedIn page is found it opens the found page. It then opens the 'People' page on LinkedIn for the company we are currently processing.
After reaching the people page company data is gathered. It scrolls through people's profile cards and starts recording info. 
After a person is found it starts the next step of the process which is in the next file 'mail_tester.py'

Process of 'mail_tester.py'

After receiving the first and last name this file starts creating possible mail combinations and finds one that is valid.
10 combinations have been added and it tests each one of them to find a valid one.
If none are valid then it goes to next person.
If a valid email is found it needs to be entered into the company database.
Two functions are created to generate a unique ID and the other one for getting the time at that moment.
These are just requirements to enter the data into the company database.
Now that we have everything we can input new data.
Unique ID, First name, email and current time are inputted into the company database.
