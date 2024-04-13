class StudentInfo:
    def __init__(self, student_id, name, balance, minimum):
        self.student_id = student_id
        self.name = name
        self.balance = balance
        self.minimum = minimum

    def is_balance_sufficient(self):
        return self.balance >= self.minimum