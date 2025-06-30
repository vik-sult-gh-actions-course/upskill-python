from typing import Optional
import pandas as pd
from sqlalchemy.orm import Session

from SFTPApi.models import People


class PeopleService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def process_people_dataframe(self, df: Optional[pd.DataFrame]) -> None:
        """Process a DataFrame to create or update people records"""
        if df is None:
            return

        for _, row in df.iterrows():
            self._process_people_row(row)

    def _process_people_row(self, row: pd.Series) -> None:
        """Process a single row of people data"""
        email = row.email
        # print(row)
        model = self._get_by_email(email)

        attributes = self._extract_attributes(row)

        if model is None:
            model = self._create(email, attributes)
        else:
            self._update(model, attributes)

        self._save(model)

    def _get_by_email(self, email: str):
        """Retrieve person by email"""
        return self.session.query(People).filter_by(email=email).first()

    @staticmethod
    def _extract_attributes(row: pd.Series) -> dict:
        """Extract person attributes from DataFrame row"""
        return {
            'source_id': row.employee_id,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'gender': row.gender,
            'phone_number': row.phone_number,
            'job_title': row.job_title,
            'department': row.department,
            'address': row.address,
            'city': row.city,
            'state': row.state,
            'country': row.country,
            'postal_code': row.postal_code,
            'start_time': row.start_time,
            'end_time': row.end_time,
            'manager_id': row.manager_id,
            'salary': row.salary,
            'hire_date': row.hire_date,
            'age': row.age,
            'years_of_experience': row.years_of_experience,
        }

    def _create(self, email: str, attributes: dict):
        """Create new person"""
        return People(email=email, **attributes)

    def _update(self, person, attributes: dict):
        """Update existing person"""
        for attr, value in attributes.items():
            setattr(person, attr, value)

    def _save(self, person):
        """Save person to database"""
        self.session.add(person)
        self.session.commit()
