from starlette import status
from starlette.responses import JSONResponse

from config import setup_logger, get_logger

from database import MongoDB

setup_logger()

# 获取日志记录器
logger = get_logger(__name__)


def judgment_auth(request) -> JSONResponse:
    auth = False
    auth_header = request.headers.get("authorization")
    user = {}
    if auth_header and auth_header.startswith("Bearer "):
        try:
            user_id = auth_header.replace("Bearer ", '')
            logger.info(f"开始处理用户认证请求，用户ID：{user_id}")  # 新增日志

            db = MongoDB()
            # 查询用户信息
            user, error_message = db.find_one('users', {'user_id': user_id},
                                              {})()

            # 用户不存在，创建新用户
            if user:
                logger.debug(f"用户已存在，用户信息：{user}")  # 查询成功日志
            else:

                # 菜单
                siderContent = {
                    "display": True,
                    "id": True,
                    "share": True,
                    "archive": True
                }

                # 消息
                messageConfig = {
                    "showAll": True,
                    "showModel": True,
                    "showPromptTokens": True,
                    "showCompletionTokens": True,
                    "showTotalTokens": True,
                    "showReasoningTokens": True,
                    "showTime": True,
                    "think": True,
                }

                promptsConfig = {
                    "share": True
                }

                user = db.insert_one('users', {
                    'user_id': user_id,
                    "setting": user_id,
                    "siderContent": siderContent,
                    "messageConfig": messageConfig,
                    "promptsConfig": promptsConfig,
                })()
                logger.info(f"创建新用户：{user_id}，状态为：{user}")

            auth = True
            logger.info(f"用户 {user_id} 认证成功")  # 认证成功日志

            user, error_message = db.find_one('users', {'user_id': user_id},
                                              {})()

        except Exception as e:
            logger.error(f"数据库操作失败: {e}", exc_info=True)
            logger.error(f"认证失败的头信息：{auth_header}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={
            "Set-Cookie": f"auth={auth}; Path=/; HttpOnly"
        },
        content={
            "status_code": status.HTTP_200_OK,
            "message": "is running...",
            "data": user,
        }
    )
