
# 在postgres中创建"system_prompts"的表

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.day13_databases import Base

class SystemPromptModel(Base):
    __tablename__ = "system_prompts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    role: Mapped[str] = mapped_column(String(50), unique=True, index=True) # 角色名，如 'interviewer'
    content: Mapped[str] = mapped_column(Text) # 具体的 Prompt 内容