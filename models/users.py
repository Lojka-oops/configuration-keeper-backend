import sqlalchemy


metadata = sqlalchemy.MetaData()

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(40), unique=True, index=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime(), nullable=False),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime()),
    sqlalchemy.Column("deleted_at", sqlalchemy.DateTime()),
    sqlalchemy.Column(
        "is_deleted", 
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.false(),
        nullable=False
    ),
)
