#errors
DATABASE_CREATE_ERROR = "database insertion error"

OK = "ok"

IMPORTANCE_CHOICES = [
    ('low','Low'),
    ('medium','Medium'),
    ('high', 'High'),
]

STATE_CHOICES = [
    ('OPEN','Open'),
    ('CLOSED','Closed'),
    ('IN PROGRESS', 'In Progress'),
    ('TESTING','Testing'),
    ('DONE','Done'),
]

ISSUE_CHOICES = [
    ('BUG','Bug'),
    ('SYSTEM DEFECT','System defect'),
    ('SPECIFICATION ISSUE','Specification issue'),
    ('DEVELOPMENT ISSUE','Development issue'),
]