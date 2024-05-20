class Reservation:
    def __init__(self, customer_id, start_date, end_date):
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date

    def get_customer_id(self):
        return self.customer_id
