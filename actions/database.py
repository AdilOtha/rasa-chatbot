import mysql.connector


def DataFetch(plant_name,plant_area,plant_problem):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="", database="rasa_test_data")
    mycursor = mydb.cursor()
    sql = "SELECT `જવાબ` FROM `table 1` WHERE `સેકટર`='ખેત' AND `ક્વેરી લખાણ` LIKE '%"+plant_problem+"%' AND (`પાક` LIKE '%"+plant_name+"%' OR `પાક` LIKE '%"+plant_area+"%') LIMIT 1"
    mycursor.execute(sql)
    result=None    
    for (data) in mycursor:
        print(data)
        result = data
    mycursor.close()
    return result

if __name__ == "__main__":
    DataFetch(plant_name,plant_area,plant_problem)
