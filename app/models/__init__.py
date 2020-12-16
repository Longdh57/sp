# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.base_model import Base  # noqa
from app.models.staff import Staff  # noqa
