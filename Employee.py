from ShareHolder import ShareHolder


class Employee(ShareHolder):
    """ Represents an Employee entity of type ShareHolder with attributes such as name, id and
        list of equity awarded so far.

        Attributes
        ----------
        full_name : str
            Employee First + Last Name
        shareholder_id : str
            Is the same as Employee ID
        employee_id : str
            Is the same as Shareholder ID
        _equity_awards : set
            Private list of unique award Ids to each Employee eg. ISO-001, IS0-002

    """
    def __init__(self, full_name, shareholder_id):
        super().__init__(full_name, shareholder_id)
        self.shareholder_type = 'Employee'
        self.employee_id = shareholder_id

