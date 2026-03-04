import AsyncStorage from "@react-native-async-storage/async-storage";
export const STORAGE_KEY = {
  PROFILE: "profile",
  notifications: "notifications",
} as const;

//Get a value  from storage (auto-parsed from JSON)

export const get = async <T>(key: string): Promise<T | null> => {
  const value = await AsyncStorage.getItem(key);
  if (value === null) return null;
  return JSON.parse(value) as T;
};

//set a value in storage (auto-stringified to JSON)

export const set = async (key: string, value: unknown): Promise<void> => {
  await AsyncStorage.setItem(key, JSON.stringify(value));
};

//remove a value from storage
export const remove = async (key: string): Promise<void> => {
  await AsyncStorage.removeItem(key);
};
