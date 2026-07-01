import { api } from "../api/client";

export interface RouteResponse {
  success: boolean;
}

export async function getRoute() {
  return api<RouteResponse>("/route");
}