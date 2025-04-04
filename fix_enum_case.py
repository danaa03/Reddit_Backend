# fix_enum_case.py
from sqlalchemy import text
from database import get_db

def fix_enum_case():
    db = next(get_db())
    try:
        # Update existing values
        db.execute(text("UPDATE users SET role = 'USER' WHERE role = 'user'"))
        db.execute(text("UPDATE users SET role = 'MODERATOR' WHERE role = 'moderator'"))
        db.execute(text("UPDATE users SET role = 'ADMIN' WHERE role = 'admin'"))
        
        # Create new enum type
        db.execute(text("ALTER TYPE userrole RENAME TO userrole_old"))
        db.execute(text("CREATE TYPE userrole AS ENUM ('USER', 'MODERATOR', 'ADMIN')"))
        
        # Update column to use new enum
        db.execute(text("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::text::userrole"))
        
        # Drop old enum
        db.execute(text("DROP TYPE userrole_old"))
        
        db.commit()
        print("Successfully updated enum values")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_enum_case()