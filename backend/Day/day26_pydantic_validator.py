
# 错误捕获与分析

from pydantic import BaseModel, Field, ValidationError

class Sensor(BaseModel):
    id: int
    val: float = Field(gt=0)

data = {"id": "ABC", "val": -10.5} # 两处错误：id不是数字，val小于0

try:
    Sensor(**data)
except ValidationError as e:
    # 1. 打印人类可读的错误
    print(e.errors()) 
    # 2. 这里的 e.errors() 会返回一个列表，告诉你：
    #    - loc: ('id',), msg: 'Input should be a valid integer'
    #    - loc: ('val',), msg: 'Input should be greater than 0'