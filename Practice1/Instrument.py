class Instrument:
    def __init__(self, name: str, price: float, stock: int, color: str, category: str):
        self.name = name
        self.price = price
        self.stock = stock
        self.color = color
        self.category = category

    def __json__(self):
        return {
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "color": self.color,
            "category": self.category,
        }
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            color=data["color"],
            category=data["category"],
        )

    def __str__(self):
        return f"{self.name} - {self.price} руб. (в наличии: {self.stock}, цвет: {self.color}, категория: {self.category})"