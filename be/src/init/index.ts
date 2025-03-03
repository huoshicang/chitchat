import {ChatDatabase} from "../dataBase";
import {createSnowflakeGenerator} from "../tool/SnowflakeIdGenerator.ts";
import {initData} from "./dataBaseTable.ts";

const db = new ChatDatabase();

//for (const i in initData) {
//  db.createTable(i, initData[i as keyof typeof initData]);
//}


//db.insert('chat', {
//  id: createSnowflakeGenerator(),
//  user: 'Alice',
//  userId: 123,
//  messageId: 123
//});

//const users = db.select('chat', {
//  condition: "WHERE user = ?",
//  params: ['Alice']
//});
//db.close()
//console.log(users);
