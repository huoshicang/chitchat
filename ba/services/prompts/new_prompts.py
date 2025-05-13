from schemas import PromptsResponse
from pymongo.errors import PyMongoError
from starlette import status
from config import get_logger
from database import MongoDB

logger = get_logger(__name__)


async def new_prompts(authorization: str,  title: str, content: str, share: bool) -> PromptsResponse:
    """
    新增预设
    :param authorization: 认证id
    :param title: 标题
    :param content: 内容
    :param share: 分享
    :return:
    """
    try:
        db = MongoDB()

        prompts, error_message = db.insert_one("prompts",
                                             {
                                                 "title": title,
                                                 "content": content,
                                                 "share": share,
                                                 "user_id": authorization,
                                             })()


        if error_message != "":
            logger.error(f" {authorization} 添加预设时发生错误: {error_message}")
            return PromptsResponse(data={}, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"添加用户 {authorization} 的预设成功")
        return PromptsResponse(data={
            "prompts_id": str(prompts.inserted_id)
        }, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return PromptsResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"获取预设时发生未知错误: {str(e)}")
        return PromptsResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
