import psycopg2


def get_otp_from_db(phone_number):
    try:
        conn = psycopg2.connect(
            host="db-web-test.coxa42cl5wsl.ap-south-1.rds.amazonaws.com",
            port=5432,
            user="doadmin",
            password="FqnQQafJfSUQgyVh4y9n",
            database="defaultdb"
        )
        cursor = conn.cursor()

        # Fetching the 'token' from 'tokens' table using the correct 'phonenumber' column
        query = f"SELECT token FROM tokens WHERE phonenumber = '{phone_number}' ORDER BY id DESC LIMIT 1"

        cursor.execute(query)
        result = cursor.fetchone()

        conn.close()

        if result:
            return str(result[0])
        else:
            return None

    except Exception as e:
        print(f"Database Error: {e}")
        return None