export function createSnowflakeGenerator(machineId: number = 123): string {
  if (machineId < 0 || machineId >= 4096) {
    throw new Error("计算机ID必须介于0和4095之间。");
  }

  let lastTimestamp: bigint = BigInt(0);
  let sequence: number = 0;

  return function generateId(): string {
    const currentTimestamp = BigInt(Math.floor(Date.now()));

    if (currentTimestamp < lastTimestamp) {
      throw new Error("时钟向后移动。拒绝生成ID。");
    }

    if (currentTimestamp === lastTimestamp) {
      sequence = (sequence + 1) % 2048;
    } else {
      sequence = 0;
    }

    lastTimestamp = currentTimestamp;

    const timestampPart = currentTimestamp << 23n;
    const machinePart = BigInt(machineId) << 11n;
    const sequencePart = BigInt(sequence);

    const id = timestampPart | machinePart | sequencePart;

    return id.toString();
  }();
}
