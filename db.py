from pymongo import MongoClient

client = MongoClient("mongodb+srv://HireIO:TestPDFfile@cluster0-1god2.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('HireIO_db')

records = db.HireIO_Records

