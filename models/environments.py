import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from .applications import applications_table


metadata = sqlalchemy.MetaData()

environments_table = sqlalchemy.Table(
    "environments", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.String(500)),
    sqlalchemy.Column(
        "code",
        UUID(as_uuid=False),
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True,
    ),
    sqlalchemy.Column("app_id", sqlalchemy.ForeignKey(applications_table.c.id, ondelete="CASCADE"), index=True),
    sqlalchemy.Column(
        "is_deleted", 
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.false(),
        nullable=False
    ),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime())
)
