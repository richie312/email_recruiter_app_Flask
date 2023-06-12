from config.database import Database
Location = ''
db = Database()

conn = db.row_insertion()
cursor = conn.cursor()

query = "select Location from company_email1 where Email_Address = %s"

cursor.execute(query,("karthick.chinnasamy@careernet.co.in",))

data = cursor.fetchall()