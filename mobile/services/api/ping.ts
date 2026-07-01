import { api } from "./client";

export interface PingResponse {
  status: string;
  message: string;
}

export function ping() {
  return api<PingResponse>("/ping");
}