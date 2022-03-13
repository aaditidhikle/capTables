# coding=utf-8
import csv
import collections
from datetime import datetime

DT_FORMAT = '%Y-%m-%d'


class CapitalizationTable:

    def __init__(self):
        self.employee_map = dict()
        self.equity_event_map = collections.defaultdict(lambda: [])

    def parse_csv(self, file_path):
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if not row:
                    continue
                event_type = row[0]
                employee_id = row[1]
                employee_name = row[2]
                award_id = row[3]
                award_date = datetime.strptime(row[4], DT_FORMAT).date()
                award_qty = int(row[5])

                if employee_id in self.employee_map:
                    emp = self.employee_map[employee_id]
                    emp.add_equity_award(award_id)
                else:
                    emp = Employee(employee_name, employee_id)
                    emp.add_equity_award(award_id)
                    self.employee_map[employee_id] = emp

                equity_event = EquityEvent(award_id, award_date, award_qty, event_type)
                self.equity_event_map[award_id].append(equity_event)

    def get_all_employee_vesting_status(self, as_of_date):
        vesting_schedule = []
        for employeeId, employee in self.employee_map.items():
            equity_awards = employee.get_equity_awards()
            for equityAward in equity_awards:
                print(employeeId, equityAward)
                equity_events = self.equity_event_map[equityAward]
                total_qty = 0
                for event in equity_events:
                    if event.awardDate > as_of_date:
                        continue
                    if event.eventType == 'VEST':
                        total_qty += event.awardQty
                    elif event.eventType == 'CANCEL':
                        total_qty -= event.awardQty
                vesting_schedule.append([employeeId, employee.employeeName, equityAward, total_qty])

        return vesting_schedule


class Employee:
    def __init__(self, employee_name, employee_id):
        self.employeeName = employee_name
        self.employeeID = employee_id
        self.equityAwards = set()  # list of award Ids ISO-001, IS0-002

    def add_equity_award(self, award_id):
        self.equityAwards.add(award_id)
        return

    def get_equity_awards(self):
        return self.equityAwards


class EquityEvent:

    def __init__(self, award_id, award_date, award_qty, event_type):
        self.awardId = award_id
        self.awardDate = award_date
        self.awardQty = award_qty
        self.eventType = event_type


if __name__ == '__main__':
    csv_path = '/Users/aaditidhikle/PycharmProjects/CapTable/example1.csv'
    target_date = datetime.strptime('2020-04-01', DT_FORMAT).date()
    capTable = CapitalizationTable()
    capTable.parse_csv(csv_path)
    print(capTable.get_all_employee_vesting_status(target_date))
