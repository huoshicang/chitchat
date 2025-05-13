from typing import List

from schemas import MoldeResponse, AiConfig, ModelConfig
from pymongo.errors import PyMongoError
from starlette import status
from config import get_logger
from database import MongoDB

logger = get_logger(__name__)


async def new_model(authorization: str, name: str, ai_var: AiConfig, model_var: ModelConfig,
                    extra: List[dict]) -> MoldeResponse:
    """
    新增模型
    :param authorization: 认证id
    :param name: 模型名称
    :param ai_var: ai设置
    :param model_var: 模型设置
    :param extra: 额外参数
    :return:
    """
    try:
        db = MongoDB()

        model, error_message = db.insert_one("model",
                                             {
                                                 "name": name,
                                                 "ai_var": dict(ai_var),
                                                 "model_var": dict(model_var),
                                                 "extra": extra,
                                                 "user_id": authorization,
                                                 "share": False,
                                             })()


        if error_message != "":
            logger.error(f" {authorization} 添加模型时发生错误: {error_message}")
            return MoldeResponse(data={}, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"添加用户 {authorization} 的模型成功")
        return MoldeResponse(data={
            "model_id": str(model.inserted_id)
        }, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return MoldeResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"获取模型时发生未知错误: {str(e)}")
        return MoldeResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
