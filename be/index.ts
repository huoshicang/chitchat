import {serve} from "bun"
import {routes} from "./src";
import pino from 'pino';

const logger = pino();

const server = serve({
  port: 9000,
  async fetch(request) {
    const url = new URL(request.url);
    const start = Date.now();


    if (request.url === `http://localhost:${this.port}/ws` && server.upgrade(request)) {
      // 如果升级成功，返回 undefined 以避免发送响应
      return;
    }

    // 先尝试处理路由
    const handler = routes[url.pathname];
    if (handler) {
      const response = await handler(request);
      logger.info(`${request.method} ${url.pathname} - ${response.status} - ${Date.now() - start}ms`);
      return response;
    }

    // 如果没有匹配的路由，尝试从 dist 文件夹中提供静态文件
    try {
      let filePath = `./dist${url.pathname}`;

      // 如果请求的是根路径，默认返回 index.html
      if (url.pathname === "/") {
        filePath = "./dist/index.html";
      }

      // 检查文件是否存在
      const file = Bun.file(filePath);
      if (await file.exists()) {
        return new Response(file);
      } else {
        // 文件不存在，返回 404
        const response = new Response("Not Found", {status: 404});
        logger.info(`${request.method} ${url.pathname} - ${response.status} - ${Date.now() - start}ms`);
        return response;
      }
    } catch (error) {
      // 捕获其他错误，返回 500
      const response = new Response("Internal Server Error", {status: 500});
      logger.error(`${request.method} ${url.pathname} - ${response.status} - ${Date.now() - start}ms - ${error}`);
      return response;
    }
  },
  websocket: {
    // 当 WebSocket 连接建立时调用
    open(ws) {
      console.log("WebSocket连接已打开");
      for (const i of "欢迎使用WebSocket服务器!") {
        ws.send(i);
      }

    },

    // 当收到 WebSocket 消息时调用
    message(ws, message) {
      console.log("Received message:", message);
      // 回显收到的消息
      ws.send(`You said: ${message}`);
      ws.close()
    },

    // 当 WebSocket 连接关闭时调用
    close(ws, code, message) {},

    // 当 WebSocket 准备好接收更多数据时调用
    drain(ws) {
      console.log("WebSocket is ready to receive more data");
    },
  },

})


console.log(`监听在 http://localhost:${server.port}`);
console.log("\n路由地址:");
for (const item in routes) {
  console.log(`http://localhost:${server.port}${item}`);
}


