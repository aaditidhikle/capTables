# capTables

Design Decisions:

1) Capitalization Table is broken into 2 normalized tables: Employee and EquityEvent
      Employee Map: is a dictionary collection of Employee objects. These objects hold employ name, id information. As well as a set of Equity awards awarded to the employee.
      Equity Event Map: contains all events of type EquityEvent mapped to a unique AwardID. 
    
   This decision was made to maintain a good balance between normalized data and a READ efficient system.
   
   * The reason to maintain normalized data in the 2 tables/hashmaps/dictionaries is that this provides for extensability into a future storage-based solution where state of data can be maintained for even higher read efficiency. Another reason was to eliminate redundancies. As we gather more information about other types of shareholders, each type can have their own tables (as related attributes of each shareholder may vary). Where as, EquityEvent table can be allowed to scale up easily as it will hold information of all equity events for all types of shareholders.
   
   * Another reason for maintaining 2 tables was to prime the data so that the 2 tables could extend themselves to many possible queries.

2) In order to make the system READ efficient, the compromise was to have the write process do the heavy lifting of appropriately segregating data into the 2 dictionaries. 

3) As the problem statement mentions that Employees are a type of Shareholders, we have a Shareholder class that will be the parent class from which classes like Employee (and Investors/Advisors in future) can inherit from

4) Certain sensitive information like "equity_award_id" list that is stored for every Shareholder has been privatized and encapsulated with the help of getters and setters.


Object oriented feautures implemented:
1) Seperation of concerns
2) Single resposibility
3) Encapsulation : by using getters and setters for private variables
4) Inheritance: extensibility, code reuseability, Information hiding

Future improvements:
1) Store information into a storage based solution where vesting schudule could be precomputed and maintained for an efficient read.
2) This system can be set up as CQRS architecture pattern( Command and Query Responsibility seggregation) where writes happen through a pub-sub mechanism into a Write DB(Event Sourcing) and reads happen on a ReadDB( materialized view of write DB) and there is eventual consistency between the 2 DBs.
3) Store data in a DB and add indices on primary keys like Employee ID/ShareHolderID and AwardID
4) Robust data validation through pandas library.
5) Polymorphism can be implemented to differentiate implementation of methods for different types of shareholders.


Code Styling guidelines followed: PEP8 and Google Python Style Guide

To run the code:
> python3 main.py example1.csv 1


