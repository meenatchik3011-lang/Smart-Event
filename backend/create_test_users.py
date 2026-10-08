from app.database import SessionLocal
from app.models import User
from app.auth import hash_password


db = SessionLocal()


def create_user(
    username,
    email,
    password,
    role,
):
    existing = db.query(User).filter(
        User.email == email
    ).first()

    if existing:
        print(
            f"{email} already exists as {existing.role}"
        )
        return

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role,
    )

    db.add(user)
    db.commit()

    print(
        f"Created {role}: {email}"
    )


create_user(
    "organizer1",
    "organizer@example.com",
    "Organizer123",
    "ORGANIZER",
)

create_user(
    "admin1",
    "admin@example.com",
    "Admin123",
    "ADMIN",
)


db.close()