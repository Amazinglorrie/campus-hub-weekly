# Week 9 — Instructor Plan: Local Storage

> **This file is gitignored. Students should never see this.**

---

## At a Glance

```
SESSION     DURATION    FOCUS
────────    ────────    ─────
Day 1       2 hours     AsyncStorage setup, storage utility, persist notifications toggle
            (separate day)
Day 2       2 hours     Persist profile data, useEffect patterns, loading states
```

Students leave Day 1 with a notifications toggle that survives app restarts.
Students leave Day 2 with a fully persistent profile form that pre-fills on revisit.

---

## Before Class (Day 1)

### What students already know (Weeks 1–8)

- TypeScript fundamentals (6 weeks of foundation), including async/await
- File-based routing, Stack and Tab navigation (Week 7)
- Nested navigation — Stack inside a Tab (the `courses/` and `settings/` patterns)
- `useState` for controlled inputs and form state (Week 8)
- Form validation patterns — validate on submit, inline errors (Week 8)
- The `AppCard` component and centralized theming

### What's already on their machines

The app has 3 tabs. Settings has a nested Stack with a notifications toggle and an Edit Profile form with 5 validated fields. Everything works — but nothing persists. Close the app, data is gone.

### What's new this week

- **`useEffect`** — first time students use it. They need to understand "run once on mount."
- **async/await in components** — students know async/await from TypeScript foundation, but using it inside `useEffect` (the nested async function pattern) is new.
- **AsyncStorage** — first third-party storage library. Simple key-value API.
- **Loading state** — simple `isLoading` boolean pattern. Preps them for Week 10 (API loading states).

### Prep checklist

- [ ] Have the current app running on your machine so you can demo live
- [ ] Verify AsyncStorage installs cleanly: `npx expo install @react-native-async-storage/async-storage`
- [ ] Have the finished `settings/index.tsx` (with persistence) ready but **don't show it yet** — build it live
- [ ] Prepare a diagram or slide showing the useEffect lifecycle (mount → load → setState → re-render)
- [ ] Have a way to demonstrate persistence (close/reopen the Expo Go app, or shake to reload)

---

## Day 1 (2 hours) — AsyncStorage + Storage Utility + Notifications Persistence

### Opening (10 min) — Demonstrate the Problem

Start by running the app.

**Say something like:**
> "Your profile form works great. Let me fill it in with valid data. Save. Looks good. Now let me go back to Settings... and tap Account again."

Show that all fields are blank. The data vanished.

> "And the notifications toggle — it's on right now. Let me turn it off. Now I'll switch to the Home tab... and back to Settings."

Show that the toggle is back to "on." The state was lost.

> "Everything you build resets when you navigate away. That's because `useState` only lives in memory — when the component unmounts, the state is gone. Today we fix that. By the end of class, the notifications toggle will remember its position even after you close the app entirely."

**This is the hook.** Students feel the pain of lost data — now they're motivated to fix it.

### Step 1 (10 min) — Install AsyncStorage

Live demo the installation:

```bash
npx expo install @react-native-async-storage/async-storage
```

**Explain briefly:**
> "AsyncStorage is like a tiny notepad on the user's phone. Your app can write things to it and read them back later — even after the app is closed and reopened. It stores everything as strings, so we'll need to convert objects to JSON."

**Don't go deep into the API yet.** They'll see it through the utility.

### Step 2 (20 min) — Build the Storage Utility

This is an important teaching moment: the utility module pattern.

**Start by showing the raw AsyncStorage API:**

```tsx
// Reading (verbose and repetitive)
const json = await AsyncStorage.getItem("profile");
const data = json ? JSON.parse(json) : null;

// Writing (verbose and repetitive)
await AsyncStorage.setItem("profile", JSON.stringify(profileData));
```

**Ask:** "What if you have 10 different screens that all need to read and write to storage? Would you want to write `JSON.parse(await AsyncStorage.getItem(...))` in every single one?"

Then build the utility together. Create `lib/storage.ts`:

```ts
import AsyncStorage from "@react-native-async-storage/async-storage";

export const STORAGE_KEYS = {
  PROFILE: "profile",
  NOTIFICATIONS: "notifications",
} as const;

export async function get<T>(key: string): Promise<T | null> {
  const value = await AsyncStorage.getItem(key);
  if (value === null) return null;
  return JSON.parse(value) as T;
}

export async function set(key: string, value: unknown): Promise<void> {
  await AsyncStorage.setItem(key, JSON.stringify(value));
}

export async function remove(key: string): Promise<void> {
  await AsyncStorage.removeItem(key);
}
```

**Key teaching points:**

1. **`STORAGE_KEYS` as constants** — "Why not just write the string `"profile"` everywhere? Because typos. If you write `"profle"` somewhere, it silently fails — no error, just no data. With a constant, TypeScript catches the typo."

2. **`<T>` generic** — "This tells TypeScript what type you expect back. When you write `storage.get<boolean>(...)`, TypeScript knows the result is `boolean | null`. It's a hint for the type system."

3. **`as const`** — "This makes the values readonly and narrows their types. It means you can't accidentally write `STORAGE_KEYS.PROFILE = 'something else'`."

4. **Why `unknown` instead of `any`** — "The `unknown` type is safer than `any`. It means 'I don't know what this is yet' without disabling type checking. JSON.stringify accepts it."

### Step 3 (25 min) — Introduce useEffect

This is the most important concept of the week. Take your time here.

**Don't show code yet.** Start with the concept:

> "Right now, every line of code in your component runs on every render. When React re-renders Settings because you toggled something, every line runs again. But loading data from storage should only happen ONCE — when the screen first appears. We need a way to say 'run this code once, when the component mounts.' That's what `useEffect` does."

**Draw or show this timeline:**

```
Component mounts (first render)
       │
       ▼
useEffect fires ──→ loads data from storage
       │
       ▼
Data arrives ──→ setState ──→ component re-renders
       │
       ▼
useEffect does NOT fire again (empty dependency array)
```

**The key rule:** "The empty array `[]` means 'no dependencies.' React interprets this as 'there's nothing this effect depends on, so it never needs to re-run.' It runs once on mount, and that's it."

**Then show the async pattern:**

> "There's one trick. `useEffect` can't be an async function directly. You can't write `useEffect(async () => {...})`. Instead, you define an async function INSIDE the effect and call it immediately."

```tsx
useEffect(() => {
  async function loadData() {
    const saved = await storage.get<boolean>(STORAGE_KEYS.NOTIFICATIONS);
    if (saved !== null) {
      setNotifications(saved);
    }
  }
  loadData();
}, []);
```

**Ask the class:** "Why do we check `if (saved !== null)` before setting state?" Let them think. Answer: "The first time someone opens the app, nothing is in storage yet. `get()` returns `null`. We want to keep the default value (`true`) instead of setting notifications to `null`."

### Step 4 (25 min) — Persist the Notifications Toggle

Now apply it to the actual code. Live code the changes to `settings/index.tsx`:

1. **Add imports:** `useEffect`, `ActivityIndicator`, storage utility
2. **Add `isLoading` state:** `const [isLoading, setIsLoading] = useState(true);`
3. **Add `useEffect`:** Load notifications on mount
4. **Create `handleToggle`:** Save to storage when toggled
5. **Add loading spinner:** Early return with `ActivityIndicator`

**Build it incrementally.** After each step, run the app and show what changed.

After step 5, do the full demo:
1. Toggle notifications off
2. Switch to Home tab and back — toggle is still off (state preserved by React)
3. **Close the Expo Go app entirely** (not just navigate away)
4. Reopen — toggle is still off! (storage preserved by AsyncStorage)

**This is the "wow" moment.** Make sure students see it clearly.

### Step 5 (15 min) — Explain Loading State

Go back and explain why `isLoading` matters:

> "Watch what happens without the loading state."

Comment out the `isLoading` logic. Toggle notifications off, close the app, reopen. The toggle briefly shows "on" then flips to "off." That flash looks like a bug.

> "The component renders immediately with the default value (true). A moment later, useEffect loads the saved value (false) and updates state. The user sees the toggle flash from on to off. The loading state prevents this — we show a spinner until the data is ready."

Uncomment the `isLoading` logic. Demo again — now there's a brief spinner, then the correct value. No flash.

### Day 1 Closing (15 min)

Run the full app. Walk through what works:
- Settings loads (brief spinner, then content)
- Notifications toggle persists across tab switches
- Notifications toggle persists across app restarts
- Account still navigates to the profile form (but data doesn't persist yet — that's Day 2)

**Set up Day 2:**
> "The notifications toggle now has memory. But the profile form is still forgetful. Next class we'll apply the exact same pattern — useEffect to load, storage.set to save — to the profile form. It's the same three steps: load on mount, save on action, show spinner while loading."

**Homework (optional):** Read the `useEffect` and `async` sections of `WEEK9_LOCAL_STORAGE.md`. Try to predict what changes are needed in `profile.tsx` before Day 2.

---

## Before Class (Day 2)

### Prep checklist

- [ ] Make sure the Day 1 code is working on your machine (notifications persist)
- [ ] Have the finished `profile.tsx` ready for reference (but build it live)
- [ ] Prepare the student challenge (Dark Mode toggle) on a slide or handout

### What students should have from Day 1

```
lib/
└── storage.ts                ← Storage utility (3 functions + STORAGE_KEYS)

app/(tab)/settings/
├── _layout.tsx               ← Stack navigator (unchanged)
├── index.tsx                 ← Settings list (NOW loads/saves notifications)
└── profile.tsx               ← Edit Profile (NOT yet persistent)
```

If any students are missing Day 1 code, give them 5 minutes at the start to catch up using the guide.

---

## Day 2 (2 hours) — Profile Persistence + View/Edit Mode

### Opening (10 min) — Recap Day 1

Quick interactive recap:

**Ask these out loud — let students answer:**
1. "What does `useEffect` with an empty array do?" (Runs code once when the component mounts)
2. "Why can't we make `useEffect` itself async?" (It would return a Promise, but React expects nothing or a cleanup function)
3. "What would happen without `isLoading`?" (The UI flashes the default value before the stored value loads)

**Then demonstrate where we left off:**

Run the app. Toggle notifications — it persists. Go to the profile form — still empty. "Today we fix the profile form. But we're also going to improve the UX."

**Motivate the view/edit pattern:**
> "Think about Instagram or LinkedIn. When you open your profile, do you see a form? No — you see your info displayed cleanly. There's an Edit button somewhere. You tap it, make changes, save, and you're back to the clean view. That's what we're building today."

### Step 6 (15 min) — Add State Variables + useEffect

Start by defining the type and new state:

```tsx
type ProfileData = {
  firstName: string;
  lastName: string;
  email: string;
  studentId: string;
  phone: string;
};

const [isLoading, setIsLoading] = useState(true);
const [isEditing, setIsEditing] = useState(false);
const [hasSavedData, setHasSavedData] = useState(false);
```

**Explain each new state:**
- `isEditing` — controls which mode the screen shows. `false` = view mode, `true` = edit mode.
- `hasSavedData` — tracks whether a profile has been saved before. Controls whether the Cancel button appears.

**Then add the useEffect:**

```tsx
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
      setIsEditing(true);  // No saved data → jump to edit mode
    }
    setIsLoading(false);
  }
  loadProfile();
}, []);
```

**Key difference from notifications:** The `useEffect` now decides the initial mode. If data exists → view mode. If no data → edit mode. Ask: "Why do we go straight to edit mode when there's no data?" Answer: "There's nothing to view yet — showing an empty view would be pointless."

### Step 7 (20 min) — Build View Mode

This is the new concept for Day 2. Build the view mode rendering:

```tsx
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
        {/* ... repeat for each field ... */}
      </View>
      <Pressable style={styles.button} onPress={() => setIsEditing(true)}>
        <Text style={styles.buttonText}>Edit Profile</Text>
      </Pressable>
    </ScrollView>
  );
}
```

**Teaching points:**
- The card uses `overflow: "hidden"` so divider lines don't bleed outside rounded corners
- `StyleSheet.hairlineWidth` gives a 1-pixel line on any screen density
- The "Edit Profile" button just sets `isEditing(true)` — the component re-renders and shows the form

**Run the app.** Since no data is saved yet, it goes straight to edit mode. Fill in data, but don't save yet — we need to update the save handler first.

### Step 8 (20 min) — Save + Cancel Handlers

**handleSubmit — save and switch to view mode:**

```tsx
async function handleSubmit() {
  if (!validate()) return;
  const profileData: ProfileData = { firstName, lastName, email, studentId, phone };
  await storage.set(STORAGE_KEYS.PROFILE, profileData);
  setErrors({});
  setHasSavedData(true);
  setIsEditing(false);  // Switch to view mode
}
```

**Ask:** "Why no Alert this time?" Answer: "The view mode IS the confirmation. The user sees their data displayed cleanly — that proves it saved. No alert needed."

**handleCancel — discard changes:**

```tsx
async function handleCancel() {
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
```

**Ask:** "Why do we reload from storage instead of just switching to view mode?" Answer: "Because the user might have changed fields in the form. Cancel means discard those changes and go back to what was saved."

**Add the buttons to edit mode:**

```tsx
{hasSavedData ? (
  <View style={styles.buttonRow}>
    <Pressable style={styles.cancelButton} onPress={handleCancel}>
      <Text style={styles.cancelButtonText}>Cancel</Text>
    </Pressable>
    <Pressable style={[styles.saveButton, !isFormFilled && styles.buttonDisabled]}
      onPress={handleSubmit} disabled={!isFormFilled}>
      <Text style={styles.buttonText}>Save Profile</Text>
    </Pressable>
  </View>
) : (
  <Pressable style={[styles.button, !isFormFilled && styles.buttonDisabled]}
    onPress={handleSubmit} disabled={!isFormFilled}>
    <Text style={styles.buttonText}>Save Profile</Text>
  </Pressable>
)}
```

**Ask:** "Why do we only show Cancel when `hasSavedData` is true?" Answer: "If the user has never saved anything, there's nothing to cancel back to. The first time, they just see Save."

**Demo the full flow:**
1. Navigate to Profile — no data, goes to edit mode (Save only, no Cancel)
2. Fill in valid data, press Save
3. Switches to view mode — data displayed in a clean card!
4. Tap "Edit Profile" — form appears, pre-filled, with Cancel + Save buttons
5. Change a field, then press Cancel — reverts to saved data, back to view mode
6. Close and reopen the app → navigate to profile → view mode with saved data!

**This is the "wow" moment.** The screen now behaves like a real app.

### Step 9 (15 min) — Review the Complete Pattern

Zoom out and show both files side by side. Highlight the shared pattern:

```
The Persistence Pattern (used in BOTH screens):
────────────────────────────────────────────────
1. Import storage utility
2. Add isLoading state (starts true)
3. useEffect on mount → load from storage → set state → set isLoading false
4. On user action → save to storage
5. Show spinner while loading
```

**The profile screen adds a bonus pattern:**

```
The View/Edit Pattern:
──────────────────────
1. isEditing state controls which UI renders
2. useEffect decides initial mode based on existing data
3. Save → switches to view mode (view IS the confirmation)
4. Cancel → reloads saved data, switches to view mode
5. hasSavedData controls whether Cancel button appears
```

> "This view/edit pattern shows up everywhere — settings screens, profile pages, admin panels. The core idea: show data as read-only by default, switch to edit mode on demand."

### Step 10 (15 min) — Common Mistakes (Live Demo)

Demonstrate at least two of these live:

1. **Forget the `[]` on useEffect** — Show the console rapidly logging "loading..." as the effect runs in an infinite loop. Add `[]` to fix it.

2. **Forget `if (saved !== null)`** — Clear AsyncStorage manually or use a new key. Show the crash when trying to access `.firstName` on `null`. Add the guard.

3. **Make useEffect async** — Show the TypeScript/lint warning. Explain why React can't handle a Promise return. Fix with the nested function pattern.

### Step 11 (15 min) — Student Challenge

Present the Dark Mode toggle challenge:

- Add a "Dark Mode" toggle to Settings (below Notifications)
- Uses the same AppCard + Switch pattern
- Persists to storage with a new key (`STORAGE_KEYS.THEME`)
- Loads on mount alongside notifications
- Survives app restarts

**Don't solve it for them.** They have the complete pattern from notifications — this is pure application. Walk around and help individually.

**If students finish early:**
- Bonus: Add a text indicator showing the stored value ("Stored: true/false")
- Bonus: Add a "Clear All Data" button that calls `storage.remove` on all keys and resets state

### Day 2 Closing (10 min)

Zoom out and connect to the bigger picture:

> "Your app now has memory. Profile data survives restarts. Preferences stick. And the profile screen behaves like a real app — view mode by default, edit on demand. In Week 10, we'll fetch data from an API — and the loading state pattern you learned today (isLoading → spinner → data) is exactly the same pattern you'll use for network requests."

**Quick knowledge check — ask these out loud:**
1. "What's the difference between `useState` and AsyncStorage?" (useState is in-memory and lost on unmount; AsyncStorage is on-device and persists)
2. "When does useEffect with `[]` run?" (Once, after the first render)
3. "Why do we need a loading state?" (To prevent the UI from flashing default values before stored data loads)
4. "What decides whether the profile screen opens in view mode or edit mode?" (Whether saved data exists in storage)

---

## Troubleshooting During Class

| Student says... | Likely cause | Fix |
|----------------|-------------|-----|
| "AsyncStorage is not found" | Package not installed or Metro cache | Run `npx expo install @react-native-async-storage/async-storage`, restart Metro with `--clear` |
| "My toggle always resets to ON" | Missing `useEffect` or missing `[]` dependency | Check that useEffect exists and has `[]` |
| "The app freezes when I open Settings" | useEffect without `[]` causing infinite loop | Add the empty dependency array |
| "Saved data doesn't load" | Wrong storage key (typo) or not checking for null | Use `STORAGE_KEYS` constants, add null check |
| "I see a flash of empty fields" | Missing `isLoading` state | Add `isLoading` with ActivityIndicator |
| "Profile data loads but toggle doesn't" | Loading notification as string instead of boolean | Check that `storage.get<boolean>` is used |
| "handleSubmit doesn't save" | `handleSubmit` not marked as `async` or missing `await` | Add `async` keyword and `await` before `storage.set` |
| "Cancel doesn't revert my changes" | Not reloading from storage in `handleCancel` | Make sure `handleCancel` calls `storage.get` and repopulates all fields |
| "View mode shows but fields are empty" | `setHasSavedData(true)` missing from useEffect or handleSubmit | Ensure `hasSavedData` is set when data exists |
| "Import errors for storage" | Wrong relative path | From `settings/`, the path is `../../../lib/storage` |

---

## Pacing Notes

### Day 1
- **If running ahead:** Have students add `storage.remove` to a "Reset Notifications" button. This exercises the third utility function and gives them more practice with async operations.
- **If running behind:** Skip the detailed explanation of `as const` and generics in the utility. Students can read about these in the guide. Prioritize getting the toggle working.
- **If students struggle with useEffect:** Draw the timeline on the board again. The visual of "mount → effect → setState → re-render" clicks faster than code examples.

### Day 2
- **If running ahead:** Have students refactor the five separate `useState` calls into a single `useState<ProfileData>` object. This is a natural extension and teaches them about state shape decisions.
- **If running behind:** Skip Step 10 (common mistakes live demo). Students can read about them in the guide. Prioritize getting the view/edit flow working and the student challenge.
- **If students struggle with view/edit mode:** Draw the flow on the board: "First visit → edit. Return visit → view → edit → save → view." The state machine is simple once they see it visually.

---

## Files students should have at the end of Week 9

```
lib/
└── storage.ts                ← Storage utility (NEW)

app/(tab)/settings/
├── _layout.tsx               ← Stack navigator (title changed to "Profile")
├── index.tsx                 ← Settings list (NOW loads/saves notifications)
└── profile.tsx               ← Profile (NOW has view mode + edit mode with persistence)
```

The `lib/` folder is new. The settings layout has a minor title change. The real changes are inside `index.tsx` (persistence) and `profile.tsx` (persistence + view/edit mode).
