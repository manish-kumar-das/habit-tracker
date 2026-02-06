"""
Habit model with category support
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Habit:
    """Habit data model"""
    id: Optional[int]
    name: str
    description: Optional[str]
    category: str
    frequency: str
    created_at: str
    is_active: bool = True
    
    @staticmethod
    def from_db_row(row) -> 'Habit':
        """Create Habit instance from database row"""
        # Handle both old and new database schemas
        try:
            category = row['category']
        except (KeyError, IndexError):
            category = 'General'
        
        return Habit(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            category=category,
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
            'category': self.category,
            'frequency': self.frequency,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
