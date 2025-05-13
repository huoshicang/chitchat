from bson import ObjectId
from schemas import PromptsResponse
from pymongo.errors import PyMongoError
from starlette import status
from config import get_logger
from database import MongoDB

logger = get_logger(__name__)


async def edit_prompts(authorization: str, title: str, content: str, prompts_id:str) -> PromptsResponse:
    """
    修改模型
    :param authorization: 认证id
    :param prompts_id: 预设id
    :param title: 标题
    :param content: 内容
    :return:
    """
    try:
        db = MongoDB()
        model, error_message = db.update_one("prompts",
                                             {"user_id": authorization, "_id": ObjectId(prompts_id)},
                                             {
                                                 "$set": {
                                                     "title": title,
                                                     "content": content,
                                                 }
                                             })()

        if error_message != "":
            logger.error(f" {authorization} 修改模型时发生错误: {error_message}")
            return PromptsResponse(data={}, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"修改 {authorization} 的模型成功")
        return PromptsResponse(data=model, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return PromptsResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"获取修改时发生未知错误: {str(e)}")
        return PromptsResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
