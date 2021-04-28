import sqlalchemy

metadata = sqlalchemy.MetaData()

applications_table = sqlalchemy.Table(
    "applications", metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.String(500)),
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
