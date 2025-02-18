import psycopg2


def get_db_connection():
    return psycopg2.connect(
        "postgresql://vitaboost_test_user:nxMYOvPGFypifp35MzunOwei8wv6QfGr@dpg-cumudblsvqrc73flhak0-a.oregon-postgres.render.com/vitaboost_test"
    )
def customer_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE email = %s", (email,))
    result = cursor.fetchone()

    cursor.close()

    if result is not None:
        return True
    else:
        return False

def insert_customer(firstname, surname, email, password, birthdate):
    conn = get_db_connection()


    if customer_exists(email):
        print("Sie haben sich bereits registriert")
        return False


    cursor = conn.cursor()

    insert_statement = """insert into customer (firstname, surname, email, password, birthdate)
    values (%s, %s, %s, %s, %s)"""



    cursor.execute(insert_statement, (firstname, surname, email, password, birthdate))
    conn.commit()



    count = cursor.rowcount
    print(count, "Datensatz erfolgreich in die Tabelle 'customer' eingefügt")

    cursor.close()
    return True

if __name__ == '__main__':
    conn = get_db_connection()

    cursor = conn.cursor()
    postgreSQL_select_Query = "select * from customer"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from publisher table using cursor.fetchall")

    publisher_records = cursor.fetchall()
    print(publisher_records)

    cursor.close()
    conn.close()
