import FingerprintJS from "@fingerprintjs/fingerprintjs";

export const getFingerprint = async (): Promise<string> => {
  const result = await FingerprintJS.load();
  const visitorId = await result.get();
  return visitorId.visitorId
}
