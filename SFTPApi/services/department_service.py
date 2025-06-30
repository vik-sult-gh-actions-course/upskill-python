from typing import Optional
import pandas as pd
from sqlalchemy.orm import Session

from SFTPApi.models import Departments


class DepartmentService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def process_department_dataframe(self, df: Optional[pd.DataFrame]) -> None:
        """Process a DataFrame to create or update department records"""
        if df is None:
            return

        for _, row in df.iterrows():
            self._process_department_row(row)

    def _process_department_row(self, row: pd.Series) -> None:
        """Process a single row of department data"""
        department_email = row.department_email
        department_model = self._get_department_by_email(department_email)

        department_attributes = self._extract_department_attributes(row)

        if department_model is None:
            department_model = self._create_department(department_email, department_attributes)
        else:
            self._update_department(department_model, department_attributes)

        self._save_department(department_model)

    def _get_department_by_email(self, email: str):
        """Retrieve department by email"""
        return self.session.query(Departments).filter_by(email=email).first()

    @staticmethod
    def _extract_department_attributes(row: pd.Series) -> dict:
        """Extract department attributes from DataFrame row"""
        return {
            'name': row.department_name,
            'code': row.department_code,
            'head': row.department_head,
            'size': row.department_size,
            'budget': row.department_budget,
            'location': row.department_location,
            'phone': row.department_phone,
            'manager': row.department_manager,
            'creation_date': row.department_creation_date,
        }

    def _create_department(self, email: str, attributes: dict):
        """Create new department"""
        return Departments(email=email, **attributes)

    def _update_department(self, department, attributes: dict):
        """Update existing department"""
        for attr, value in attributes.items():
            setattr(department, attr, value)

    def _save_department(self, department):
        """Save department to database"""
        self.session.add(department)
        self.session.commit()
