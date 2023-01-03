import psycopg2


def create_db(conn):

    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            surname VARCHAR(60) NOT NULL,
            email VARCHAR(90) NOT NULL UNIQUE );
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(id),
            number VARCHAR(11) UNIQUE);
        """)
        conn.commit()
        print('Созданы таблицы clients и phones')

def add_client(conn, client_name, client_surname, client_email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO clients(name, surname, email)
        VALUES (%s, %s, %s) RETURNING id;
        """, (client_name, client_surname, client_email,))
        client_id = cur.fetchone()
        if phones:
            for phone in phones:
                cur.execute("""
                        INSERT INTO phones(client_id, number)
                        VALUES (%s, %s);
                        """, (client_id, phone))
            conn.commit()

    print('Добавлен новый клиент: ', client_name, client_surname, client_email, phones)

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phones(client_id, number) 
        VALUES (%s, %s);
        """, (client_id, phone))
        conn.commit()
    print('Клиенту с id ', client_id, 'добавлен новый номер телефона:', phone)

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone_to_update=None, new_phone = None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("""
            UPDATE clients
            SET name = %s
            WHERE id = %s;
        """, (first_name, client_id))
        if last_name:
            cur.execute("""
            UPDATE clients
            SET surname = %s
            WHERE id = %s;
        """, (last_name, client_id))
        if email:
            cur.execute("""
            UPDATE clients
            SET email = %s
            WHERE id = %s
        """, (email, client_id))
        if phone_to_update and new_phone:
            cur.execute(
                """
                UPDATE phones
                SET number = %s
                WHERE number = %s;
                """, (new_phone, phone_to_update)
            )
        conn.commit()
    print('Для клиента ', client_id, 'сделаны запрошенные изменения')
def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id = %s AND number = %s;
        """, (client_id, phone))

    conn.commit()
    print('Для клиента ', client_id, 'добавлен номер телефона', phone)

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phones
        WHERE client_id = %s;
        """, (client_id,))

        cur.execute("""
        DELETE FROM clients
        WHERE id = %s;
        """, (client_id,))
    conn.commit()
    print('Клиент номер ', client_id, 'удален')

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        if first_name:
            cur.execute("""
            SELECT * FROM clients
            WHERE name = %s;
            """, (first_name,))
            clients_info = cur.fetchall()
        elif last_name:
            cur.execute("""
                        SELECT * FROM clients
                        WHERE surname = %s;
                        """, (last_name,))
            clients_info = cur.fetchall()
        elif email:
            cur.execute("""
                        SELECT * FROM clients
                        WHERE email = %s;
                        """, (email,))
            clients_info = cur.fetchall()
        elif phone:
            cur.execute("""
                            SELECT client_id FROM phones
                            WHERE number = %s;
            """, (phone,))
            client_id = cur.fetchone()
            cur.execute("""
                            SELECT * FROM clients
                            WHERE id = %s;
                            """, (client_id,))
            clients_info = cur.fetchall()
        for client_info in clients_info:
            client_id = list(client_info)[0]
            cur.execute("""
            SELECT number FROM phones
            WHERE client_id = %s
            """, (client_id,))
            number = cur.fetchall()

            print('Информация о клиенте: ', ' '.join([i for i in client_info[1:]]), '\nЗарегистрированные номера телефонов: ', ' '.join([i[0] for i in number]))


if __name__ == "__main__":
    with psycopg2.connect(database="PersonalData", user="postgres", password="postgres") as conn:
        create_db(conn)
        add_client(conn, 'Daria', 'Korotkova', 'dasha1235@example.com', phones=['89045974659'])
        add_client(conn, 'Ivan', 'Ivanov', 'ii1235@example.com', phones=['89045975555'])

        add_phone(conn, 1, '49151503593')

        change_client(conn, 1, first_name='Alexandra', last_name='Ivanova', email='sahsa@gmail.com', phone_to_update='89045974659',
                          new_phone='89045975554')
        delete_phone(conn, 1, '89045975555')
        delete_client(conn, 2)
        find_client(conn, phone='89045975554')

# conn.close()