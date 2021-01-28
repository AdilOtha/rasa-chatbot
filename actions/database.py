import mysql.connector


def DataFetch(plant_name, plant_area, plant_problem):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="", database="kisan")
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT `response` FROM `query` WHERE `sector`='ખેત' AND ((`query_text` LIKE '%{}%' AND `crop` LIKE '%{}%') OR `query_text` LIKE '%{}%') AND `response` NOT LIKE '%કિસાન કોલ સેન્ટર%' LIMIT 1".format(
        plant_problem, plant_name, plant_area)
    mycursor.execute(sql)
    result = None
    for data in mycursor:
        result = data
        break
    mycursor.close()
    return result


def DataInsert(query):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="", database="kisan")
    mycursor = mydb.cursor()
    sql = "INSERT INTO fallback_queries (query) VALUES ('{}');".format(query)
    mycursor.execute(sql)
    result = None
    for (data) in mycursor:
        print(data)
    mycursor.close()
    mydb.commit()


def GetPrice(plant_name):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="", database="kisan")
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT `response` FROM `query` WHERE `query_type`='બજાર માહિતી' AND `crop` LIKE '%{}%' AND `response` NOT LIKE '%કિસાન કોલ સેન્ટર%' LIMIT 1".format(plant_name)
    mycursor.execute(sql)
    result = None
    for data in mycursor:
        result = data
        break
    mycursor.close()
    return result

def GetFertilizer(plant_name):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="", database="kisan")
    mycursor = mydb.cursor(buffered=True)
    sql = "SELECT `response` FROM `query` WHERE `query_type`='ખાતર ઉપયોગ અને ઉપલબ્ધિ' AND `crop` LIKE '%{}%' AND (`query_text` LIKE '%/Gernal%' OR `query_text` LIKE '%ખાતર%' OR `query_text` LIKE '%PGR%') AND `response` NOT LIKE '%કિસાન કોલ સેન્ટર%' LIMIT 1".format(plant_name)
    mycursor.execute(sql)
    result = None
    for data in mycursor:
        result = data
        break
    mycursor.close()
    return result    
