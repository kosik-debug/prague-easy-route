import { Text, TouchableOpacity, View } from "react-native";
import SearchCard from "./SearchCard";
import { Stop } from "../../services/routing/searchStops";

type Props = {
  searchQuery: string;
  onSearchChange: (text: string) => void;
  stops: Stop[];
  selectedStop: Stop | null;
  onStopPress: (stop: Stop) => void;
};

function serviceText(stop: Stop) {
  const s = stop.services;

  if (!s) return "";

  return [
    s.metro?.length ? `Metro ${s.metro.join(", ")}` : null,
    s.tram?.length ? `Tram ${s.tram.join(", ")}` : null,
    s.bus?.length ? `Bus ${s.bus.join(", ")}` : null,
    s.train?.length ? `Rail ${s.train.join(", ")}` : null,
  ]
    .filter(Boolean)
    .join(" • ");
}

function distanceLabel(stop: Stop) {
  if (!stop.distance_m) return "";

  return stop.distance_m < 1000
    ? `${Math.round(stop.distance_m)} m away`
    : `${(stop.distance_m / 1000).toFixed(1)} km away`;
}

export default function BottomSheet({
  searchQuery,
  onSearchChange,
  stops,
  selectedStop,
  onStopPress,
}: Props) {
  return (
    <View
      style={{
        backgroundColor: "rgba(255,255,255,0.97)",
        borderRadius: 34,
        padding: 18,
        shadowColor: "#000",
        shadowOpacity: 0.14,
        shadowRadius: 34,
        shadowOffset: {
          width: 0,
          height: 12,
        },
      }}
    >
      <View
        style={{
          width: 42,
          height: 5,
          borderRadius: 3,
          backgroundColor: "#D1D1D1",
          alignSelf: "center",
          marginBottom: 18,
        }}
      />

      {selectedStop ? (
        <View>
          <Text
            style={{
              fontSize: 30,
              fontWeight: "800",
              color: "#111",
              letterSpacing: -0.8,
            }}
          >
            {selectedStop.name}
          </Text>

          {!!serviceText(selectedStop) && (
            <Text
              style={{
                marginTop: 6,
                fontSize: 14,
                color: "#6E6E73",
                lineHeight: 20,
              }}
            >
              {serviceText(selectedStop)}
            </Text>
          )}

          {!!distanceLabel(selectedStop) && (
            <Text
              style={{
                marginTop: 4,
                fontSize: 13,
                color: "#9A9A9A",
              }}
            >
              {distanceLabel(selectedStop)}
            </Text>
          )}

          <View style={{ flexDirection: "row", gap: 10, marginTop: 20 }}>
            <TouchableOpacity
              style={{
                flex: 1,
                height: 54,
                borderRadius: 18,
                backgroundColor: "#111",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Text style={{ color: "#fff", fontSize: 16, fontWeight: "800" }}>
                Navigate
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={{
                width: 54,
                height: 54,
                borderRadius: 18,
                backgroundColor: "#F4F4F2",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Text style={{ color: "#111", fontSize: 20, fontWeight: "800" }}>
                …
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      ) : (
        <SearchCard
          value={searchQuery}
          onChange={onSearchChange}
          stops={stops}
          onStopPress={onStopPress}
          compact={searchQuery.length >= 2}
          title={searchQuery.length >= 2 ? undefined : "Nearby stops"}
        />
      )}
    </View>
  );
}