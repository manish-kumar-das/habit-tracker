"""
Service for managing user profile
"""

from datetime import datetime
from app.db.database import get_db_connection


class ProfileService:
    """Service for profile operations"""
    
    def __init__(self):
        pass
    
    def get_profile(self):
        """Get user profile"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM user_profile WHERE id = 1')
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'name': row['name'],
                'email': row['email'],
                'bio': row['bio'],
                'avatar_path': row['avatar_path'] if 'avatar_path' in row.keys() else None,
                'created_at': row['created_at'],
                'updated_at': row['updated_at'] if 'updated_at' in row.keys() else None
            }
        else:
            # Return default profile
            return {
                'name': 'Alex Morgan',
                'email': 'alex.morgan@example.com',
                'bio': 'Building better habits, one day at a time! 🚀',
                'avatar_path': None,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': None
            }
    
    def update_profile(self, name=None, email=None, bio=None, avatar_path=None):
        """Update user profile"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if name is not None:
            updates.append("name = ?")
            params.append(name)
        
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        
        if bio is not None:
            updates.append("bio = ?")
            params.append(bio)
        
        if avatar_path is not None:
            updates.append("avatar_path = ?")
            params.append(avatar_path)
        
        if updates:
            # Add updated_at timestamp
            updates.append("updated_at = ?")
            params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            params.append(1)  # id = 1
            
            query = f"UPDATE user_profile SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
        
        conn.close()
        
        return True


# Global service instance
_profile_service_instance = None


def get_profile_service() -> ProfileService:
    """Get global profile service instance"""
    global _profile_service_instance
    if _profile_service_instance is None:
        _profile_service_instance = ProfileService()
    return _profile_service_instance
