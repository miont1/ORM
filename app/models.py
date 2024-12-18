from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    orders = relationship("Order", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="orders")
    books = relationship(
        "Book", secondary="order_items", back_populates="orders", overlaps="order_items"
    )
    order_items = relationship("OrderItem", back_populates="order", overlaps="books")

    # Метод для отримання кількості конкретної книгиs
    def get_book_quantity(self, book_id: int) -> int:
        order_item = next(
            (item for item in self.order_items if item.book_id == book_id), None
        )
        return order_item.quantity if order_item else 0

    def __repr__(self) -> str:

        books_info = ", ".join(
            [f"{book.title}: {self.get_book_quantity(book.id)}" for book in self.books]
        )
        return f"Order{self.id}, Books: [{books_info}], User:{self.user}"


class OrderItem(Base):
    __tablename__ = "order_items"
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items", overlaps="books")
    book = relationship(
        "Book", back_populates="order_items", overlaps="orders", viewonly=True
    )


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    orders = relationship(
        "Order",
        secondary="order_items",
        back_populates="books",
        overlaps="order",
        viewonly=True,
    )
    authors = relationship("Author", secondary="books_authors", back_populates="books")
    order_items = relationship("OrderItem", back_populates="book", overlaps="orders")

    def __repr__(self) -> str:
        return f"Book - {self.title}"


books_authors = Table(
    "books_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    books = relationship("Book", secondary="books_authors", back_populates="authors")

    def __repr__(self) -> str:
        return f"Author - {self.name}"
