import { useEffect, useState } from "react";
import {
  KeyboardAvoidingView,
  Platform,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

import { CityMap } from "../components/Map/CityMap";
import BottomSheet from "../components/BottomSheet/BottomSheet";
import { useUserLocation } from "../hooks/useUserLocation";
import { ping } from "../services/api/ping";
import { searchStops, Stop } from "../services/routing/searchStops";
import { getNearestStops } from "../services/routing/getNearestStops";

export default function HomeScreen() {
  const userLocation = useUserLocation();

  const [searchQuery, setSearchQuery] = useState("");
  const [stops, setStops] = useState<Stop[]>([]);
  const [selectedStop, setSelectedStop] = useState<Stop | null>(null);

  useEffect(() => {
    ping()
      .then((res) => console.log("PING:", res))
      .catch((err) => console.log("PING ERROR:", err));
  }, []);

  useEffect(() => {
    if (!userLocation) return;

    if (searchQuery.length >= 2) return;

    getNearestStops(userLocation)
      .then((result) => {
        setStops(Array.isArray(result) ? result : []);
      })
      .catch((err) => console.log("NEAREST ERROR:", err));
  }, [userLocation, searchQuery]);

  useEffect(() => {
    if (searchQuery.length < 2) {
      setSelectedStop(null);
      return;
    }

    const timeout = setTimeout(async () => {
      try {
        const result = await searchStops(searchQuery, userLocation);
        setStops(Array.isArray(result) ? result : []);
      } catch (err) {
        console.log("SEARCH ERROR:", err);
      }
    }, 300);

    return () => clearTimeout(timeout);
  }, [searchQuery, userLocation]);

  function handleSearchChange(text: string) {
    setSearchQuery(text);
    setSelectedStop(null);
  }

  function handleStopPress(stop: Stop) {
    setSelectedStop(stop);
    setSearchQuery(stop.name);
    setStops([stop]);
  }

  return (
    <View style={{ flex: 1 }}>
      <CityMap
        userLocation={userLocation}
        stops={stops}
        selectedStop={selectedStop}
      />

      <TouchableOpacity
        onPress={() => {
          setSelectedStop(null);
          setSearchQuery("");
        }}
        style={{
          position: "absolute",
          top: 60,
          right: 16,
          width: 52,
          height: 52,
          borderRadius: 26,
          backgroundColor: "rgba(255,255,255,0.95)",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 100,
        }}
      >
        <Text style={{ fontSize: 24, fontWeight: "700" }}>⌖</Text>
      </TouchableOpacity>

      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={{
          position: "absolute",
          left: 14,
          right: 14,
          bottom: 14,
        }}
      >
        <BottomSheet
          searchQuery={searchQuery}
          onSearchChange={handleSearchChange}
          stops={stops}
          selectedStop={selectedStop}
          onStopPress={handleStopPress}
        />
      </KeyboardAvoidingView>
    </View>
  );
}