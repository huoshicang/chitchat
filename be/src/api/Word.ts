export const wordApiRoutes = (req: Request): Response | Promise<Response> => {

  function getRandomInt(min: number, max: number) {
    min = Math.ceil(min); // 向上取整，确保min为整数
    max = Math.floor(max); // 向下取整，确保max为整数
    return Math.floor(Math.random() * (max - min + 1)) + min; // 包括最大值和最小值
  }


  Bun.sleepSync(1000);

  return new Response('Word, API!', {status: 200});
};
