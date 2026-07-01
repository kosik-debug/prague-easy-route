import { api } from "../api/client";

export type TransportMode = "metro" | "tram" | "bus" | "train";

export type StopServices = {
  metro?: string[];
  tram?: string[];
  bus?: string[];
  train?: string[];
};

export interface Stop {
  id: string;
  name: string;
  lat: number;
  lon: number;
  distance_m?: number;
  modes?: TransportMode[];
  hub?: boolean;
  services?: StopServices;
}

export async function searchStops(
  query: string,
  location?: { latitude: number; longitude: number } | null
) {
  const params = new URLSearchParams({ query });

  if (location) {
    params.append("lat", String(location.latitude));
    params.append("lon", String(location.longitude));
  }

  const stops = await api<Stop[]>(`/search-stop?${params.toString()}`);

  console.log(JSON.stringify(stops[0], null, 2));

  return stops;
}