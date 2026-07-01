import { View } from "react-native";

export function RoadLayer() {
  return (
    <>
      {/* Magistrála */}
      <View
        style={{
          position: "absolute",
          top: 130,
          left: -80,
          right: -80,
          height: 28,
          backgroundColor: "#ffffff",
          borderRadius: 16,
          transform: [{ rotate: "-18deg" }],
        }}
      />

      {/* Jižní spojka */}
      <View
        style={{
          position: "absolute",
          top: 290,
          left: -120,
          right: -120,
          height: 24,
          backgroundColor: "#ffffff",
          borderRadius: 16,
          transform: [{ rotate: "24deg" }],
        }}
      />

      {/* Kolmá komunikace */}
      <View
        style={{
          position: "absolute",
          top: 430,
          left: 110,
          width: 20,
          height: 340,
          borderRadius: 16,
          backgroundColor: "#ffffff",
          transform: [{ rotate: "8deg" }],
        }}
      />
    </>
  );
}