"""
Habit model
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    """Habit data model"""
    id: Optional[int]
    name: str
    description: Optional[str]
    frequency: str
    created_at: str
    is_active: bool = True
    
    @staticmethod
    def from_db_row(row) -> 'Habit':
        """Create Habit instance from database row"""
        return Habit(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            frequency=row['frequency'],
            created_at=row['created_at'],
            is_active=bool(row['is_active'])
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'frequency': self.frequency,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
