import sqlalchemy

from .environments import environments_table

metadata = sqlalchemy.MetaData()

variables_table = sqlalchemy.Table(
    "variables", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255)),
    sqlalchemy.Column("value", sqlalchemy.String()),
    sqlalchemy.Column(
        "is_deleted", 
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.false(),
        nullable=False
    ),
    sqlalchemy.Column("env_id", sqlalchemy.ForeignKey(environments_table.c.id, ondelete="CASCADE"), index=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime())
)
