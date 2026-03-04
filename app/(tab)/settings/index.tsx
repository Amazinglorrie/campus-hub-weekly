// Week 9: Local Storage — MODIFIED (added persistence for notifications toggle)
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import AppCard from "../../../components/AppCard";
import { theme } from "../../../styles/theme";
import * as storage from "../../../lib/storage";
import { STORAGE_KEYS } from "../../../lib/storage";

const Settings = () => {
  const [notifications, setNotifications] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  // Load saved notification preference on mount
  useEffect(() => {
    // Define an async function to load the value since useEffect can't be async
    const loadNotifications = async () => {
      // Try to load saved value from storage, if it exists
      const saved = await storage.get<boolean>(STORAGE_KEYS.NOTIFICATIONS);
      if (saved !== null) {
        // If we have a saved value, use it to set the state
        setNotifications(saved);
      }
      setIsLoading(false);
    };
    // Call the async function to load notifications
    loadNotifications();
  }, []);

  // Save notification preference when toggled
  const handleToggle = async (value: boolean) => {
    setNotifications(value);
    await storage.set(STORAGE_KEYS.NOTIFICATIONS, value);
  };

  if (isLoading) {
    // Show a loading indicator while we load the saved preference
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Settings</Text>

      <AppCard
        title="Notifications"
        subtitle="Enable app notifications"
        right={
          // The Switch component calls handleToggle when toggled, which updates state and saves the new value to storage
          <Switch value={notifications} onValueChange={handleToggle} />
        }
      />

      <Pressable onPress={() => router.push("/(tab)/settings/profile")}>
        <AppCard
          title="Account"
          subtitle="Update profile settings"
          right={
            <Ionicons
              name="chevron-forward"
              size={20}
              color={theme.colors.muted}
            />
          }
        />
      </Pressable>
    </View>
  );
};

export default Settings;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: theme.spacing.screen,
    backgroundColor: theme.colors.bg,
  },
  h1: {
    fontSize: 22,
    fontWeight: "800",
    marginBottom: 12,
    color: theme.colors.text,
  },
});
