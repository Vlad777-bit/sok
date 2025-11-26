from app.db.conn import get_conn


class ClientRepository:
    def create(self, data: dict) -> dict:
        sql = """
        INSERT INTO clients (
          full_name, date_of_birth,
          passport_series, passport_number,
          address_registration, phone, email,
          workplace, position, monthly_income
        )
        VALUES (%(full_name)s, %(date_of_birth)s,
                %(passport_series)s, %(passport_number)s,
                %(address_registration)s, %(phone)s, %(email)s,
                %(workplace)s, %(position)s, %(monthly_income)s)
        RETURNING *;
        """

        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)
                return cur.fetchone()

    def get_by_id(self, client_id: int) -> dict | None:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM clients WHERE id = %s;", (client_id,))
                return cur.fetchone()
