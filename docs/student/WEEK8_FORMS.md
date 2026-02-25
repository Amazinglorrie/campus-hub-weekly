# Week 8: Forms + Validation

## A Step-by-Step Guide for Building Your First Form in React Native

---

## Table of Contents

1. [Before vs After](#before-vs-after)
2. [Architecture Impact](#architecture-impact)
3. [New Concepts](#new-concepts)
4. [Step-by-Step Implementation](#step-by-step)
5. [Common Mistakes](#common-mistakes)
6. [Student Challenge](#student-challenge)

---

## Before vs After <a name="before-vs-after"></a>

### Before (Week 7)

```
Settings tab = a single file (settings.tsx)
├── Notifications toggle (works)
└── Account card (just sits there — not tappable)
```

The Account card looks clickable but does nothing. There's no form anywhere in the app.

### After (Week 8)

```
Settings tab = a folder with its own Stack navigator (settings/)
├── Settings list (index.tsx)
│   ├── Notifications toggle (works)
│   └── Account card (NOW tappable → pushes to profile form)
│
└── Edit Profile form (profile.tsx)  ← NEW
    ├── First Name input (validated)
    ├── Last Name input (validated)
    ├── Email input (validated)
    ├── Student ID input (validated)
    ├── Phone Number input (validated)
    └── Save button (validates on press)
```

Tapping the Account card now pushes to a real Edit Profile screen — with a back button, just like tapping a course pushes to course details.

---

## Architecture Impact <a name="architecture-impact"></a>

### The Pattern You Already Know

In Week 7, you built the Courses tab as a **folder with a nested Stack**:

```
courses/
├── _layout.tsx    ← Stack navigator
├── index.tsx      ← Courses list
└── [id].tsx       ← Course details (pushed on tap)
```

### The Same Pattern, Applied Again

This week, Settings gets the same treatment:

```
settings/
├── _layout.tsx    ← Stack navigator (NEW)
├── index.tsx      ← Settings list (MOVED from settings.tsx)
└── profile.tsx    ← Edit Profile form (NEW)
```

**Why does this matter?** You now have **two** examples of the nested Stack pattern. This isn't a coincidence — most real-world apps use this pattern everywhere. Any tab that needs to "drill deeper" into content gets its own folder with a Stack layout.

### File Changes Summary

```
 DELETED:  app/(tab)/settings.tsx
 CREATED:  app/(tab)/settings/_layout.tsx    ← Stack navigator
 CREATED:  app/(tab)/settings/index.tsx      ← Settings list (moved content)
 CREATED:  app/(tab)/settings/profile.tsx    ← Edit Profile form
MODIFIED:  styles/theme.ts                   ← Added error color, input radius
```

### Updated Architecture Diagram

```
    app/_layout.tsx .................. Stack (Root)
        |
        └── app/(tab)/_layout.tsx ... Tabs
                |
                ├── home.tsx ........ Tab Screen (simple)
                |
                ├── courses/_layout.tsx .. Stack (Nested)   ← Week 7
                |       |
                |       ├── index.tsx ... Courses list
                |       └── [id].tsx .... Course details
                |
                └── settings/_layout.tsx . Stack (Nested)   ← Week 8 (NEW!)
                        |
                        ├── index.tsx ... Settings list
                        └── profile.tsx . Edit Profile form
```

**Notice:** Settings now mirrors the Courses pattern exactly. The Tab layout doesn't need any changes — Expo Router automatically resolves `name="settings"` to the `settings/` folder.

---

## New Concepts <a name="new-concepts"></a>

### The Libraries

Before writing any code, it helps to understand what each library actually is and why it exists.

---

#### React Hook Form

**React Hook Form (RHF)** is a library that manages all the moving parts of a form for you — tracking what the user typed in each field, knowing which fields have been touched, deciding when to show error messages, and handling submission. Without it, you would need a separate `useState` for every field plus extra logic to coordinate them all.

RHF is built around a single hook — `useForm` — which you call once at the top of your component. It gives back everything you need: `control` to register fields, `handleSubmit` to handle the submit button, and `formState` to read errors and other status info.

It is one of the most downloaded React libraries in the world and is used extensively in production apps.

> **Docs & more info:** [react-hook-form.com](https://react-hook-form.com/) — the official site has interactive examples for every concept. Start with the [Get Started](https://react-hook-form.com/get-started) guide and the [`useForm` API reference](https://react-hook-form.com/docs/useform).

---

#### Zod

**Zod** is a schema validation library built specifically for TypeScript. A "schema" is a description of what valid data looks like — you define the rules once, and Zod checks any value against them.

The key advantage over writing validation logic by hand: your rules are in one place, in a consistent format, and Zod automatically generates a TypeScript type from them. You never write the same rule twice — once in a type definition and again in an `if` statement.

Zod is the current industry standard for TypeScript data validation. It's used not just in forms but also for validating API responses, environment variables, and config files.

> **Docs & more info:** [zod.dev](https://zod.dev/) — the official docs are well written and example-heavy. See [Basic Usage](https://zod.dev/?id=basic-usage) and the full list of [string validators](https://zod.dev/?id=strings) for what's available beyond what we use this week.

---

#### @hookform/resolvers

This is the adapter package that makes RHF and Zod work together. By itself, RHF doesn't know about Zod, and Zod doesn't know about RHF. `@hookform/resolvers/zod` translates between them — you pass it to `useForm` as the `resolver` option, and from that point on, RHF runs your Zod schema automatically whenever it needs to validate.

> **More info:** [github.com/react-hook-form/resolvers](https://github.com/react-hook-form/resolvers) — the package also supports other validation libraries (Yup, Joi, Valibot) if you encounter them in future projects.

---

### The Library Stack: Three Tools, One Job

Building forms involves two separate concerns:

```
┌──────────────────────────────────────────────────────────────┐
│  1. Capturing what the user typed                            │
│     — tracking field values, knowing which fields are dirty  │
│     — deciding when to show errors                           │
│     → handled by: react-hook-form                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  2. Defining what "valid" means                              │
│     — firstName must be at least 2 chars                     │
│     — email must look like an email                          │
│     — phone must have at least 10 digits                     │
│     → handled by: zod                                        │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  3. Connecting the two                                       │
│     — one import that makes RHF and Zod work together        │
│     → handled by: @hookform/resolvers/zod                    │
└──────────────────────────────────────────────────────────────┘
```

Before this week, you would have written a manual `validate()` function with all those rules scattered across your component. With this stack, the rules live in the schema — in one place, in one format — and the libraries handle the rest.

---

### 1. Zod Schemas

A **schema** is a description of what valid data looks like. You write it once, and Zod uses it to check any value against your rules.

```ts
import { z } from "zod";

const profileSchema = z.object({
  firstName: z.string().trim().min(2, "First name must be at least 2 characters."),
  lastName:  z.string().trim().min(2, "Last name must be at least 2 characters."),
  email:     z.string().trim().email("Please enter a valid email address."),
  studentId: z.string().trim().length(9, "Student ID must be exactly 9 characters."),
  phone:     z.string().refine(
    (val) => val.replace(/\D/g, "").length >= 10,
    "Phone number must have at least 10 digits."
  ),
});
```

**Reading each line:**

| Rule | What it checks | Example that fails |
|------|---------------|-------------------|
| `.trim().min(2, "...")` | At least 2 non-space characters | `"  "` (just spaces) |
| `.trim().email("...")` | Looks like a real email address | `"notanemail"` |
| `.trim().length(9, "...")` | Exactly 9 characters | `"A001234"` (only 7) |
| `.refine(fn, "...")` | Custom rule — function returns true/false | `"403"` (only 3 digits) |

**Phone validation explained — `.refine()`:**

```ts
z.string().refine(
  (val) => val.replace(/\D/g, "").length >= 10,
  "Phone number must have at least 10 digits."
)
```

`val.replace(/\D/g, "")` strips out everything that isn't a digit — parentheses, dashes, spaces, all of it. Then we check if at least 10 digits remain. This means `"(403) 555-0123"` passes because the digits alone are `4035550123` (10 digits), even though the full string is longer.

---

### 2. Type Inference from Schema

Once you have a schema, Zod can generate a TypeScript type from it automatically:

```ts
type ProfileForm = z.infer<typeof profileSchema>;
// Result: { firstName: string; lastName: string; email: string; studentId: string; phone: string; }
```

You didn't write that type by hand — Zod did. If you add a new field to the schema, the type updates automatically. This is one of the main reasons Zod is preferred over manual type definitions for form data.

---

### 3. `useForm` — React Hook Form's Core Hook

```tsx
const {
  control,
  handleSubmit,
  formState: { errors },
} = useForm<ProfileForm>({
  resolver: zodResolver(profileSchema),
  defaultValues: {
    firstName: "",
    lastName:  "",
    email:     "",
    studentId: "",
    phone:     "",
  },
  mode: "onSubmit",
});
```

**What each piece does:**

| Piece | Role |
|-------|------|
| `control` | Passed to each `Controller`. Lets RHF track every field in the form. |
| `handleSubmit` | Wraps your submit function. Runs validation first. Only calls your function if the schema passes. |
| `formState.errors` | Object of error messages, keyed by field name. Only populated after a failed submit. |
| `resolver: zodResolver(profileSchema)` | Connects Zod to RHF. This one line replaces a manual `validate()` function. |
| `defaultValues` | Starting values for every field. Required for controlled inputs. |
| `mode: "onSubmit"` | When to validate. `"onSubmit"` means wait until the user presses Save. |

---

### 4. `Controller` — Connecting React Native Inputs

React Hook Form has two ways to register a field: `register` and `Controller`.

- `register` works with standard HTML `<input>` elements
- `Controller` works with any component — including React Native's `TextInput`

**Why the difference?** HTML inputs use `onChange`. React Native's `TextInput` uses `onChangeText`. `Controller` handles this translation for you.

```tsx
<Controller
  control={control}          // The control object from useForm
  name="firstName"           // Must match a key in your schema
  render={({ field: { onChange, value } }) => (
    <TextInput
      value={value}          // The current field value (from RHF)
      onChangeText={onChange} // Update RHF's state when user types
      placeholder="e.g. Jane"
    />
  )}
/>
```

**The cycle:**

```
    User types "J"
         │
         ▼
    onChangeText fires → calls onChange("J")
         │
         ▼
    React Hook Form updates its internal state: firstName = "J"
         │
         ▼
    Controller re-renders → passes value="J" to TextInput
         │
         ▼
    TextInput displays "J"
```

The key difference from plain `useState`: RHF manages all field state internally. You don't write `const [firstName, setFirstName] = useState("")` for every field. You just use `control` and `Controller`.

---

### 5. Error Display

After a failed submit, `formState.errors` contains error information for each failing field:

```tsx
// If firstName fails, errors.firstName looks like:
// { message: "First name must be at least 2 characters.", type: "too_small" }

// If firstName passes, errors.firstName is undefined.
```

To show errors in the UI:

```tsx
{/* Red border when there's an error */}
<Controller
  control={control}
  name="firstName"
  render={({ field: { onChange, value } }) => (
    <TextInput
      style={[styles.input, errors.firstName && styles.inputError]}
      value={value}
      onChangeText={onChange}
    />
  )}
/>

{/* Error message — only renders if errors.firstName exists */}
{errors.firstName && (
  <Text style={styles.error}>{errors.firstName.message}</Text>
)}
```

**Two patterns used here:**
- `style={[styles.input, errors.firstName && styles.inputError]}` — array of styles. `inputError` (red border) only applies when there's an error.
- `{errors.firstName && <Text>...}` — short-circuit rendering. If `errors.firstName` is `undefined`, nothing renders.

The error message comes directly from the Zod schema — you wrote it once there, and it surfaces here automatically.

---

### 6. `handleSubmit` and `onSubmit`

```tsx
function onSubmit(data: ProfileForm) {
  // Only called if validation passes
  // data is fully typed and matches your schema
  Alert.alert("Profile Saved", "Your profile has been updated.");
}

<Pressable onPress={handleSubmit(onSubmit)}>
  <Text>Save Profile</Text>
</Pressable>
```

**Do not pass `onSubmit` directly to `onPress`.** Always wrap it with `handleSubmit`:

```tsx
// WRONG — skips validation entirely
onPress={onSubmit}

// CORRECT — validates first, then calls onSubmit if valid
onPress={handleSubmit(onSubmit)}
```

`handleSubmit` is RHF's interceptor. It:
1. Runs the Zod schema against all current field values
2. If any rule fails → populates `errors`, triggers re-render to show them, does **not** call `onSubmit`
3. If all rules pass → calls `onSubmit(data)` where `data` is the typed, validated form values

---

## Step-by-Step Implementation <a name="step-by-step"></a>

### Step 1: Add Theme Values

**File:** `styles/theme.ts`

```ts
export const theme = {
  colors: {
    bg: "#f8fafc",
    card: "#ffffff",
    text: "#111827",
    muted: "#6b7280",
    primary: "#2563eb",
    border: "#e5e7eb",
    error: "#dc2626",      // ← NEW
  },
  spacing: {
    screen: 20,
    card: 16,
    gap: 12,
  },
  radius: {
    card: 14,
    input: 10,             // ← NEW
  },
};
```

---

### Step 2: Create the Settings Stack Layout

**File:** `app/(tab)/settings/_layout.tsx`

```tsx
import { Stack } from "expo-router";

export default function SettingsLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Settings" }} />
      <Stack.Screen name="profile" options={{ title: "Edit Profile" }} />
    </Stack>
  );
}
```

Identical in structure to `courses/_layout.tsx`. If you understood that file, you understand this one.

---

### Step 3: Move Settings Content to `index.tsx`

**File:** `app/(tab)/settings/index.tsx`

Same content as the old `settings.tsx` with two changes:
1. Import paths updated (one folder deeper now — one extra `../`)
2. Account card wrapped in `Pressable` with navigation

```tsx
import React, { useState } from "react";
import { Pressable, StyleSheet, Switch, Text, View } from "react-native";
import { router } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import AppCard from "../../../components/AppCard";
import { theme } from "../../../styles/theme";

export default function Settings() {
  const [notifications, setNotifications] = useState(true);

  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Settings</Text>

      <AppCard
        title="Notifications"
        subtitle="Enable app notifications"
        right={
          <Switch value={notifications} onValueChange={setNotifications} />
        }
      />

      {/* NEW: Pressable wrapper makes the card tappable */}
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
```

**Key change from original `settings.tsx`:**

| What | Before | After |
|------|--------|-------|
| Import paths | `../../components/AppCard` | `../../../components/AppCard` |
| Account icon | `person-circle-outline` | `chevron-forward` (signals "tappable") |
| Account card | Static | Wrapped in `Pressable` with navigation |

---

### Step 4: Build the Edit Profile Form

**File:** `app/(tab)/settings/profile.tsx`

#### 4a. Schema + Type

```tsx
import { z } from "zod";

const profileSchema = z.object({
  firstName: z.string().trim().min(2, "First name must be at least 2 characters."),
  lastName:  z.string().trim().min(2, "Last name must be at least 2 characters."),
  email:     z.string().trim().email("Please enter a valid email address."),
  studentId: z.string().trim().length(9, "Student ID must be exactly 9 characters."),
  phone:     z.string().refine(
    (val) => val.replace(/\D/g, "").length >= 10,
    "Phone number must have at least 10 digits."
  ),
});

type ProfileForm = z.infer<typeof profileSchema>;
```

All five validation rules are defined here, once. No separate `FormErrors` type. No `validate()` function. The schema is the source of truth.

#### 4b. `useForm` Setup

```tsx
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const {
  control,
  handleSubmit,
  formState: { errors },
} = useForm<ProfileForm>({
  resolver: zodResolver(profileSchema),
  defaultValues: {
    firstName: "",
    lastName:  "",
    email:     "",
    studentId: "",
    phone:     "",
  },
  mode: "onSubmit",
});
```

#### 4c. Submit Handler

```tsx
function onSubmit(data: ProfileForm) {
  Alert.alert("Profile Saved", "Your profile has been updated.", [
    { text: "OK", onPress: () => router.back() },
  ]);
}
```

`data` is typed as `ProfileForm` — TypeScript knows the exact shape because Zod inferred it.

#### 4d. Each Field — The Repeating Pattern

Every field follows the exact same structure:

```tsx
<Text style={styles.label}>First Name</Text>
<Controller
  control={control}
  name="firstName"
  render={({ field: { onChange, value } }) => (
    <TextInput
      style={[styles.input, errors.firstName && styles.inputError]}
      placeholder="e.g. Jane"
      placeholderTextColor={theme.colors.muted}
      value={value}
      onChangeText={onChange}
      autoCapitalize="words"
    />
  )}
/>
{errors.firstName && (
  <Text style={styles.error}>{errors.firstName.message}</Text>
)}
```

**For each subsequent field, only these things change:**
- `name` prop on `Controller` → matches the schema key
- `placeholder` text
- TextInput-specific props (`keyboardType`, `autoCapitalize`, `maxLength`)

| Field | `name` | Key extra props |
|-------|--------|----------------|
| First Name | `"firstName"` | `autoCapitalize="words"` |
| Last Name | `"lastName"` | `autoCapitalize="words"` |
| Email | `"email"` | `keyboardType="email-address"`, `autoCapitalize="none"` |
| Student ID | `"studentId"` | `autoCapitalize="characters"`, `maxLength={9}` |
| Phone | `"phone"` | `keyboardType="phone-pad"` |

#### 4e. Submit Button

```tsx
<Pressable style={styles.button} onPress={handleSubmit(onSubmit)}>
  <Text style={styles.buttonText}>Save Profile</Text>
</Pressable>
```

No `disabled` prop needed — `handleSubmit` handles everything. If validation fails, `onSubmit` simply never runs and errors appear in the UI.

---

### Step 5: Delete the Old File

Delete `app/(tab)/settings.tsx`. The content now lives in `app/(tab)/settings/index.tsx`.

**No changes needed to `app/(tab)/_layout.tsx`** — Expo Router resolves `name="settings"` to the `settings/` folder automatically.

---

## Common Mistakes <a name="common-mistakes"></a>

### 1. Using `onChange` instead of `onChangeText`

```tsx
// WRONG — this is the HTML event handler, does nothing in React Native
<TextInput onChange={onChange} />

// CORRECT
<TextInput onChangeText={onChange} />
```

This is the most common mistake when coming from web React. The field will appear frozen — typing does nothing — if you use the wrong handler.

### 2. Calling `onSubmit` directly on `onPress`

```tsx
// WRONG — skips validation
onPress={onSubmit}

// CORRECT — validates first
onPress={handleSubmit(onSubmit)}
```

Without `handleSubmit`, the form submits regardless of whether the data is valid.

### 3. Forgetting `defaultValues`

Without `defaultValues`, React Hook Form doesn't know the initial state of each field. Always include a value for every field in your schema.

### 4. Forgetting `resolver`

```tsx
// Missing resolver — Zod schema is completely ignored
useForm<ProfileForm>({
  defaultValues: { ... }
  // No resolver here
})
```

The form will submit with any data. The Zod schema is only active when you connect it with `zodResolver`.

### 5. Forgetting to delete `settings.tsx`

If both `settings.tsx` and `settings/index.tsx` exist, Expo Router will have a duplicate route conflict. Always delete the single file when converting a tab to a folder.

### 6. Not updating import paths after moving the file

When `settings.tsx` moves from `app/(tab)/` to `app/(tab)/settings/index.tsx`, it's one folder deeper. All relative imports need an extra `../`:

```
BEFORE: ../../components/AppCard
AFTER:  ../../../components/AppCard
```

---

## Student Challenge <a name="student-challenge"></a>

### Add a "Program" Picker

Add a sixth field to the Edit Profile form where the user can select their program of study.

**Requirements:**
- Add `program` to the Zod schema: `z.string().min(1, "Please select a program.")`
- Update `type ProfileForm` is automatic — `z.infer` handles it
- Define a `PROGRAMS` constant array outside the component with at least three options
- Use `Controller` with `name="program"` — but instead of a `TextInput`, render a list of `Pressable` items that call `onChange(programName)` when tapped
- Apply conditional styling so the selected program is visually distinct
- Show the selected program in the success alert

**Hint — how to use `Controller` with a non-TextInput component:**

```tsx
<Controller
  control={control}
  name="program"
  render={({ field: { onChange, value } }) => (
    <View>
      {PROGRAMS.map((p) => (
        <Pressable
          key={p}
          onPress={() => onChange(p)}
          style={[styles.option, value === p && styles.optionSelected]}
        >
          <Text>{p}</Text>
        </Pressable>
      ))}
    </View>
  )}
/>
{errors.program && <Text style={styles.error}>{errors.program.message}</Text>}
```

`Controller` doesn't care that there's no `TextInput` inside. It just gives you `onChange` and `value`. You call `onChange` with the selected program when the user taps a `Pressable`. The schema validates that `value` is not an empty string.

**Bonus:** Use `z.enum(["Software Development", "Data Analytics", "Network Systems"])` instead of `z.string().min(1)` — this restricts the value to only those three options and gives you a stricter schema.

---

*This guide builds on the routing concepts from Week 7. The nested Stack pattern (settings/ folder) is identical to what you built for Courses — review `ROUTING_GUIDE.md` if you need a refresher.*
