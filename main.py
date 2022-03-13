# coding=utf-8
import csv
import collections
from datetime import datetime

DT_FORMAT = '%Y-%m-%d'


class Employee:
    """ Represents an Employee entity with attributes such as name, id, list of equity awarded so far

        Attributes
        ----------
        employee_name : str
            Employee First + Last Name
        employee_id : str
            Unique Identifier starts with E
        equityAwards : set
            List of unique award Ids eg. ISO-001, IS0-002

    """
    def __init__(self, employee_name, employee_id):
        self.employeeName = employee_name
        self.employeeID = employee_id
        self.equityAwards = set()

    def add_equity_award(self, award_id):
        """Setter Method to add a new award id"""
        self.equityAwards.add(award_id)
        return

    def get_equity_awards(self):
        """Getter method for returning equity awards list"""
        return self.equityAwards


class EquityEvent:
    """Represents an Equity Event of type Vest/Cancel on a given date for certain quantity

        Attributes
        ----------
        awardId : str
            Unique Award ID for every new equity awarded to the employee
        eventDate : date
            Date of equity vesting or cancelling
        awardQty : decimal/int
            quantity getting vested/cancelled
        eventType: str
            VEST or CANCEL
    """
    def __init__(self, award_id, event_date, award_qty, event_type):
        self.awardId = award_id
        self.eventDate = event_date
        self.awardQty = award_qty
        self.eventType = event_type


class CapitalizationTable:
    """A class that parses raw equity events, maintains an employee map and an equity event map
        Attributes
        ----------
        employee_map : hashmap/dictionary
            Map of employee ids mapped to an employee obj that contains employee info alongwith equity IDs
            of equity awarded to them so far
        equity_event_map : defaultdict
            Map of all events pivoted by award id (eq. ISO-001)
    """
    def __init__(self):
        self.employee_map = dict()
        self.equity_event_map = collections.defaultdict(lambda: [])

    def parse_csv(self, file_path):
        """ Parses raw csv events and adds data into Employee dictionary and equity_event dictionary"""
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if not row:
                    continue
                event_type = row[0]
                employee_id = row[1]
                employee_name = row[2]
                award_id = row[3]
                event_date = datetime.strptime(row[4], DT_FORMAT).date()
                award_qty = int(row[5])

                #add data into employee table
                self.update_employee_map(employee_name, employee_id, award_id)
                #add data into equity event table
                self.update_equity_event_map(award_id, event_date, award_qty, event_type)
        return

    def update_employee_map(self, employee_name, employee_id, award_id):
        """Create or update an existing Employee object with new award id"""
        if employee_id in self.employee_map:
            emp = self.employee_map[employee_id]
            emp.add_equity_award(award_id)
        else:
            emp = Employee(employee_name, employee_id)
            emp.add_equity_award(award_id)
            self.employee_map[employee_id] = emp
        return

    def update_equity_event_map(self, award_id, event_date, award_qty, event_type):
        """Add Equity event to Equity Event Map"""
        equity_event = EquityEvent(award_id, event_date, award_qty, event_type)
        self.equity_event_map[award_id].append(equity_event)
        return

    def get_employee_vesting_status(self, as_of_date, employee_id, employee):
        """ Get vesting status for a single individual"""
        vesting_schedule = []
        equity_awards = employee.get_equity_awards()
        for equityAward in equity_awards:
            print(employee_id, equityAward)
            equity_events = self.equity_event_map[equityAward]
            total_qty = 0
            for event in equity_events:
                if event.eventDate > as_of_date:
                    continue
                if event.eventType == 'VEST':
                    total_qty += event.awardQty
                elif event.eventType == 'CANCEL':
                    total_qty -= event.awardQty
            vesting_schedule.append([employee_id, employee.employeeName, equityAward, total_qty])
        return vesting_schedule

    def get_all_employee_vesting_status(self, as_of_date):
        """Get vesting status as of a given date for all employees in the employee map"""
        vesting_schedule = []
        for employeeId, employee in self.employee_map.items():
            employee_vesting_status = self.get_employee_vesting_status(as_of_date, employeeId, employee)
            vesting_schedule += employee_vesting_status
        return vesting_schedule


if __name__ == '__main__':
    csv_path = '/Users/aaditidhikle/PycharmProjects/CapTable/example1.csv'
    target_date = datetime.strptime('2020-04-01', DT_FORMAT).date()
    capTable = CapitalizationTable()
    capTable.parse_csv(csv_path)
    print(capTable.get_all_employee_vesting_status(target_date))
