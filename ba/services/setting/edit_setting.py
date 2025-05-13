from bson import ObjectId
from schemas import SettingsResponse, SiderContent, MessageConfig
from pymongo.errors import PyMongoError
from starlette import status
from config import get_logger
from database import MongoDB

logger = get_logger(__name__)


async def edit_setting(authorization: str, setting: str, _id: str, siderContent: SiderContent, messageConfig: MessageConfig,
             ) -> SettingsResponse:
    """
    修改设置
    :param authorization: 认证id
    :param setting: 设置
    :param _id: kuid
    :param siderContent: 侧边栏
    :param messageConfig: 消息
    :return:
    """
    try:
        db = MongoDB()
        users, error_message = db.update_one("users",
                                             {"user_id": authorization, "_id": ObjectId(_id)},
                                             {
                                                 "$set": {
                                                     "setting": setting,
                                                     "siderContent": dict(siderContent),
                                                     "messageConfig": dict(messageConfig),
                                                 }
                                             })()

        if error_message != "":
            logger.error(f" {authorization} 修改设置时发生错误: {error_message}")
            return SettingsResponse(data={}, status_code=status.HTTP_400_BAD_REQUEST, message=error_message)

        logger.info(f"修改 {authorization} 的设置成功")
        return SettingsResponse(data=users, status_code=status.HTTP_200_OK, message="成功")

    except PyMongoError as e:
        logger.error(f"数据库错误: {str(e)}")
        return SettingsResponse(data={}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="数据库服务不可用")

    except Exception as e:
        logger.error(f"获取设置时发生未知错误: {str(e)}")
        return SettingsResponse(data={}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message="服务器内部错误")
