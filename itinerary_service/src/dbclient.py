import psycopg2
from schemas import TravelPlan
from typing import List
from uuid import uuid4

class DbClient:
    def __init__(self, user, password):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user=user,
            password=password,
            database="itinerary_db"
        )

        self.create_travel_plans_if_not_exists()
    
    def create_travel_plans_if_not_exists(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS travel_plans (
                    id UUID PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    location_name VARCHAR(255),
                    location_lat DOUBLE PRECISION,
                    location_long DOUBLE PRECISION,
                    arrival_date BIGINT,
                    departure_date BIGINT,
                    user_email VARCHAR(255) NOT NULL
                )
                """
            )
            self.conn.commit()
    
    def get_all_travel_plans_by_email(self, email: str) -> List[TravelPlan]:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM travel_plans WHERE user_email=%s
                """,
                (email,)
            )
            rows = cursor.fetchall()
            travel_plans = [TravelPlan(*row) for row in rows]

            return travel_plans

    def create_new_travel_plan(self, travel_plan: TravelPlan):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO travel_plans (
                    id, 
                    title, 
                    description,
                    location_name,
                    location_lat,
                    location_long,
                    arrival_date,
                    departure_date, 
                    user_email
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(uuid4()), 
                    travel_plan.title, 
                    travel_plan.description, 
                    travel_plan.location_name,
                    travel_plan.location_lat,
                    travel_plan.location_long,
                    travel_plan.arrival_date,
                    travel_plan.departure_date,
                    travel_plan.user_email
                )
            )

            self.conn.commit()