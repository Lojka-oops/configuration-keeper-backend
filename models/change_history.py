import enum

import sqlalchemy


metadata = sqlalchemy.MetaData()

change_history_table = sqlalchemy.Table(
    "change_history", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("entity_type", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("entity_id", sqlalchemy.Integer, index=True, nullable=False),
    sqlalchemy.Column("field", sqlalchemy.String(100)),
    sqlalchemy.Column("old_value", sqlalchemy.String()),
    sqlalchemy.Column("new_value", sqlalchemy.String()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(), nullable=False)
)
