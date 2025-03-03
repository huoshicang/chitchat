import {ChatDatabase} from "../dataBase";

export const getChat = (req: Request): Response => {

  const db = new ChatDatabase();


  try {
    const users = db.select('chat', {
      fields: ['id', 'user', 'messageId', 'title', 'creationTime', 'modificationTime'],
      condition: 'WHERE isDelete = 0 ',
    });

    return new Response(JSON.stringify(users), {
      status: 200,
      headers: {
        "Content-Type": "application/json"
      },
    });

  } catch (error) {
    return new Response(JSON.stringify(error), {
      status: 404,
    });
  }


};
