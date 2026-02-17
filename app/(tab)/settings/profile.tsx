// Week 9: Local Storage — MODIFIED (added persistence + view/edit mode)
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { theme } from "../../../styles/theme";
import * as storage from "../../../lib/storage";
import { STORAGE_KEYS } from "../../../lib/storage";

type ProfileData = {
  firstName: string;
  lastName: string;
  email: string;
  studentId: string;
  phone: string;
};

type FormErrors = {
  firstName?: string;
  lastName?: string;
  email?: string;
  studentId?: string;
  phone?: string;
};

export default function Profile() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [studentId, setStudentId] = useState("");
  const [phone, setPhone] = useState("");

  const [errors, setErrors] = useState<FormErrors>({});
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [hasSavedData, setHasSavedData] = useState(false);

  // Load saved profile data on mount
  useEffect(() => {
    async function loadProfile() {
      const saved = await storage.get<ProfileData>(STORAGE_KEYS.PROFILE);
      if (saved !== null) {
        setFirstName(saved.firstName);
        setLastName(saved.lastName);
        setEmail(saved.email);
        setStudentId(saved.studentId);
        setPhone(saved.phone);
        setHasSavedData(true);
      } else {
        setIsEditing(true);
      }
      setIsLoading(false);
    }
    loadProfile();
  }, []);

  const isFormFilled =
    firstName.length > 0 &&
    lastName.length > 0 &&
    email.length > 0 &&
    studentId.length > 0 &&
    phone.length > 0;

  function validate() {
    const newErrors: FormErrors = {};

    // First Name: required, min 2 characters
    if (firstName.trim().length < 2) {
      newErrors.firstName = "First name must be at least 2 characters.";
    }

    // Last Name: required, min 2 characters
    if (lastName.trim().length < 2) {
      newErrors.lastName = "Last name must be at least 2 characters.";
    }

    // Email: required, must match email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      newErrors.email = "Please enter a valid email address.";
    }

    // Student ID: required, exactly 9 characters (e.g., "A00123456")
    if (studentId.trim().length !== 9) {
      newErrors.studentId = "Student ID must be exactly 9 characters.";
    }

    // Phone: required, at least 10 digits
    const digitsOnly = phone.replace(/\D/g, "");
    if (digitsOnly.length < 10) {
      newErrors.phone = "Phone number must have at least 10 digits.";
    }

    setErrors(newErrors);

    // Return true if no errors
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit() {
    if (!validate()) return;

    // Save profile data to storage
    const profileData: ProfileData = {
      firstName,
      lastName,
      email,
      studentId,
      phone,
    };
    await storage.set(STORAGE_KEYS.PROFILE, profileData);

    setErrors({});
    setHasSavedData(true);
    setIsEditing(false);
  }

  async function handleCancel() {
    // Reload saved data to discard any edits
    const saved = await storage.get<ProfileData>(STORAGE_KEYS.PROFILE);
    if (saved !== null) {
      setFirstName(saved.firstName);
      setLastName(saved.lastName);
      setEmail(saved.email);
      setStudentId(saved.studentId);
      setPhone(saved.phone);
    }
    setErrors({});
    setIsEditing(false);
  }

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  // VIEW MODE — show saved profile data
  if (!isEditing) {
    return (
      <ScrollView style={styles.container} contentContainerStyle={styles.content}>
        <Text style={styles.h1}>My Profile</Text>

        <View style={styles.profileCard}>
          <View style={styles.profileRow}>
            <Text style={styles.profileLabel}>First Name</Text>
            <Text style={styles.profileValue}>{firstName}</Text>
          </View>

          <View style={styles.divider} />

          <View style={styles.profileRow}>
            <Text style={styles.profileLabel}>Last Name</Text>
            <Text style={styles.profileValue}>{lastName}</Text>
          </View>

          <View style={styles.divider} />

          <View style={styles.profileRow}>
            <Text style={styles.profileLabel}>Email</Text>
            <Text style={styles.profileValue}>{email}</Text>
          </View>

          <View style={styles.divider} />

          <View style={styles.profileRow}>
            <Text style={styles.profileLabel}>Student ID</Text>
            <Text style={styles.profileValue}>{studentId}</Text>
          </View>

          <View style={styles.divider} />

          <View style={styles.profileRow}>
            <Text style={styles.profileLabel}>Phone</Text>
            <Text style={styles.profileValue}>{phone}</Text>
          </View>
        </View>

        <Pressable style={styles.button} onPress={() => setIsEditing(true)}>
          <Text style={styles.buttonText}>Edit Profile</Text>
        </Pressable>
      </ScrollView>
    );
  }

  // EDIT MODE — form with validation
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.h1}>Edit Profile</Text>

      {/* First Name */}
      <Text style={styles.label}>First Name</Text>
      <TextInput
        style={[styles.input, errors.firstName && styles.inputError]}
        placeholder="e.g. Jane"
        placeholderTextColor={theme.colors.muted}
        value={firstName}
        onChangeText={setFirstName}
        autoCapitalize="words"
      />
      {errors.firstName && <Text style={styles.error}>{errors.firstName}</Text>}

      {/* Last Name */}
      <Text style={styles.label}>Last Name</Text>
      <TextInput
        style={[styles.input, errors.lastName && styles.inputError]}
        placeholder="e.g. Smith"
        placeholderTextColor={theme.colors.muted}
        value={lastName}
        onChangeText={setLastName}
        autoCapitalize="words"
      />
      {errors.lastName && <Text style={styles.error}>{errors.lastName}</Text>}

      {/* Email */}
      <Text style={styles.label}>Email</Text>
      <TextInput
        style={[styles.input, errors.email && styles.inputError]}
        placeholder="e.g. jane.smith@edu.ca"
        placeholderTextColor={theme.colors.muted}
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      {errors.email && <Text style={styles.error}>{errors.email}</Text>}

      {/* Student ID */}
      <Text style={styles.label}>Student ID</Text>
      <TextInput
        style={[styles.input, errors.studentId && styles.inputError]}
        placeholder="e.g. A00123456"
        placeholderTextColor={theme.colors.muted}
        value={studentId}
        onChangeText={setStudentId}
        autoCapitalize="characters"
        maxLength={9}
      />
      {errors.studentId && (
        <Text style={styles.error}>{errors.studentId}</Text>
      )}

      {/* Phone Number */}
      <Text style={styles.label}>Phone Number</Text>
      <TextInput
        style={[styles.input, errors.phone && styles.inputError]}
        placeholder="e.g. (403) 555-0123"
        placeholderTextColor={theme.colors.muted}
        value={phone}
        onChangeText={setPhone}
        keyboardType="phone-pad"
      />
      {errors.phone && <Text style={styles.error}>{errors.phone}</Text>}

      {/* Buttons */}
      {hasSavedData ? (
        <View style={styles.buttonRow}>
          <Pressable style={styles.cancelButton} onPress={handleCancel}>
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </Pressable>
          <Pressable
            style={[styles.saveButton, !isFormFilled && styles.buttonDisabled]}
            onPress={handleSubmit}
            disabled={!isFormFilled}
          >
            <Text style={styles.buttonText}>Save Profile</Text>
          </Pressable>
        </View>
      ) : (
        <Pressable
          style={[styles.button, !isFormFilled && styles.buttonDisabled]}
          onPress={handleSubmit}
          disabled={!isFormFilled}
        >
          <Text style={styles.buttonText}>Save Profile</Text>
        </Pressable>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.bg,
  },
  content: {
    padding: theme.spacing.screen,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: theme.colors.bg,
  },
  h1: {
    fontSize: 22,
    fontWeight: "800",
    marginBottom: 20,
    color: theme.colors.text,
  },

  // View mode styles
  profileCard: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.radius.card,
    borderWidth: 1,
    borderColor: theme.colors.border,
    overflow: "hidden",
  },
  profileRow: {
    padding: 16,
  },
  profileLabel: {
    fontSize: 13,
    color: theme.colors.muted,
    marginBottom: 4,
  },
  profileValue: {
    fontSize: 16,
    color: theme.colors.text,
    fontWeight: "500",
  },
  divider: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: theme.colors.border,
  },

  // Edit mode styles
  label: {
    fontSize: 14,
    fontWeight: "600",
    color: theme.colors.text,
    marginBottom: 6,
    marginTop: 16,
  },
  input: {
    backgroundColor: theme.colors.card,
    borderWidth: 1,
    borderColor: theme.colors.border,
    borderRadius: theme.radius.input,
    padding: 14,
    fontSize: 16,
    color: theme.colors.text,
  },
  inputError: {
    borderColor: theme.colors.error,
  },
  error: {
    color: theme.colors.error,
    fontSize: 13,
    marginTop: 4,
  },

  // Button styles
  button: {
    backgroundColor: theme.colors.primary,
    borderRadius: theme.radius.input,
    padding: 16,
    alignItems: "center",
    marginTop: 28,
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: "#ffffff",
    fontSize: 16,
    fontWeight: "700",
  },
  buttonRow: {
    flexDirection: "row",
    gap: 12,
    marginTop: 28,
  },
  cancelButton: {
    flex: 1,
    borderRadius: theme.radius.input,
    padding: 16,
    alignItems: "center",
    borderWidth: 1,
    borderColor: theme.colors.border,
    backgroundColor: theme.colors.card,
  },
  cancelButtonText: {
    color: theme.colors.text,
    fontSize: 16,
    fontWeight: "700",
  },
  saveButton: {
    flex: 1,
    backgroundColor: theme.colors.primary,
    borderRadius: theme.radius.input,
    padding: 16,
    alignItems: "center",
  },
});
