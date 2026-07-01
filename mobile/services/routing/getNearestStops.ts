import { api } from "../api/client";
import { Stop } from "./searchStops";

export function getNearestStops(location: {
  latitude: number;
  longitude: number;
}) {
  const params = new URLSearchParams({
    lat: String(location.latitude),
    lon: String(location.longitude),
  });

  return api<Stop[]>(`/nearest?${params.toString()}`);
}