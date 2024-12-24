from sqlalchemy.orm import Session
from ..model import Event


class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event: Event) -> Event:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_event_by_id(self, event_id: int):
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_all_events(self, user_id: int):
        return self.db.query(Event).filter(Event.user_id == user_id).all()
