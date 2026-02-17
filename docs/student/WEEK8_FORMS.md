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
    └── Save button (disabled until all fields filled)
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

**Notice:** Settings now mirrors the Courses pattern exactly. The Tab layout doesn't need any changes — Expo Router automatically resolves `name="settings"` to the `settings/` folder, just like it does for `courses`.

---

## New Concepts <a name="new-concepts"></a>

### 1. Controlled Inputs

In a normal HTML input, the text field manages its own value — you type, it shows what you typed, and your code has to go ask the input "what do you have right now?" whenever it needs the value.

A **controlled input** flips this. React state is the boss. The input field is not allowed to display anything on its own — it can only show what React tells it to show.

Here's how the cycle works:

```
    ┌──────────────────────────────────────────────────────┐
    │                                                      │
    │   1. User types "J"                                  │
    │          │                                           │
    │          ▼                                           │
    │   2. onChangeText fires → calls setFirstName("J")    │
    │          │                                           │
    │          ▼                                           │
    │   3. React state updates: firstName = "J"            │
    │          │                                           │
    │          ▼                                           │
    │   4. Component re-renders                            │
    │          │                                           │
    │          ▼                                           │
    │   5. TextInput reads value={firstName} → displays "J"│
    │                                                      │
    │   ...cycle repeats for every keystroke               │
    └──────────────────────────────────────────────────────┘
```

The input never shows what the user typed directly. It shows what **state** says. They happen to be the same thing here, but that's because we choose to set state to whatever the user typed. We could just as easily ignore certain characters, transform the text to uppercase, or limit the length — because React is in charge, not the input.

**The code — three pieces that make the cycle work:**

```tsx
const [firstName, setFirstName] = useState("");  // The source of truth

<TextInput
  value={firstName}              // "Only display what state says"
  onChangeText={setFirstName}    // "When the user types, update state"
/>
```

| Piece | Role | What happens without it |
|-------|------|------------------------|
| `useState` | Stores the current value | No memory — the value is lost between renders |
| `value={firstName}` | Tells the input what to display | Input manages itself — React can't control it |
| `onChangeText={setFirstName}` | Updates state when user types | The input appears frozen — typing does nothing |

**Why does this matter for forms?** Because at any moment, you can read `firstName` and know exactly what the user has typed. When they press Submit, you already have every field's value in state — ready to validate, send to an API, or display in an alert. No need to "reach into" the input to ask what it contains.

### 2. Form Validation

Validation = checking if the data is **correct** before using it.

```
    USER FILLS FORM          PRESSES SUBMIT          VALIDATION RUNS
    ───────────────          ──────────────          ────────────────
    First Name: ""           ───→  Click  ───→      ❌ "First name must be at least 2 characters"
    Last Name: ""                                    ❌ "Last name must be at least 2 characters"
    Email: "not-email"                               ❌ "Please enter a valid email"
    ID: "A001"                                       ❌ "Student ID must be exactly 9 characters"
    Phone: "403"                                     ❌ "Phone number must be at least 10 digits"

    First Name: "Jane"       ───→  Click  ───→      ✅ All valid → show success alert
    Last Name: "Smith"
    Email: "jane@edu.ca"
    ID: "A00123456"
    Phone: "(403) 555-0123"
```

**Our approach: validate on submit**, not on every keystroke. This is simpler for beginners and less annoying for users (they don't see errors while still typing).

### 3. Conditional Styling

You can combine styles based on conditions:

```tsx
style={[styles.input, errors.firstName && styles.inputError]}
//     ^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//     Always applied    Only applied when there's an error
```

This is like CSS classes, but using an array. React Native merges them — later styles override earlier ones. So `inputError` changes just the border color while keeping everything else from `input`.

### 4. Disabled Button Pattern

```tsx
const isFormFilled =
  firstName.length > 0 && lastName.length > 0 && email.length > 0 &&
  studentId.length > 0 && phone.length > 0;

<Pressable
  disabled={!isFormFilled}                                    // Can't press
  style={[styles.button, !isFormFilled && styles.buttonDisabled]}  // Looks faded
>
```

The button is both **functionally disabled** (`disabled` prop) and **visually disabled** (reduced opacity). Users get two signals: it looks faded AND nothing happens when they tap it.

---

## Step-by-Step Implementation <a name="step-by-step"></a>

### Step 1: Add Theme Values

**File:** `styles/theme.ts`

We need two new values — a red color for errors and a border radius for inputs.

```ts
export const theme = {
  colors: {
    bg: "#f8fafc",
    card: "#ffffff",
    text: "#111827",
    muted: "#6b7280",
    primary: "#2563eb",
    border: "#e5e7eb",
    error: "#dc2626",      // ← NEW: red for error messages and borders
  },
  spacing: {
    screen: 20,
    card: 16,
    gap: 12,
  },
  radius: {
    card: 14,
    input: 10,             // ← NEW: slightly less rounded than cards
  },
};
```

**Why add these to the theme?** Consistency. If you later want to change the error color across every form in the app, you change it in one place.

---

### Step 2: Create the Settings Stack Layout

**File:** `app/(tab)/settings/_layout.tsx`

This is identical in structure to `courses/_layout.tsx`. If you understood that file, you already understand this one.

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

**What this does:**
- Declares two screens: `index` (the settings list) and `profile` (the edit form)
- Stack navigation means tapping Account will **push** `profile` on top of `index`
- A back button appears automatically (just like in Courses)

---

### Step 3: Move Settings Content to `index.tsx`

**File:** `app/(tab)/settings/index.tsx`

This is the old `settings.tsx` content with two changes:
1. Import paths updated (we're one folder deeper now)
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

**Key changes from the original `settings.tsx`:**

| What | Before | After |
|------|--------|-------|
| Import paths | `../../components/AppCard` | `../../../components/AppCard` |
| Account icon | `person-circle-outline` | `chevron-forward` (signals "tappable") |
| Account card | Static | Wrapped in `Pressable` with navigation |

**Why `chevron-forward`?** It's the same icon used in the Courses list. Students will recognize the visual pattern — "chevron means tappable, and it pushes to a detail screen."

---

### Step 4: Build the Edit Profile Form

**File:** `app/(tab)/settings/profile.tsx`

This is the main new code for Week 8. Let's break it down section by section.

#### 4a. State Setup

```tsx
type FormErrors = {
  firstName?: string;
  lastName?: string;
  email?: string;
  studentId?: string;
  phone?: string;
};

const [firstName, setFirstName] = useState("");
const [lastName, setLastName] = useState("");
const [email, setEmail] = useState("");
const [studentId, setStudentId] = useState("");
const [phone, setPhone] = useState("");

const [errors, setErrors] = useState<FormErrors>({});
```

- Five state variables for five form fields (all start empty)
- A named `FormErrors` type defines which fields can have error messages — this is cleaner than writing the type inline, especially as the form grows
- One `errors` object that can hold an error message for each field
- The `?` in the type means each field is optional — no error = field not present in the object

#### 4b. Checking If the Form Is Filled

```tsx
const isFormFilled =
  firstName.length > 0 && lastName.length > 0 && email.length > 0 &&
  studentId.length > 0 && phone.length > 0;
```

This is **not** validation — it just checks that the user has typed _something_ in every field. Used to enable/disable the submit button. With five fields, we chain all five checks with `&&`. This value updates automatically every time any state changes (React re-evaluates it on every render).

#### 4c. Validation Function

```tsx
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

  if (phone.replace(/\D/g, "").length < 10) {
    newErrors.phone = "Phone number must be at least 10 digits.";
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
}
```

**How it works:**
1. Create a fresh empty errors object (now typed as `FormErrors` instead of `typeof errors`)
2. Check each field — if invalid, add an error message
3. Set the errors state (this triggers a re-render, showing error messages)
4. Return `true` if no errors were added, `false` otherwise

**Why `trim()`?** Removes leading/trailing spaces. `"  "` looks like input but is really empty.

**The phone validation trick:** `phone.replace(/\D/g, "")` strips out everything that isn't a digit — parentheses, dashes, spaces all disappear. Then we check if at least 10 digits remain. This means `"(403) 555-0123"` counts as 10 digits even though the string is longer than 10 characters.

**The email regex explained:**
```
/^[^\s@]+@[^\s@]+\.[^\s@]+$/
  ^^^^^^^  ^^^^^^^  ^^^^^^^
  something  @  something  .  something
  (no spaces    (no spaces    (no spaces
   or @)         or @)         or @)
```
This is a simple check, not a production-grade email validator — but it catches obvious mistakes like `"notanemail"` or `"missing@domain"`.

#### 4d. Submit Handler

```tsx
function handleSubmit() {
  if (!validate()) return;    // Stop if validation fails
  Alert.alert(
    "Profile Saved",
    `Name: ${firstName} ${lastName}\nEmail: ${email}\nID: ${studentId}\nPhone: ${phone}`
  );
}
```

If `validate()` returns `false`, we stop. The errors are already displayed (validation set them). If it returns `true`, we show a success alert. Notice the name is now built from two pieces — `${firstName} ${lastName}` — with a space between them.

#### 4e. The Input Fields (JSX)

```tsx
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
```

**Breaking it down:**
- `style={[styles.input, errors.firstName && styles.inputError]}` — red border when there's an error
- `value={firstName}` — controlled input (always shows current state)
- `onChangeText={setFirstName}` — updates state on every keystroke
- `autoCapitalize="words"` — capitalizes first letter of each word (good for names)
- `{errors.firstName && <Text>...</Text>}` — conditional rendering: only shows error if one exists

**Last Name uses the exact same pattern** — just swap `firstName`/`setFirstName`/`errors.firstName` for `lastName`/`setLastName`/`errors.lastName`, and change the placeholder to `"e.g. Smith"`. The validation logic is identical (minimum 2 characters).

**The same pattern also repeats for Email and Student ID**, with field-specific props:
- Email: `keyboardType="email-address"`, `autoCapitalize="none"`
- Student ID: `autoCapitalize="characters"`, `maxLength={9}`

**Phone Number** adds one new prop:

```tsx
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
```

The key difference here is `keyboardType="phone-pad"` — this tells the device to show a number pad optimized for phone entry (digits, plus, and common phone symbols) instead of the standard text keyboard. The user can type the number in any format they like (with dashes, parentheses, spaces) because our validation strips non-digits before counting.

#### 4f. The Submit Button

```tsx
<Pressable
  style={[styles.button, !isFormFilled && styles.buttonDisabled]}
  onPress={handleSubmit}
  disabled={!isFormFilled}
>
  <Text style={styles.buttonText}>Save Profile</Text>
</Pressable>
```

Two layers of feedback:
1. **Visual:** Button is faded (opacity 0.5) when not all fields are filled
2. **Functional:** `disabled` prop prevents `onPress` from firing

---

### Step 5: Delete the Old File

Delete `app/(tab)/settings.tsx`. The content now lives in `app/(tab)/settings/index.tsx`.

**No changes needed to `app/(tab)/_layout.tsx`** — Expo Router resolves `name="settings"` to the `settings/` folder automatically, the same way it resolves `name="courses"` to the `courses/` folder.

---

## Common Mistakes <a name="common-mistakes"></a>

### 1. Forgetting to delete `settings.tsx`

If both `settings.tsx` and `settings/index.tsx` exist, Expo Router will be confused. You'll see errors about duplicate routes. **Always delete the single file when converting to a folder.**

### 2. Using `onChangeText={(text) => setFirstName(text)}` instead of `onChangeText={setFirstName}`

Both work, but the second is cleaner. `onChangeText` already passes the text as the first argument, so `setFirstName` receives it directly. No need for the wrapper arrow function.

### 3. Validating on every keystroke

```tsx
// DON'T do this (for now):
onChangeText={(text) => {
  setFirstName(text);
  validate();  // ← Annoying! Shows errors while user is still typing
}}
```

Validate on submit only. Users don't want to see "invalid email" when they've typed one character. Let them finish, then check.

### 4. Forgetting `trim()` in validation

```tsx
// BAD: "   " (spaces) would pass this check
if (firstName.length < 2) { ... }

// GOOD: trim removes spaces first
if (firstName.trim().length < 2) { ... }
```

### 5. Not updating import paths after moving the file

When `settings.tsx` moves from `app/(tab)/` to `app/(tab)/settings/index.tsx`, it's one folder deeper. All relative imports need an extra `../`:

```
BEFORE: ../../components/AppCard
AFTER:  ../../../components/AppCard
```

### 6. Confusing "filled" with "valid"

```
isFormFilled = all fields have SOME text       → enables the button
validate()   = all fields have CORRECT text    → allows submission
```

A user can type "x" in every field — the button enables, but validation will catch the errors on submit.

---

## Student Challenge <a name="student-challenge"></a>

### Add a "Program" Picker

Add a sixth field to the Edit Profile form where the user can select their program of study. This is not a text input — it is a selection from a predefined list.

**Requirements:**
- Define a `PROGRAMS` array constant outside the component with at least three options (e.g., `"Software Development"`, `"Data Analytics"`, `"Network Systems"`)
- Add state to track which program is selected (e.g., the selected index, or `null` if nothing is selected)
- Display each program as a `Pressable` item — tapping one selects it
- Apply conditional styling so the selected program is visually distinct (e.g., highlighted background, bold text, or a border using `theme.colors.primary`)
- Validate that a program has been selected before allowing submission — add a `program` key to `FormErrors`
- Display the selected program name in the success alert alongside the other fields

**Hints:**
1. Define the array at the top of the file: `const PROGRAMS = ["Software Development", "Data Analytics", "Network Systems"];`
2. Use `useState<number | null>(null)` to track the selected index — `null` means nothing is selected yet
3. Render the list with `PROGRAMS.map((program, index) => ...)` inside a `View`
4. In each `Pressable`, compare `index === selectedProgram` to decide whether to apply the selected style
5. In validation, check `if (selectedProgram === null)` and set an error like `"Please select a program."`
6. In the success alert, use `PROGRAMS[selectedProgram]` to get the name
7. Include `selectedProgram !== null` in your `isFormFilled` check

**Bonus:** Add an "Other" option at the end. When "Other" is selected, show a `TextInput` where the student can type a custom program name. Validate that the custom input is not empty when "Other" is selected.

---

*This guide builds on the routing concepts from Week 7. The nested Stack pattern (settings/ folder) is identical to what you built for Courses — review `ROUTING_GUIDE.md` if you need a refresher.*
