# capTables

Introduction:
We help companies manage and understand ownership. Corporations represent ownership on a ledger called a capitalization table, or “cap table” for short. This table lists each of the company’s shareholders (investors, employees, and advisors), the number of shares they own, the price they paid to purchase them, and their ownership percentage. Keeping a cap table accurate and up to date is a challenging problem, and most cap tables are broken as a result.
When a company grants an equity award (shares) to an employee, it usually has to vest before you can do anything with it. This vesting usually occurs in increments over a period of time, encouraging recipients to stay longer at the company. A vesting schedule defines how much total equity has been vested over a time.
In this exercise, you will generate a cumulative vesting schedule from a series of individual vesting events.


Design:

csv --------> Employee Map
      |
      ------> Equity Event Map

Employee Map: is a dictionary collection of Employee objects. These objects hold employ name, id information. As well as a set of Equity awards awarded to the employee.

Equity Event Map: contains all events of type EquityEvent mapped to a unique AwardID. 
