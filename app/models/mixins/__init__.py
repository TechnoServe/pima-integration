"""Init file for centralizing the mixins importation"""

from .audit import AuditMixin
from .sf_id import SFIDMixin
from .soft_delete import SoftDeleteMixin
from .timestamp import TimestampMixin
from .uuid import UUIDMixin

print("Imported all centralized model mixins successfully!")
