# 给短剧推荐系统 写一个用户评论的校验器
# 评论内容 content 必须是字符串，且长度至少 10 个字。
# 评分 score 必须是 1 到 5 之间的整数。

from pydantic import BaseModel, Field

class Comment(BaseModel):
    id: int

    # 字符串用 min_length，数字才用 ge
    # content: str = Field(min_length=10)

    # 如果 JSON 里没有 content，就自动填入 "暂无评价"
    # content: str = Field(default="暂无评价", min_length=10)

    # 这里的 str | None 表示：可以是字符串，也可以是空（None）
    # default=None 表示如果不传，默认就是 None
    content: str | None = Field(default=None, min_length=10)

    score: int = Field(ge=1, le=5)


# 模拟从网络接收到的 JSON
json_data = '{"id": 101, "content": "这个短剧太精彩了，反转很多！", "score": 6}'

try:
    # 这一步是交给底层的 Rust 去快速解析
    comment_obj = Comment.model_validate_json(json_data)
except Exception as e:
    # 这里会报错，因为 score 是 6，超出了 le=5 的限制
    print("发现非法评分！")