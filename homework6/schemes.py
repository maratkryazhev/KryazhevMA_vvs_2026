class User:
    __tablename__ = "users"

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.passwd = passwd
        self.operations_cnt = 0
        self.energy = 0
