import { Text, TouchableOpacity, View } from "react-native";

export default function RouteRecommendation() {
  return (
    <View style={{ marginTop: 22 }}>
      <Text
        style={{
          fontSize: 13,
          color: "#6E6E73",
          fontWeight: "600",
          marginBottom: 8,
        }}
      >
        Recommended for you
      </Text>

      <Text
        style={{
          fontSize: 28,
          fontWeight: "800",
          color: "#111",
          letterSpacing: -0.7,
          marginBottom: 14,
        }}
      >
        Transit is fastest today
      </Text>

      <View style={{ flexDirection: "row", gap: 12 }}>
        <View
          style={{
            flex: 1,
            borderRadius: 18,
            borderWidth: 1,
            borderColor: "#111",
            padding: 16,
          }}
        >
          <Text style={{ fontSize: 14, fontWeight: "700" }}>Transit</Text>
          <Text style={{ fontSize: 28, fontWeight: "800", marginTop: 8 }}>
            31 min
          </Text>
          <Text style={{ fontSize: 13, color: "#6E6E73", marginTop: 4 }}>
            Recommended
          </Text>
        </View>

        <View
          style={{
            flex: 1,
            borderRadius: 18,
            borderWidth: 1,
            borderColor: "#E5E5E5",
            padding: 16,
          }}
        >
          <Text style={{ fontSize: 14, fontWeight: "700" }}>Drive</Text>
          <Text style={{ fontSize: 28, fontWeight: "800", marginTop: 8 }}>
            49 min
          </Text>
          <Text style={{ fontSize: 13, color: "#6E6E73", marginTop: 4 }}>
            Traffic
          </Text>
        </View>
      </View>

      <TouchableOpacity
        style={{
          marginTop: 18,
          height: 56,
          borderRadius: 18,
          backgroundColor: "#111",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Text style={{ color: "#fff", fontSize: 16, fontWeight: "800" }}>
          Show route
        </Text>
      </TouchableOpacity>
    </View>
  );
}