from dataclasses import dataclass

@dataclass
class Habit:
    id: int
    name: str
    description: str
    category: str
    frequency: str
    created_at: str
    
    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row['id'],
            name=row['name'],
            description=row['description'] if row['description'] else '',
            category=row['category'] if row['category'] else 'General',
            frequency=row['frequency'],
            created_at=row['created_at']
        )
