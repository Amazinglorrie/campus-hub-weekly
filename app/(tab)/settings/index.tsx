// Week 9: Local Storage — MODIFIED (added persistence for notifications toggle)
import React, { useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import AppCard from "../../../components/AppCard";
import { theme } from "../../../styles/theme";
import * as storage from "../../../lib/storage";
import { STORAGE_KEYS } from "../../../lib/storage";

export default function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  // Load saved notification preference on mount
  useEffect(() => {
    async function loadNotifications() {
      const saved = await storage.get<boolean>(STORAGE_KEYS.NOTIFICATIONS);
      if (saved !== null) {
        setNotifications(saved);
      }
      setIsLoading(false);
    }
    loadNotifications();
  }, []);

  // Save notification preference when toggled
  async function handleToggle(value: boolean) {
    setNotifications(value);
    await storage.set(STORAGE_KEYS.NOTIFICATIONS, value);
  }

  if (isLoading) {
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
}

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
