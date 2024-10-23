from pymongo import MongoClient

# Conectar a MongoDB Atlas
client = MongoClient("mongodb+srv://ismael:taco1234@cluster0.axu9d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mongo = client['LIEG']
