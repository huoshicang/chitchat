from pymongo.errors import PyMongoError
from starlette import status
from bson import ObjectId
from config import get_logger
from database import MongoDB
from schemas import MoldeResponse

logger = get_logger(__name__)


async def share_model(authorization: str, model_id: str) -> MoldeResponse:
    """
    分享模型记录
    :param authorization: 认证id
    :param model_id: 模型记录id
    :return:
    """
    try:
        db = MongoDB()

        find_model, _ = db.find_one("model", {"user_id": authorization, "_id": ObjectId(model_id)},
                              {"share": True, "_id": False})()

        model, error_message = db.update_one("model",
                                            {"user_id": authorization, "_id": ObjectId(model_id)},
                                            {"$set": {"share": not find_model.get("share", True)}
                                             })()

        if error_message != "":
            logger.error(f"分享 {authorization} 的记录时发生错误: {error_message}")
            return MoldeResponse(data=model, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"{model_id} 的模型分享成功")
        return MoldeResponse(data=model, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return MoldeResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"分享记录时发生未知错误: {str(e)}")
        return MoldeResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
