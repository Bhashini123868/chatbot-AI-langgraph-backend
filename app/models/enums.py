import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    chef = "chef"
    cashier = "cashier"

class OrderStatus(str, enum.Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    served = "served"
    completed = "completed"
    cancelled = "cancelled"

class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"
    mobile = "mobile"
    online = "online"


