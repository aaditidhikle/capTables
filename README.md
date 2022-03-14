# capTables

Introduction:
We help companies manage and understand ownership. Corporations represent ownership on a ledger called a capitalization table, or “cap table” for short. This table lists each of the company’s shareholders (investors, employees, and advisors), the number of shares they own, the price they paid to purchase them, and their ownership percentage. Keeping a cap table accurate and up to date is a challenging problem, and most cap tables are broken as a result.
When a company grants an equity award (shares) to an employee, it usually has to vest before you can do anything with it. This vesting usually occurs in increments over a period of time, encouraging recipients to stay longer at the company. A vesting schedule defines how much total equity has been vested over a time.
In this exercise, you will generate a cumulative vesting schedule from a series of individual vesting events.


Design:

1) Have tried to make the system READ efficient. This was a conscious decision which makes the write process longer.
2) For future improvements, this system can be set up as CQRS where writes happen through a pub sub mechanism.


Employee Map: is a dictionary collection of Employee objects. These objects hold employ name, id information. As well as a set of Equity awards awarded to the employee.

Equity Event Map: contains all events of type EquityEvent mapped to a unique AwardID. 

Object oriented feautures:
1) Seperation of concerns
2) Single resposibility
3) Encapsulation : by using getters and setters for private variables
4) Information hiding
5) Inheritance: extensibility, code reuseability, data hiding

Future improvements:
1) CQRS
2) Store data in a DB.
3) Stronger data validation through pandas library.
4) Polymorphism can be implemented to differentiate implementation of methods for different types of shareholders.


Code Styling guidelines: PEP8 and Google Python Style Guide


