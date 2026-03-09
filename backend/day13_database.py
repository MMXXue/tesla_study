from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from day12_models import Base

# 1. 数据库连接地址
# 根据你 Docker 的配置：用户名 postgres, 密码 password, 数据库名 postgres
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

# 2. 创建 SQLAlchemy 引擎
# 这相当于连接数据库的“总管道”
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # pool_size 和 max_overflow 是为了应对高并发请求，符合你 Tesla 工程师的目标
    pool_size=10, 
    max_overflow=20
)

# 3. 创建 SessionLocal 类
# 这是一个“工厂”，每次调用它都会产生一个新的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. 核心：get_db 依赖项 (这就是你问的“管家”)
def get_db():
    """
    这是一个生成器函数。
    每次 API 请求开始时，它会创建一个数据库连接。
    请求结束后，它会自动关闭连接。
    """
    db = SessionLocal() # 创建连接
    try:
        yield db       # 把连接“借给” API 函数使用
    finally:
        db.close()     # 无论成功还是报错，最后一定关闭连接，释放资源