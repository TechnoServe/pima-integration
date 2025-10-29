from sqlalchemy.orm import Session
from models import Attendance
from schemas import AttendanceCreate
from core import logger


class AttendanceService:
    """Handles database operations for training sessions"""

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, data: AttendanceCreate, created_by_id: str) -> Attendance:
        """Upsert training session data"""

        # Check if record exists by CommCare case ID
        existing = (
            self.db.query(Attendance)
            .filter(
                Attendance.submission_id == data.submission_id,
                Attendance.is_deleted == False,
            )
            .first()
        )

        if existing:
            logger.info(
                {
                    "message": f"Updating existing attendance record: {data.submission_id}"
                }
            )
            return self._update_existing(existing, data, created_by_id)
        else:
            logger.info(
                {"message": f"Creating new attendance record: {data.submission_id}"}
            )
            return self._create_new(data, created_by_id)

    def _update_existing(
        self, existing: Attendance, data: AttendanceCreate, updated_by_id: str
    ) -> Attendance:
        """Update existing training session with smart merging"""

        # Smart update: don't overwrite existing data with None values
        for field, value in data.model_dump(exclude_unset=True).items():
            if field in ["training_session_id", "farmer_id", "submission_id"]:
                # Always update core fields
                setattr(existing, field, value)
            elif value is not None:
                # Only update other fields if new value is not None
                current_value = getattr(existing, field, None)
                if current_value is None or value != current_value:
                    setattr(existing, field, value)

        existing.last_updated_by_id = updated_by_id

        self.db.commit()
        self.db.refresh(existing)
        return existing

    def _create_new(self, data: AttendanceCreate, created_by_id: str) -> Attendance:
        """Create new training session"""

        attendance = Attendance(
            **data.model_dump(exclude_unset=True),
            created_by_id=created_by_id,
            last_updated_by_id=created_by_id,
        )

        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance
