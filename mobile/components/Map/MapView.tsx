import { Camera, Map, ViewAnnotation } from "@maplibre/maplibre-react-native";
import { Text, View } from "react-native";
import { Stop } from "../../services/routing/searchStops";

type Props = {
  userLocation: {
    latitude: number;
    longitude: number;
  } | null;
  stops?: Stop[];
  selectedStop: Stop | null;
};

const PRAGUE_CENTER: [number, number] = [14.4378, 50.0755];

export default function MapView({
  userLocation,
  stops = [],
  selectedStop,
}: Props) {
  const center: [number, number] = selectedStop
    ? [Number(selectedStop.lon), Number(selectedStop.lat)]
    : userLocation
    ? [userLocation.longitude, userLocation.latitude]
    : PRAGUE_CENTER;

  const zoom = selectedStop ? 17 : userLocation ? 15 : 13;

  return (
    <Map
      key={`${center[0]}-${center[1]}-${zoom}`}
      style={{ flex: 1 }}
      mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
      logo={false}
      attribution={false}
      compass={false}
    >
      <Camera
        initialViewState={{
          center,
          zoom,
        }}
      />

      {userLocation && (
        <ViewAnnotation
          lngLat={[userLocation.longitude, userLocation.latitude]}
          anchor="center"
        >
          <View
            style={{
              width: 18,
              height: 18,
              borderRadius: 9,
              backgroundColor: "#111",
              borderWidth: 4,
              borderColor: "#fff",
            }}
          />
        </ViewAnnotation>
      )}

      {stops.map((stop) => {
        const isSelected = selectedStop?.id === stop.id;

        return (
          <ViewAnnotation
            key={String(stop.id)}
            lngLat={[Number(stop.lon), Number(stop.lat)]}
            anchor="center"
          >
            <View style={{ alignItems: "center" }}>
              <View
                style={{
                  width: isSelected ? 20 : 12,
                  height: isSelected ? 20 : 12,
                  borderRadius: 99,
                  backgroundColor: isSelected ? "#111" : "#fff",
                  borderWidth: 3,
                  borderColor: "#111",
                }}
              />

              {isSelected && (
                <Text
                  style={{
                    marginTop: 4,
                    fontSize: 12,
                    fontWeight: "700",
                    color: "#111",
                    backgroundColor: "rgba(255,255,255,0.95)",
                    paddingHorizontal: 8,
                    paddingVertical: 3,
                    borderRadius: 10,
                  }}
                >
                  {stop.name}
                </Text>
              )}
            </View>
          </ViewAnnotation>
        );
      })}
    </Map>
  );
}