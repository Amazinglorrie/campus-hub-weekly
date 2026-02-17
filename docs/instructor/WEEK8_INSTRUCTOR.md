# Week 8 — Instructor Plan: Forms + Validation

> **This file is gitignored. Students should never see this.**

---

## At a Glance

```
SESSION     DURATION    FOCUS
────────    ────────    ─────
Day 1       2 hours     State, controlled inputs, building the form UI
            (separate day)
Day 2       2 hours     Validation logic, error display, submit handling
```

Students leave Day 1 with a form that looks right but doesn't validate.
Students leave Day 2 with a fully working, validated form.

---

## Before Class (Day 1)

### What students already know (Weeks 1–7)

- TypeScript fundamentals (6 weeks of foundation)
- File-based routing, Stack and Tab navigation (Week 7)
- Nested navigation — Stack inside a Tab (the `courses/` pattern)
- `useState` basics (they've used it for the notifications toggle in `settings.tsx`)
- The `AppCard` component and centralized theming

### What's already on their machines

The app has 3 tabs. Settings is a single file (`settings.tsx`) with a notifications toggle and a static Account card. They've never built a form or validated input.

### Prep checklist

- [ ] Have the current app running on your machine so you can demo live
- [ ] Open `app/(tab)/courses/_layout.tsx` in a tab — you'll reference it when creating `settings/_layout.tsx`
- [ ] Open `app/(tab)/courses/index.tsx` in a tab — you'll reference the `Pressable` + `router.push` pattern
- [ ] Have the finished `profile.tsx` ready but **don't show it yet** — build it live

---

## Day 1 (2 hours) — State + Controlled Inputs + Form UI

### Opening (10 min) — Connect to What They Know

Start by running the app and navigating to the Settings tab.

**Say something like:**
> "Last week you built the Courses tab — a folder with its own Stack navigator. Tapping a course pushes to a detail screen. Today we're doing the exact same thing to Settings. By the end of today, tapping the Account card will push to an Edit Profile form. Same navigation pattern, new content."

Tap the Account card to show that nothing happens. This is the "before" — by end of Day 1, the navigation will work and the form will be on screen.

### Step 1 (15 min) — Convert `settings.tsx` to a folder

This is the most important teaching moment of Day 1. Students see the nested Stack pattern for the **second time**.

1. **Side-by-side:** Show `courses/_layout.tsx` on one side of the screen
2. **Ask the class:** "If I wanted Settings to have its own Stack — a list screen and a detail screen — what would the folder structure look like?"
3. Let them answer. They should be able to guess based on `courses/`.
4. **Live code:** Create `settings/_layout.tsx` — type it out, don't copy-paste

```
courses/              settings/
├── _layout.tsx  →    ├── _layout.tsx    (same pattern)
├── index.tsx    →    ├── index.tsx      (same pattern)
└── [id].tsx          └── profile.tsx    (static route instead of dynamic)
```

5. Move contents of `settings.tsx` into `settings/index.tsx`
6. **Delete `settings.tsx`** — explain why (duplicate route conflict)
7. Run the app — Settings tab should still work exactly as before

**Key point to emphasize:** "No changes needed in the Tab layout. Expo Router is smart enough to resolve `name='settings'` to the `settings/` folder, just like it does for `courses/`. You've seen this before."

### Step 2 (10 min) — Make the Account card tappable

Show `courses/index.tsx` — point out the `Pressable` wrapper and `router.push`.

**Ask:** "How would you make the Account card navigate to a profile screen?"

Live code the changes:
- Wrap Account card in `Pressable`
- Add `router.push("/(tab)/settings/profile")`
- Swap icon to `chevron-forward` (ask why — visual consistency with Courses)

Run the app. Tapping Account should crash or show a blank screen (profile.tsx doesn't exist yet). That's fine — it proves the navigation works.

### Step 3 (20 min) — Introduce controlled inputs

This is the concept they need to understand before writing the form.

**Don't jump into code yet.** Explain the idea first:

> "In a normal input field, the field manages its own text. You type, it shows what you typed. Your code has to go ask the input 'hey, what do you have right now?' whenever it needs the value."
>
> "A controlled input is the opposite. React state is the boss. The input is not allowed to show anything on its own — it can only display what React tells it to."

Draw or show this cycle on the board/screen:

```
User types → onChangeText fires → setState → re-render → input shows value from state
     ↑                                                              │
     └──────────────────── cycle repeats ◀──────────────────────────┘
```

Then explain the three pieces:

| Piece | What it does | What breaks without it |
|-------|-------------|----------------------|
| `useState("")` | Stores the value | No memory between renders |
| `value={firstName}` | Tells input what to show | Input manages itself, React can't control it |
| `onChangeText={setFirstName}` | Updates state on keypress | Input appears frozen |

**Demo:** Create a minimal `profile.tsx` with just ONE input field (First Name) to prove the concept works. Show that typing updates state. Add a `<Text>` below that shows `firstName` live so students can see state changing in real time.

```tsx
<TextInput value={firstName} onChangeText={setFirstName} />
<Text>You typed: {firstName}</Text>
```

**Remove the debug `<Text>` after the demo** — it was just to prove the point.

### Step 4 (25 min) — Build the form UI

Now add all five fields. Live code this — have students follow along.

Go through each field one at a time:
1. **First Name** — `autoCapitalize="words"` (ask: "why words and not sentences?")
2. **Last Name** — `autoCapitalize="words"` (same reasoning as First Name — proper name capitalization)
3. **Email** — `keyboardType="email-address"`, `autoCapitalize="none"` (show how the keyboard changes on a phone/simulator)
4. **Student ID** — `autoCapitalize="characters"`, `maxLength={9}` (explain maxLength as a first line of defense, not validation)
5. **Phone Number** — `keyboardType="phone-pad"` (show how the keyboard switches to the numeric dialer layout)

For each field, follow the same structure:
```
Label → TextInput → (error message placeholder — leave empty for now)
```

Style as you go. Use `theme.ts` values — don't hardcode colors or spacing. Add `error` and `input` to the theme first if you haven't already.

### Step 5 (15 min) — The submit button + disabled state

Introduce the `isFormFilled` concept:

```tsx
const isFormFilled =
  firstName.length > 0 && lastName.length > 0 && email.length > 0 &&
  studentId.length > 0 && phone.length > 0;
```

**Ask the class:** "Is this validation?" (No — it just checks something was typed, not that it's correct.)

Build the button with both visual and functional disabled states. Run the app — show that the button is faded when fields are empty and solid when all fields have text.

### Day 1 Closing (10 min)

Run the full app. Walk through what works:
- Settings tab loads
- Tapping Account pushes to the Edit Profile screen (with back button)
- Five input fields accept text (First Name, Last Name, Email, Student ID, Phone Number)
- Button enables when all fields have text
- Pressing Save does... nothing useful yet

**Set up Day 2:**
> "Right now you can type 'x' in every field and press Save. The app is happy. That's a problem. Next class we add validation — the app will check if the data is actually correct before accepting it."

**Homework (optional):** Read the "Controlled Inputs" section of `WEEK8_FORMS.md`. Come to Day 2 ready to explain the cycle in your own words.

---

## Before Class (Day 2)

### Prep checklist

- [ ] Make sure the Day 1 code is working on your machine
- [ ] Have a version with intentional bugs ready for the common mistakes demo (Step 10)
- [ ] Prepare the student challenge requirements on a slide or handout

### What students should have from Day 1

```
app/(tab)/settings/
├── _layout.tsx       ← Stack navigator
├── index.tsx         ← Settings list (Account card tappable)
└── profile.tsx       ← Form with 5 inputs + submit button (NO validation yet)

styles/theme.ts       ← Updated with error color + input radius
```

If any students are missing Day 1 code, give them 5 minutes at the start to catch up using the guide.

---

## Day 2 (2 hours) — Validation + Error Display + Submit

### Opening (10 min) — Recap Day 1

Don't assume they remember everything. Quick interactive recap:

**Ask these out loud — let students answer:**
1. "What did we do to the Settings tab structure?" (Converted from a single file to a folder with a Stack)
2. "Why did we delete `settings.tsx`?" (Duplicate route conflict with `settings/index.tsx`)
3. "What makes our TextInputs 'controlled'?" (The `value` prop is tied to state)

**Then demonstrate the problem we're solving today:**

Run the app. Type "x" in every field. Press Save. Nothing happens — or worse, it "succeeds" with garbage data.

> "The form accepts anything right now. Today we fix that. By the end of class, the app will reject bad input and show clear error messages."

### Step 6 (30 min) — The `validate()` function

This is the core of Day 2. Build it rule by rule.

**Start with the name fields.** Mention the error type first:

```tsx
type FormErrors = {
  firstName?: string;
  lastName?: string;
  email?: string;
  studentId?: string;
  phone?: string;
};
```

> "We give this type a name — `FormErrors` — instead of writing it inline. It keeps the code cleaner, especially now that we have five fields."

Then build the function, starting with `firstName` and `lastName`:

```tsx
function validate() {
  const newErrors: FormErrors = {};

  if (firstName.trim().length < 2) {
    newErrors.firstName = "First name must be at least 2 characters.";
  }

  if (lastName.trim().length < 2) {
    newErrors.lastName = "Last name must be at least 2 characters.";
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
}
```

**Pause and explain:**
- Why `trim()`? — Type 3 spaces in the First Name field. It looks filled but it's empty. `trim()` catches this.
- Why a fresh `newErrors` object each time? — If you reuse old errors, fixed fields still show errors.
- Why `Object.keys().length === 0`? — If no keys were added, nothing was wrong → return true.
- Why validate both `firstName` and `lastName` the same way? — Same rule, different fields. Ask: "Could we write a helper? Sure, but let's keep it explicit for now."

**Then add email validation:**

```tsx
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
```

Don't spend more than 2–3 minutes on regex. Say:
> "This checks: something @ something . something. It's not perfect, but it catches obvious mistakes. Production apps use libraries for this — for now, this is enough."

Test with: `"jane"` (fails), `"jane@"` (fails), `"jane@edu.ca"` (passes).

**Then add Student ID validation:**

```tsx
if (studentId.trim().length !== 9) {
  newErrors.studentId = "Student ID must be exactly 9 characters.";
}
```

Straightforward — just a length check.

**Then add Phone Number validation:**

```tsx
if (phone.replace(/\D/g, "").length < 10) {
  newErrors.phone = "Phone number must be at least 10 digits.";
}
```

**Explain the regex:** `\D` matches any non-digit character. `replace(/\D/g, "")` strips everything that isn't a digit — dashes, parentheses, spaces. Then we check if the remaining digits are at least 10. This means students can type `(604) 555-1234` and it still passes because the digits alone are `6045551234` (10 digits).

### Step 7 (20 min) — Displaying errors

Now wire up the error messages in JSX. Do the first field together, then let students try the other four on their own for 5 minutes.

```tsx
{errors.firstName && <Text style={styles.error}>{errors.firstName}</Text>}
```

**Explain the pattern:** `{condition && <Component />}` — short-circuit rendering. If `errors.firstName` is undefined (no error), nothing renders. If it has a string, the `<Text>` appears.

**Then add the red border:**

```tsx
style={[styles.input, errors.firstName && styles.inputError]}
```

**Ask:** "Why is this an array?" — React Native merges the styles. The second style only applies when there's an error, and it overrides just the `borderColor`.

Give students 5 minutes to add error display for lastName, email, studentId, and phone on their own. Walk around and help.

### Step 8 (15 min) — The submit handler

```tsx
function handleSubmit() {
  if (!validate()) return;
  Alert.alert(
    "Profile Saved",
    `Name: ${firstName} ${lastName}\nEmail: ${email}\nID: ${studentId}\nPhone: ${phone}`
  );
}
```

Wire it to the button's `onPress`. Test the full flow:

1. Leave all fields empty, try to press Save → button is disabled (can't press)
2. Type "x" in each field, press Save → errors appear (validation fails)
3. Fix each field with valid data, press Save → success alert

**This is the satisfying moment.** Let students experience the full cycle.

### Step 9 (15 min) — Common mistakes walkthrough

Don't just list these — **demonstrate them live**:

1. **Put `settings.tsx` back alongside the folder** → show the crash. Delete it again. "This is why we delete the old file."

2. **Remove `trim()` from the firstName check** → type 3 spaces, submit. It passes validation but the name is empty. Add `trim()` back.

3. **Add `validate()` inside `onChangeText`** → type one character in email, watch the error flash immediately. "See why we only validate on submit? Let them finish typing."

### Step 10 (20 min) — Student challenge

Present the Program selection challenge. Give them the requirements:

- New field: Program (e.g. "Software Development", "Data Analytics", "Network Systems")
- Create a list of program options and display them as `Pressable` items the user can tap to select
- Highlight the selected program visually (different background color, border, etc.)
- Store the selected program in state
- Validation: a program must be selected before submitting
- Show the selected program in the success alert

**Don't solve it for them.** This is their chance to apply what they know — state management, Pressable (which they used in Courses), conditional styling, and validation. Walk around and help individually.

If students finish early, bonus challenge: add a "Clear Form" button that resets all state to empty strings, deselects the program, and clears errors.

### Day 2 Closing (10 min)

Zoom out and connect to the bigger picture:

> "You now know how to build any form. Login screens, signup screens, search filters, settings — they're all the same pattern: controlled inputs + validation on submit. Next week we'll save this profile data so it persists when you close the app."

**Quick knowledge check — ask these out loud:**
1. "What makes an input 'controlled'?" (value prop tied to state)
2. "When do we validate — every keystroke or on submit?" (on submit)
3. "What's the difference between `isFormFilled` and `validate()`?" (filled = has text, valid = text is correct)

---

## Troubleshooting During Class

| Student says... | Likely cause | Fix |
|----------------|-------------|-----|
| "My Settings tab disappeared" | Both `settings.tsx` and `settings/` exist | Delete `settings.tsx` |
| "Typing doesn't do anything" | Missing `onChangeText` or the handler isn't calling `setState` | Check the TextInput props |
| "Errors never go away" | Reusing the old errors object instead of creating a fresh one | Make sure `validate()` starts with `const newErrors = {}` |
| "Button is always disabled" | `isFormFilled` check has a logic error (using `||` instead of `&&`) | Review the boolean logic |
| "Imports are broken" | Relative paths didn't get updated after moving to settings/ folder | Need one more `../` — three levels up now |
| "Back button doesn't appear" | Missing `_layout.tsx` in the settings folder | Create it with the Stack navigator |

---

## Pacing Notes

### Day 1
- **If running ahead:** Let students experiment with TextInput props — `secureTextEntry`, `multiline`, `autoCorrect={false}`. Builds curiosity for future forms.
- **If running behind:** Combine Steps 4 and 5. Build the button alongside the last input field instead of as a separate step.
- **If students are struggling with controlled inputs:** Keep the debug `<Text>You typed: {firstName}</Text>` under each field for the rest of Day 1. Seeing state change in real time makes it click faster than any explanation.

### Day 2
- **If running ahead:** Extend the student challenge — have them also add format validation to the Student ID (must start with "A00"). Or let them start on the bonus "Clear Form" button.
- **If running behind:** Skip the live common mistakes demo (Step 9). Students can read about them in the guide. Prioritize getting the full form working + student challenge time.
- **If Day 1 code is broken for some students:** Spend the first 10 minutes of Day 2 helping them catch up. Pair them with a student who has working code.

---

## Files students should have at the end of Week 8

```
app/(tab)/settings/
├── _layout.tsx       ← Stack navigator (2 screens)
├── index.tsx         ← Settings list (Account card now tappable)
└── profile.tsx       ← Edit Profile form (5 validated fields)

styles/theme.ts       ← Updated with error color + input radius
```

The old `app/(tab)/settings.tsx` should be **deleted**.
