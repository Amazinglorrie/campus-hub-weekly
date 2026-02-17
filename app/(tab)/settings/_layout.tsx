// Week 8: Forms + Validation — NEW file (nested Stack for settings)
import { Stack } from "expo-router";

export default function SettingsLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Settings" }} />
      <Stack.Screen name="profile" options={{ title: "Profile" }} />
    </Stack>
  );
}
