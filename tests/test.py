import psycopg2

def main():
    conn = psycopg2.connect("postgresql://vitaboost_test_user:nxMYOvPGFypifp35MzunOwei8wv6QfGr@dpg-cumudblsvqrc73flhak0-a.oregon-postgres.render.com/vitaboost_test")
    conn.close()

if __name__ == '__main__':
    main()
