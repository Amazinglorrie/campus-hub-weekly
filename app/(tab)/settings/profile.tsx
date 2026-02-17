// Week 8: Forms + Validation — NEW file (profile form with validation, no persistence)
import React, { useState } from "react";
import {
  Alert,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { router } from "expo-router";
import { theme } from "../../../styles/theme";

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

  const isFormFilled =
    firstName.length > 0 &&
    lastName.length > 0 &&
    email.length > 0 &&
    studentId.length > 0 &&
    phone.length > 0;

  function validate() {
    const newErrors: FormErrors = {};

    if (firstName.trim().length < 2) {
      newErrors.firstName = "First name must be at least 2 characters.";
    }

    if (lastName.trim().length < 2) {
      newErrors.lastName = "Last name must be at least 2 characters.";
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      newErrors.email = "Please enter a valid email address.";
    }

    if (studentId.trim().length !== 9) {
      newErrors.studentId = "Student ID must be exactly 9 characters.";
    }

    const digitsOnly = phone.replace(/\D/g, "");
    if (digitsOnly.length < 10) {
      newErrors.phone = "Phone number must have at least 10 digits.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  function handleSubmit() {
    if (!validate()) return;

    Alert.alert("Profile Saved", "Your profile has been updated.", [
      { text: "OK", onPress: () => router.back() },
    ]);
  }

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

      {/* Submit Button */}
      <Pressable
        style={[styles.button, !isFormFilled && styles.buttonDisabled]}
        onPress={handleSubmit}
        disabled={!isFormFilled}
      >
        <Text style={styles.buttonText}>Save Profile</Text>
      </Pressable>
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
  h1: {
    fontSize: 22,
    fontWeight: "800",
    marginBottom: 20,
    color: theme.colors.text,
  },
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
});
