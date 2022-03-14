class ShareHolder:
    """ Represents an ShareHolder class that will be a parent to entities
        Employee, Investors and Advisors.

        Attributes
        ----------
        full_name : str
            Shareholder First + Last Name
        shareholder_id : str
            Unique Identifier for a shareholder. The Employee Ids start with E
        _equity_awards : set
            Private list of unique award Ids eg. ISO-001, IS0-002
    """
    def __init__(self, full_name, shareholder_id):
        self.shareholder_id = shareholder_id
        self.full_name = full_name
        self._equity_awards = set()

    def add_equity_award(self, award_id):
        """Setter Method to add a new award id"""
        self._equity_awards.add(award_id)
        return

    def get_equity_awards(self):
        """Getter method for returning equity awards list"""
        return self._equity_awards
    
