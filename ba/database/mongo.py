import json

from pymongo import MongoClient
from typing import Optional, Dict, List, Any
from datetime import datetime

from config.logging_config import get_logger

class MongoDB:
    _instance = None  # 用于单例模式，存储唯一的实例
    _URL = 'mongodb://mongodb:Miss177155@8.141.8.50:27017/'  # MongoDB连接字符串
    _client: MongoClient = None  # MongoClient实例，用于连接MongoDB
    _db = None  # 数据库实例
    _is_connected: bool = False  # 连接状态标记
    _last_result = None  # 存储上一次操作的结果
    _result = ""  # 存储上一次操作的结果
    _logger = get_logger(__name__)

    def __new__(cls):
        """
        重写__new__方法，实现单例模式，确保只有一个实例存在
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        初始化方法，创建MongoClient实例，并设置连接参数
        """
        if MongoDB._client is None:
            MongoDB._client = MongoClient(
                MongoDB._URL,
                serverSelectionTimeoutMS=5000,  # 服务器选择超时时间，单位：毫秒
                connectTimeoutMS=10000,  # 连接超时时间，单位：毫秒
                socketTimeoutMS=45000,  # 套接字超时时间，单位：毫秒
                maxPoolSize=50,  # 连接池最大连接数
                minPoolSize=5  # 连接池最小连接数
            )
        self._last_result = None

    @classmethod
    def get_instance(cls) -> 'MongoDB':
        """
        静态方法，获取唯一的MongoDB实例
        Returns:
            MongoDB: 唯一的MongoDB实例
        """
        if not cls._instance:
            cls._instance = MongoDB()
        return cls._instance

    def connect(self) -> 'MongoDB':
        """
        连接MongoDB数据库的方法，检查是否已连接，若未连接则进行连接
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if self._is_connected:
            return self
        try:
            self._db = self._client['chitchat']  # 选择数据库
            self._is_connected = True
            self._logger.info('成功连接到MongoDB')
        except Exception as e:
            self._logger.error(f'连接失败: {e}')
            self._is_connected = False
            raise Exception('数据库连接异常')
        return self

    def get_db(self) -> Any:
        """
        获取数据库实例的方法，检查是否已连接，若未连接则抛出异常
        Returns:
            Any: 数据库实例
        """
        if not self._is_connected:
            raise Exception('数据库未连接，请先调用connect()方法')
        return self._db

    def get_collection(self, collection_name: str) -> Any:
        """
        获取指定集合的方法，检查是否已连接，若未连接则抛出异常
        Args:
            collection_name (str): 要获取的集合名称
        Returns:
            Any: 指定集合的实例
        """
        if not self._is_connected:
            raise Exception('数据库未连接，请先调用connect()方法')
        return self._db[collection_name]

    def insert_one(self, collection_name: str, data: Dict[str, Any]) -> 'MongoDB':
        """
        插入单条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            data (Dict[str, Any]): 要插入的数据，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            document = {
                **data,
                'creation_time': datetime.now(),
                'modification_time': datetime.now(),
                'is_del': False
            }
            result = collection.insert_one(document)
            self._last_result = result
        except Exception as e:
            self._logger.error(f'插入数据失败: {e}')
            self._last_result = False
            self._result = str(e)
        return self

    def insert_many(self, collection_name: str, data: List[Dict[str, Any]]) -> 'MongoDB':
        """
        插入多条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            data (List[Dict[str, Any]]): 要插入的数据列表，每个元素为字典，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            documents = [
                {
                    **doc,
                    'creation_time': datetime.now(),
                    'modification_time': datetime.now(),
                    'is_del': False
                } for doc in data
            ]
            result = collection.insert_many(documents)
            self._last_result = result.acknowledged
        except Exception as e:
            self._logger.error(f'批量插入数据失败: {e}')
            self._last_result = False
            self._result = str(e)
        return self

    def find_one(self, collection_name: str, query: Dict[str, Any], options: Optional[Dict[str, bool]]=None) -> 'MongoDB':
        """
        查询单条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            query (Dict[str, Any]): 查询条件，键为字符串，值为任意类型
            options (Optional[Dict[str, bool]]): 可选的查询选项，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if options is None:
            options = {}
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            self._last_result = collection.find_one(query, options)
        except Exception as e:
            self._logger.error(f'查询数据失败: {e}')
            self._last_result = None
            self._result = str(e)
        return self

    def find(self, collection_name: str, query: Dict[str, Any], options: Optional[Dict[str, bool]]=None) -> 'MongoDB':
        """
        查询多条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            query (Dict[str, Any]): 查询条件，键为字符串，值为任意类型
            options (Optional[Dict[str, bool]]): 可选的查询选项，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if options is None:
            options = {}
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            cursor = collection.find(query, options)
            self._last_result = list(cursor)
        except Exception as e:
            self._logger.error(f'查询数据失败: {e}')
            self._last_result = []
            self._result = str(e)
        return self

    def update_one(self, collection_name: str, filter: Dict[str, Any], update: Dict[str, Any]) -> 'MongoDB':
        """
        更新单条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            filter (Dict[str, Any]): 更新条件，键为字符串，值为任意类型
            update (Dict[str, Any]): 更新操作，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            update_with_timestamp = {
                **update,
                '$set': {
                    **update.get('$set', {}),
                    'modification_time': datetime.now()
                }
            }
            result = collection.update_one(filter, update_with_timestamp)
            self._last_result = result.raw_result
        except Exception as e:
            self._logger.error(f'更新数据失败: {e}')
            self._last_result = False
            self._result = str(e)
        return self

    def update_many(self, collection_name: str, filter: Dict[str, Any], update: Dict[str, Any]) -> 'MongoDB':
        """
        更新多条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            filter (Dict[str, Any]): 更新条件，键为字符串，值为任意类型
            update (Dict[str, Any]): 更新操作，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            update_with_timestamp = {
                **update,
                '$set': {
                    **update.get('$set', {}),
                    'modification_time': datetime.now()
                }
            }
            result = collection.update_many(filter, update_with_timestamp)
            self._last_result = result.acknowledged
        except Exception as e:
            self._logger.error(f'批量更新数据失败: {e}')
            self._last_result = False
            self._result = str(e)
        return self

    def delete_one(self, collection_name: str, filter: Dict[str, Any]) -> 'MongoDB':
        """
        删除单条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            filter (Dict[str, Any]): 删除条件，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            result = collection.delete_one(filter)
            self._last_result = result.acknowledged
        except Exception as e:
            self._logger.error(f'删除数据失败: {e}')
            self._last_result = False
            self._result = str(e)
        return self

    def delete_many(self, collection_name: str, filter: Dict[str, Any]) -> 'MongoDB':
        """
        删除多条数据的方法，检查是否已连接，若未连接则尝试连接
        Args:
            collection_name (str): 目标集合名称
            filter (Dict[str, Any]): 删除条件，键为字符串，值为任意类型
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if not self._is_connected:
            self.connect()
        try:
            collection = self._db[collection_name]
            result = collection.delete_many(filter)
            self._last_result = result.acknowledged
        except Exception as e:
            self._logger.error(f'批量删除数据失败: {e}')
            self._last_result = False
            self._result = str(e)
        return self


    def close(self):
        """
        关闭MongoDB连接的方法
        Returns:
            MongoDB: 当前实例，用于链式调用
        """
        if self._client and self._is_connected:
            self._client.close()
            self._is_connected = False
            self._logger.info('连接已关闭')
    
    def get_result(self) -> Any:
        """
        获取上一次操作的结果
        Returns:
            Any: 上一次操作的结果
        """
        self.close()
        return self._last_result
    
    def __call__(self) -> Any:
        """
        使对象可调用，返回上一次操作的结果
        这样可以直接调用对象实例来获取结果，例如：db()
        Returns:
            Any: 上一次操作的结果
        """
        # 转换ObjectId为字符串
        if isinstance(self._last_result, dict) and '_id' in self._last_result:
            self._last_result['_id'] = str(self._last_result['_id'])
        elif isinstance(self._last_result, list):
            for doc in self._last_result:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
        return self._last_result, self._result