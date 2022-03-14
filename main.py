# coding=utf-8
import csv
import collections
import enum
import argparse
from datetime import datetime
from datetime import date
from EquityEvent import EquityEvent
from Employee import Employee


class EquityEventType(enum.Enum):
    VEST = 'VEST'
    CANCEL = 'CANCEL'

    @staticmethod
    def from_string(s):
        try:
            return EquityEventType[s]
        except KeyError:
            raise ValueError('Error while parsing {event} as an event type'.format(event=s))


DT_FORMAT = '%Y-%m-%d'


class CapitalizationTable:
    """A class that parses raw equity events, maintains an employee map and
        an equity event map.

        Attributes
        ----------
        _employee_map : hashmap/dictionary
            Private map of employee ids mapped to an employee obj that contains employee
            info along with equity IDs of equity awarded to them so far
        _equity_event_map : defaultdict
            Private map of all events pivoted by award id (eq. ISO-001)
    """

    def __init__(self):
        self._employee_map = dict()
        self._equity_event_map = collections.defaultdict(lambda: [])
        self.event_file_names = {'event_type': 'str',
                                 'employee_id': 'str',
                                 'employee_name': 'str',
                                 'award_id': 'str',
                                 'event_date': 'date',
                                 'award_qty': 'int'
                                 }

    def validate_data_row(self, row):
        """ Validate data in each csv row. Employee ID and Award ID cannot be null"""
        try:
            row['event_type'] = EquityEventType.from_string(row['event_type'].strip().upper())
            employee_id = row['employee_id'].strip()
            if employee_id is None or len(employee_id) < 1:
                raise ValueError('Employee ID cannot be null')
            row['employee_id'] = employee_id
            row['employee_name'] = row['employee_name'].strip()
            award_id = row['award_id'].strip()
            if award_id is None or len(award_id) < 1:
                raise ValueError('Award ID cannot be null')
            row['award_id'] = award_id
            row['event_date'] = datetime.strptime(row['event_date'].strip(), DT_FORMAT).date()
            row['award_qty'] = int(row['award_qty'].strip())
        except ValueError as e:
            print('Exception caught for {data_row}'.format(data_row=row))
            raise e
        return row

    def parse_csv(self, file_path):
        """ Parses raw csv events and adds data into Employee dictionary
            and equity_event dictionary
        """
        try:
            with open(file_path, newline='') as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=self.event_file_names.keys())
                rows = list(reader)
                if not len(rows):
                    raise Exception("Empty CSV File")
                for row in reader:
                    if len(row) < len(self.event_file_names.keys()):
                        raise Exception("File contains malformed row.")

                    row = self.validate_data_row(row)
                    # add data into employee table
                    self.update_employee_map(row['employee_name'], row['employee_id'], row['award_id'])
                    # add data into equity event table
                    self.update_equity_event_map(row['award_id'],
                                                 row['event_date'],
                                                 row['award_qty'],
                                                 row['event_type'])
        except EOFError as ex:
            print("Caught EOF error while parsing file {file_path}".format(file_path=file_path))
            raise ex
        except IOError as ie:
            print("Caught I/O error while parsing file {file_path}".format(file_path=file_path))
            raise ie
        except TypeError as t:
            print("File contains malformed row")
        except ValueError as v:
            print("Invalid data found. Not parsing further rows.")
        except Exception as exp:
            raise exp
        return

    def update_employee_map(self, employee_name, employee_id, award_id):
        """Create or update an existing Employee object with new award id"""
        if employee_id in self._employee_map:
            emp = self._employee_map[employee_id]
            emp.add_equity_award(award_id)
        else:
            emp = Employee(employee_name, employee_id)
            emp.add_equity_award(award_id)
            self._employee_map[employee_id] = emp
        return

    def update_equity_event_map(self, award_id, event_date, award_qty, event_type):
        """Add Equity event to Equity Event Map"""
        equity_event = EquityEvent(award_id, event_date, event_type, award_qty)
        self._equity_event_map[award_id].append(equity_event)
        return

    def get_employee_vesting_status(self, as_of_date, employee_id, employee):
        """ Get vesting status for an employee"""
        vesting_schedule = []
        equity_awards = employee.get_equity_awards()
        for equity_award in equity_awards:
            equity_events = self._equity_event_map[equity_award]
            total_qty = 0
            for event in equity_events:
                if event.event_date > as_of_date:
                    continue
                if event.event_type == EquityEventType.VEST:
                    total_qty += event.award_qty
                elif event.event_type == EquityEventType.CANCEL:
                    total_qty -= event.award_qty
            vesting_schedule.append([employee_id,
                                     employee.full_name,
                                     equity_award,
                                     total_qty])
        return vesting_schedule

    def get_all_employee_vesting_status(self, as_of_date=date.today()):
        """Get vesting status as of a given date for all employees
           in the employee map

           Attributes:
          ------------
          as_of_date: date
          Defaults to Today's date if date is not passed
        """
        vesting_schedule = []
        for employee_id, employee in self._employee_map.items():
            employee_vesting_status = self.get_employee_vesting_status(as_of_date,
                                                                       employee_id,
                                                                       employee)
            vesting_schedule += employee_vesting_status
        return vesting_schedule


if __name__ == '__main__':
    try:
        csv_path = '/Users/aaditidhikle/PycharmProjects/CapTable/example1.csv'
        target_date = datetime.strptime('2021-04-01', DT_FORMAT).date()
        capTable = CapitalizationTable()
        capTable.parse_csv(csv_path)
        print(capTable.get_all_employee_vesting_status(target_date))
        '''
           arg_parser = argparse.ArgumentParser()
            arg_parser.add_argument('csv_path', type=str)
            arg_parser.add_argument("target_date",
                                   type=lambda d: datetime.strptime(d, DT_FORMAT).date())
            args = arg_parser.parse_args()
    
            cap_table = CapitalizationTable()
            cap_table.parse_csv(args.csv_path)
            schedule = cap_table.get_all_employee_vesting_status(args.target_date)
            for item in schedule:
                print(item)
        '''
    except Exception as e:
        print(e)


if __name__ == '__main__':
    csv_path = '/Users/aaditidhikle/PycharmProjects/CapTable/example1.csv'
    target_date = datetime.strptime('2020-04-01', DT_FORMAT).date()
    capTable = CapitalizationTable()
    capTable.parse_csv(csv_path)
    print(capTable.get_all_employee_vesting_status(target_date))
