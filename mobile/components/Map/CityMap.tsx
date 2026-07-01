import MapView from "./MapView";
import { Stop } from "../../services/routing/searchStops";

type Props = {
  userLocation: {
    latitude: number;
    longitude: number;
  } | null;
  stops: Stop[];
  selectedStop: Stop | null;
};

export function CityMap({ userLocation, stops, selectedStop }: Props) {
  return (
    <MapView
      userLocation={userLocation}
      stops={stops}
      selectedStop={selectedStop}
    />
  );
}