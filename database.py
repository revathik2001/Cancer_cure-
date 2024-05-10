import mysql.connector

host = "localhost"
user = "root"
password ="root"  
database_name = "python_core_cancer_main"  

def select(query):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    return result

def update(query):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query)
    cnx.commit()
    result = cursor.rowcount
    cursor.close()
    cnx.close()
    return result

def delete(query):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query)
    cnx.commit()
    result = cursor.rowcount
    cursor.close()
    cnx.close()
    return result

def insert(query):
    cnx = mysql.connector.connect(host=host, user=user, password=password, database=database_name)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query)  
    cnx.commit()
    result = cursor.lastrowid
    cursor.close()
    cnx.close()
    return result

def save_user(name, email, password):
    query = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
    data = (name, email, password)
    return insert(query, data)