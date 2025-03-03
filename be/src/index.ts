import {getChat} from './api/getChat.ts'
import {wordApiRoutes} from './api/Word.ts'
import {dataApiRoutes} from './api/data.ts'

interface RouteMap {
  [key: string]: (request: Request) => Promise<Response> | Response;
}

export const routes: RouteMap = {
  "/running": () => new Response("is running..."),
  '/getChat': getChat,
  '/word': wordApiRoutes,
  //'/data': dataApiRoutes,
  // 添加更多的路由...
};
