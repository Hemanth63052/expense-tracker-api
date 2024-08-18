import logging as logger

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.orm import Session


class SQLUtil:
    def __init__(self, session: Session):
        self.session = session

    def __del__(self):
        self.session.close()

    def fetch_as_json(self, query):
        try:
            return jsonable_encoder(self.session.execute(query).mappings().all())
        except Exception as e:
            logger.error(f"Error occurred while fetching data: {e}")

    def insert_into_postgres_using_session(self, data, pg_table):
        final_records = []
        try:
            if isinstance(data, dict):
                final_records.append(pg_table(**data))
            elif isinstance(data, list):
                for each_data in data:
                    final_records.append(pg_table(**each_data))
            self.session.add_all(final_records)
            self.session.commit()
            logger.info(f"Save Success to {pg_table.__tablename__}")
        except Exception as e:
            logger.info(e)

    def update_postgres_columns(self, filter_dict, update_dict, table):
        with self.session as session:
            filters = self.create_dynamic_filter(table, filter_dict)
            query = session.query(table).filter(*filters)
            records = query.all()
            for record in records:
                for key, value in update_dict.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
            session.commit()

    @staticmethod
    def create_dynamic_filter(model, filter_dict):
        filters = [getattr(model, key) == value for key, value in filter_dict.items()]
        return filters

    def delete_data(self, filter_dict, table):
        with self.session as session:
            filters = [
                getattr(table, key) == value for key, value in filter_dict.items()
            ]
            query = session.query(table).filter(and_(*filters))
            records = query.all()
            for record in records:
                session.delete(record)
            session.commit()
