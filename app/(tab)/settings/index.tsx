// Week 8: Forms + Validation — NEW file (settings list with navigation to profile)
import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleSheet,
  Switch,
  Text,
  View,
} from "react-native";
import AppCard from "../../../components/AppCard";
import * as Storage from "../../../lib/storage";
import { theme } from "../../../styles/theme";

export default function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  //Load saved notitication preference on mount
  useEffect(() => {
    //Define an async function to laod the value since useEffect itself can't be async
    const loadNotifications = async () => {
      //Try to load the saved value from storage if it exists, otherwise default to true
      const saved = await Storage.get<boolean>(
        Storage.STORAGE_KEY.notifications,
      );
      setIsLoading(true);
      const savedNotifications = await Storage.get<boolean>(
        Storage.STORAGE_KEY.notifications,
      );
      if (savedNotifications !== null) {
        //if we have a saved value, use it to set the state
        setNotifications(savedNotifications);
      }
      setIsLoading(false); //turning off the spinner after loading is done
    };

    loadNotifications();
  }, []);

  const handleToggle = async (value: boolean) => {
    setNotifications(value);
    await Storage.set(Storage.STORAGE_KEY.notifications, value);
  };

  if (isLoading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Settings</Text>

      <AppCard
        title="Notifications"
        subtitle="Enable app notifications"
        right={<Switch value={notifications} onValueChange={handleToggle} />}
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
