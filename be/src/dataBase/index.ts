import path from 'path';
import {Database} from "bun:sqlite";
import dayjs from "dayjs";

/**
 * ChatDatabase 类用于管理 SQLite 数据库连接和操作。
 */
export class ChatDatabase {
  // 私有属性，用于存储数据库连接实例
  private db: Database;
  // 私有只读属性，用于存储数据库文件名
  private readonly database: string = "chat.sqlite"

  /**
   * 检查 SQL 语句是否合法
   * @param sql 需要检查的 SQL 语句
   * @returns 如果合法返回 true，否则返回 false
   */
  private isSqlValid(sql: string): boolean {
    // 定义允许的关键字（白名单）
    const allowedKeywords = [
      'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'JOIN', 'ON',
      'AND', 'OR', 'ORDER BY', 'GROUP BY', 'LIMIT', 'VALUES', 'SET', 'INTO'
    ];

    // 定义不允许的字符或模式（黑名单）
    const forbiddenPatterns = [
      /;.*--/, // 禁止分号和注释
      /[\s;]DROP\s/i, // 禁止 DROP 操作
      /[\s;]TRUNCATE\s/i, // 禁止 TRUNCATE 操作
      /[\s;]ALTER\s/i, // 禁止 ALTER 操作
      /[\s;]EXEC\s/i, // 禁止 EXEC 操作
      /[\s;]UNION\s/i, // 禁止 UNION 操作
      /[\s;]--\s/, // 禁止单行注释
      /\/\*.*\*\//, // 禁止多行注释
      ///['"`]/, // 禁止引号
    ];

    // 检查是否包含不允许的模式
    for (const pattern of forbiddenPatterns) {
      if (pattern.test(sql)) {
        console.error('SQL 语句包含非法模式:', pattern);
        return false;
      }
    }

    // 检查是否使用了允许的关键字
    const upperSql = sql.toUpperCase();
    const hasValidKeyword = allowedKeywords.some(keyword => upperSql.includes(keyword));
    if (!hasValidKeyword) {
      console.error('SQL 语句未包含任何允许的关键字');
      return false;
    }

    // 如果通过所有检查，则认为 SQL 语句合法
    return true;
  }

  /**
   * 构造函数，初始化数据库连接并设置日志模式为 WAL。
   */
  constructor() {
    // 创建一个新的数据库连接实例
    this.db = new Database(path.join(path.join(__dirname, this.database)));
    // 设置数据库的日志模式为 WAL（Write-Ahead Logging）
    this.db.exec("PRAGMA journal_mode = WAL;");
  }

  /**
   * 创建表
   * @param tableName 表名
   * @param columns 列定义数组
   */
  createTable(tableName: string, columns: string[]): void {
    // 将列定义数组转换为逗号分隔的字符串
    const columnDefinitions = columns.join(', ');

    // 构建创建表的 SQL 语句
    const sql = `CREATE TABLE IF NOT EXISTS ${tableName} (${columnDefinitions})`;

    // 检查 SQL 语句是否合法
    if (!this.isSqlValid(sql)) {}

    // 执行 SQL 语句
    this.db.prepare(sql).run();
  }

  /**
   * 插入数据
   * @param tableName 表名
   * @param data 要插入的数据对象
   */
  insert(tableName: string, data: Record<string, any>): void {
    // 获取数据对象的键名，并将其转换为逗号分隔的字符串
    const columns = Object.keys(data).join(', ');
    // 为每个键名生成一个占位符，并将其转换为逗号分隔的字符串
    const placeholders = Object.keys(data).map(() => '?').join(', ');
    // 获取数据对象的值，并将其转换为数组
    const values = Object.values(data);
    // 构建插入数据的 SQL 语句
    const sql = `INSERT INTO ${tableName} (${columns}) VALUES (${placeholders})`;

    // 检查 SQL 语句是否合法
    if (!this.isSqlValid(sql)) {
    }

    // 执行 SQL 语句
    this.db.prepare(sql).run(...values);
  }

  /**
   * 从指定表中查询数据
   * @param tableName - 表名
   * @param options - 查询选项
   * @param options.fields - 指定查询的字段
   * @param options.condition - 查询条件
   * @param options.params - 查询参数
   * @param options.orderBy - 排序字段
   * @param options.orderDirection - 排序方向 ASC 升序   DESC 降序
   * @param options.limit - 限制返回的记录数
   * @param options.offset - 偏移量
   * @returns 查询结果数组
   */
  select<T = any>(
    tableName: string,
    options: {
      fields?: string[];
      condition?: string;
      params?: any[];
      orderBy?: string;
      orderDirection?: 'ASC' | 'DESC';
      limit?: number;
      offset?: number;
    }
  ): T[] {

    // 构建查询语句 如果fields不为空则使用,拼接fields，否则使用*
    let sql = `SELECT ${options.fields ? options.fields.join(', ') : '*'} FROM ${tableName}`;

    // 如果有条件则拼接条件
    if (options.condition) {
      sql += ` ${options.condition}`;
    }

    // 如果有排序则拼接排序
    if (options.orderBy) {
      const direction = options.orderDirection || 'ASC';
      sql += ` ORDER BY ${options.orderBy} ${direction}`;
    }

    // 如果有限制则拼接限制
    if (options.limit !== undefined) {
      sql += ` LIMIT ${options.limit}`;
      if (options.offset !== undefined) {
        sql += ` OFFSET ${options.offset}`;
      }
    }

    // 检查 SQL 语句是否合法
    if (!this.isSqlValid(sql)) {
    }

    return this.db.prepare(sql).all(...(options.params || [])) as T[];
  }

  /**
   * 更新数据
   * @param tableName 表名
   * @param data 要更新的数据对象
   * @param condition 更新条件
   * @param params 更新参数
   */
  update(tableName: string, data: Record<string, any>, condition: string = '', params: any[] = []): void {
    // 构建 SET 子句，将数据对象的键值对转换为列名和占位符的形式

    data['modificationTime'] = dayjs().format("YYYY-MM-DD HH:mm:ss")

    const setClause = Object.keys(data).map(key => `${key} = ?`).join(', ');
    // 获取数据对象的值，并将其转换为数组
    const values = Object.values(data);
    // 构建更新数据的 SQL 语句
    const sql = `UPDATE ${tableName} SET ${setClause} ${condition}`;

    // 检查 SQL 语句是否合法
    if (!this.isSqlValid(sql)) {
    }

    // 执行 SQL 语句
    this.db.prepare(sql).run(...values, ...params);
  }

  /**
   * 删除数据
   * @param tableName 表名
   * @param condition 删除条件
   * @param params 删除参数
   */
  delete(tableName: string, condition: string = '', params: any[] = []): void {
    // 构建删除数据的 SQL 语句
    const sql = `DELETE FROM ${tableName} ${condition}`;

    // 检查 SQL 语句是否合法
    if (!this.isSqlValid(sql)) {
    }

    // 执行 SQL 语句
    this.db.prepare(sql).run(...params);
  }

  /**
   * 关闭数据库连接
   */
  close(): void {
    // 关闭数据库连接
    this.db.close();
  }

}


// 调用ChatDatabase
//const db = new ChatDatabase();

//// 创建表
//db.createTable('users', [
//  'id INTEGER PRIMARY KEY AUTOINCREMENT',
//  'name TEXT NOT NULL',
//  'email TEXT NOT NULL UNIQUE'
//]);
//
//// 插入数据
//db.insert('users', {name: 'Alice', email: 'alice@example.com'});
//db.insert('users', {name: 'Bob', email: 'bob@example.com'});

// 查询数据
//interface User {
//  id: number;
//  name: string;
//  email: string;
//}
//
//const users = db.select<User>('users', {
//  fields: ["id", "name"],
//  condition: 'WHERE name = ? AND email = ?',
//  params: ["Alice", "alice@example.com"]
//});
//db.close()
//console.log(users);
//
//// 更新数据
//db.update('users', {name: 'Alice Smith'}, 'WHERE id = ?', [1]);
//
//// 查询更新后的数据
//const updatedUsers = db.select<User>('users');
//console.log(updatedUsers);
//
//// 删除数据
//db.delete('users', 'WHERE id = ?', [2]);
//
//// 查询删除后的数据
//const remainingUsers = db.select<User>('users');
//console.log(remainingUsers);
//
//// 关闭数据库连接
//db.close();
//
////// 示例使用
////const sql1 = 'SELECT * FROM users WHERE id = 1';
////const sql2 = "DROP TABLE users; -- 恶意操作";
////const sql3 = "SELECT * FROM users WHERE name = 'admin' OR '1'='1'";
////
////console.log(chatDatabase.isSqlValid(sql1)); // true
////console.log(chatDatabase.isSqlValid(sql2)); // false
////console.log(chatDatabase.isSqlValid(sql3)); // false
//
