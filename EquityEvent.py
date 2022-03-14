class EquityEvent:
    """Represents an Equity Event of type Vest/Cancel on a given date for
       certain quantity.

        Attributes
        ----------
        award_id : str
            Unique Award ID for every new equity awarded to the employee
        event_date : date
            Date of equity vesting or cancelling
        award_qty : decimal/int
            quantity getting vested/cancelled
        event_type: str
            VEST or CANCEL
    """
    def __init__(self, award_id, event_date, event_type, award_qty=0):
        self.award_id = award_id
        self.event_date = event_date
        self.award_qty = award_qty
        self.event_type = event_type
