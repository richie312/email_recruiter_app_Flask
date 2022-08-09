class Generator(object):

    """
    Generator class generates common sql insert, update, delete,
    select along with where clause.
    It expects the payloads which further supplies the reqd information
    to the specific methods.

    """

    def __init__(self, payload):
        self.payload = payload

    def create_table(self):
        query = """CREATE TABLE user (id INT NOT NULL AUTO_INCREMENT,
                                      public_id VARCHAR(50),name VARCHAR(100),
                                      email CHAR(100), password VARCHAR(80),
                                      created DATE,
	                                  CONSTRAINT contacts_pk PRIMARY KEY (id));"""

        return query

    def delete_query(self):
        query = """del from {table_name} where {target_column}=%s""".format(
            table_name=self.payload["TableName"],
            target_column=self.payload["TargetColumn"],
        )

    def select_query(self):
        query = "select * from {table_name}".format(
            table_name=self.payload["TableName"]
        )
        return query

    def insert_query(self):
        columns = self.payload["Params"]["Data"]["Columns"]
        data_type = self.payload["Params"]["Placeholder"]
        # create the dynamic insert query.
        insert_query = (
            "INSERT INTO {table}".format(table=self.payload["TableName"])
            + "{columns} ".format(columns=columns)
            + "VALUES "
            + "{data_type}".format(data_type=data_type)
        )
        print(insert_query)
        return insert_query

    def col_query(self):
        col_query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s".format(
            TABLE_NAME=self.payload["TableName"]
        )
        return col_query
