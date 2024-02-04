import databases
import sqlalchemy

DATABASE_URL = "sqlite:///shop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("Пользователи", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("Имя", sqlalchemy.String(32)),
                         sqlalchemy.Column("Фамилия", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128), unique=True),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

products = sqlalchemy.Table("Товары", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("Название", sqlalchemy.String(50)),
                            sqlalchemy.Column("Описание", sqlalchemy.String(300)),
                            sqlalchemy.Column("Цена", sqlalchemy.Float)
                            )

orders = sqlalchemy.Table("Заказы", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("Пользователи.id")),
                          sqlalchemy.Column("prod_id", sqlalchemy.ForeignKey("Товары.id")),
                          sqlalchemy.Column("Дата_заказа", sqlalchemy.DateTime),
                          sqlalchemy.Column("Статус_заказа", sqlalchemy.String(20))
                          )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

try:
    metadata.create_all(engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating tables: {e}")
