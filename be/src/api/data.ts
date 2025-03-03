import {Database} from "bun:sqlite";

export const dataApiRoutes = (req: Request): Response | Promise<Response> => {

  const db = new Database(":memory:");
  const query = db.query("select 'Hello world' as message;");
  console.log(query.get()) // => { message: "Hello world" }


  return new Response(JSON.stringify({message: "Hello, API!"}), {
    status: 200,
    headers: {
      "Content-Type": "application/json"
    },
  });
};
