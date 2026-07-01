import { Text, TextInput, TouchableOpacity, View } from "react-native";
import { Stop } from "../../services/routing/searchStops";

type Props = {
  value: string;
  onChange: (text: string) => void;
  stops: Stop[];
  onStopPress: (stop: Stop) => void;
  compact?: boolean;
  title?: string;
};

function distanceLabel(stop: Stop) {
  if (stop.distance_m === undefined) return "";

  if (stop.distance_m < 1000) {
    return `${Math.round(stop.distance_m)} m`;
  }

  return `${(stop.distance_m / 1000).toFixed(1)} km`;
}

function servicesLabel(stop: Stop) {
  if (!stop.services) return "";

  const parts: string[] = [];

  if (stop.services.metro?.length) {
    parts.push(`Metro ${stop.services.metro.join(", ")}`);
  }

  if (stop.services.tram?.length) {
    parts.push(`Tram ${stop.services.tram.join(", ")}`);
  }

  if (stop.services.bus?.length) {
    parts.push(`Bus ${stop.services.bus.join(", ")}`);
  }

  if (stop.services.train?.length) {
    parts.push(`Rail ${stop.services.train.join(", ")}`);
  }

  return parts.join(" • ");
}

function StopRow({
  stop,
  onPress,
}: {
  stop: Stop;
  onPress: () => void;
}) {
  return (
    <TouchableOpacity
      activeOpacity={0.7}
      onPress={onPress}
      style={{
        paddingVertical: 14,
        borderBottomWidth: 1,
        borderBottomColor: "#EFEFEF",
      }}
    >
      <Text
        style={{
          fontSize: 18,
          fontWeight: "700",
          color: "#111",
        }}
      >
        {stop.name}
      </Text>

      {!!servicesLabel(stop) && (
        <Text
          numberOfLines={1}
          style={{
            marginTop: 4,
            fontSize: 13,
            color: "#6E6E73",
          }}
        >
          {servicesLabel(stop)}
        </Text>
      )}

      {!!distanceLabel(stop) && (
        <Text
          style={{
            marginTop: 4,
            fontSize: 13,
            color: "#9B9B9B",
          }}
        >
          {distanceLabel(stop)}
        </Text>
      )}
    </TouchableOpacity>
  );
}

export default function SearchCard({
  value,
  onChange,
  stops,
  onStopPress,
  compact = false,
  title,
}: Props) {
  return (
    <View>
      {!compact && (
        <Text
          style={{
            fontSize: 34,
            fontWeight: "800",
            color: "#111",
            marginBottom: 18,
            letterSpacing: -1,
          }}
        >
          {title ?? "Where to?"}
        </Text>
      )}

      <TextInput
        value={value}
        onChangeText={onChange}
        placeholder="Search destination"
        placeholderTextColor="#999"
        autoCorrect={false}
        autoCapitalize="none"
        style={{
          height: 56,
          borderRadius: 18,
          backgroundColor: "#F4F4F2",
          paddingHorizontal: 18,
          fontSize: 18,
        }}
      />

      {stops.length > 0 && (
        <View style={{ marginTop: 16 }}>
          {stops.map((stop) => (
            <StopRow
              key={stop.id}
              stop={stop}
              onPress={() => onStopPress(stop)}
            />
          ))}
        </View>
      )}
    </View>
  );
}