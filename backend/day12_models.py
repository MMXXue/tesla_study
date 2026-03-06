# 你告诉 SQLAlchemy：“如果将来我要存数据，请按照这个规格（ID、视频ID、状态）来建表。
# 这里是我的模型文件,用于规范化alembic,让他作为SQLalchemy和postgres之间的翻译官


from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
import datetime

# 声明所有 ORM 模型共享的基类。
# 后续定义的表模型都应继承 Base，便于统一创建和管理数据表。
Base = declarative_base()

class PerceptionTask(Base):
    """感知任务表对应的 ORM 模型。

    该模型用于记录一次视频感知任务的核心信息：
    - 任务关联的视频 ID
    - 使用的模型版本
    - 推理置信度
    - 任务执行状态
    - 任务创建时间
    """
    __tablename__ = 'perception_tasks'  # 数据库里的表名

    # 新增的修改!!!!!用于测试
    processing_time = Column(Float)
    
    # 主键 ID：每条任务记录的唯一标识。
    id = Column(Integer, primary_key=True)

    # 视频 ID：标识本任务处理的是哪一个视频（必填）。
    video_id = Column(String(50), nullable=False)   # 视频 ID

    # 模型版本：记录执行该任务时所用 AI 模型版本。
    model_version = Column(String(20))              # AI 模型版本

    # 置信度评分：模型输出结果的可信程度（通常在 0~1 之间）。
    confidence_score = Column(Float)                # 置信度评分

    # 任务状态：默认 pending，可按流程变为 running / done。
    status = Column(String(20), default="pending")  # 任务状态 (pending/running/done)

    # 创建时间：记录任务创建时刻（默认使用 UTC 时间）。
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
