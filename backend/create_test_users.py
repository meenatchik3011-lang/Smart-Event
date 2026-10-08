
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password


db = SessionLocal()


def create_user(
    username: str,
    email: str,
    password: str,
    role: str,
):
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        print(
            f"User already exists: "
            f"{email} ({existing_user.role})"
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
    db.refresh(user)

    print(
        f"Created {role}: {email}"
    )


# =========================================================
# ORGANIZER 1
# =========================================================

create_user(
    username="organizer1",
    email="organizer@example.com",
    password="Organizer123",
    role="ORGANIZER",
)


# =========================================================
# ORGANIZER 2
# =========================================================

create_user(
    username="organizer2",
    email="organizer2@example.com",
    password="Organizer456",
    role="ORGANIZER",
)


# =========================================================
# ADMIN
# =========================================================

create_user(
    username="admin1",
    email="admin@example.com",
    password="Admin123",
    role="ADMIN",
)


db.close()

print("Test users setup completed.")
