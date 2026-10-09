
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password


db = SessionLocal()

try:
    email = "organizer2@example.com"

    user = db.query(User).filter(User.email == email).first()

    if user:
        user.role = "ORGANIZER"
        db.commit()
        print(f"{email} updated to ORGANIZER")

    else:
        organizer = User(
            username="organizer2",
            email=email,
            hashed_password=hash_password("Organizer@123"),
            role="ORGANIZER",
        )

        db.add(organizer)
        db.commit()

        print("Organizer created successfully!")
        print("Email: organizer2@example.com")
        print("Password: Organizer@123")
        print("Role: ORGANIZER")

except Exception as exc:
    db.rollback()
    print(f"Error: {exc}")

finally:
    db.close()
