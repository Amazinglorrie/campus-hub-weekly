# Week 8 — Instructor Plan: Forms + Validation

> **This file is gitignored. Students should never see this.**

---

## At a Glance

```
SESSION     DURATION    FOCUS
────────    ────────    ─────
Day 1       2 hours     Install libraries, Zod schema, Controller basics, form UI
            (separate day)
Day 2       2 hours     Error display, submit handling, mode options, student challenge
```

Students leave Day 1 with a form that captures input using React Hook Form but doesn't display errors yet.
Students leave Day 2 with a fully working, schema-validated form.

---

## Tech Stack for This Week

| Library | Role | Docs |
|---------|------|------|
| `react-hook-form` | Manages form state, tracks dirty/touched, calls validation on submit | [react-hook-form.com](https://react-hook-form.com/) |
| `zod` | Defines validation rules as a schema (the "what is valid") | [zod.dev](https://zod.dev/) |
| `@hookform/resolvers` | Bridges RHF and Zod so they work together with one line | [github.com/react-hook-form/resolvers](https://github.com/react-hook-form/resolvers) |

**Why this stack?**
- No manual `validate()` function — rules live in the schema, not scattered across the component
- TypeScript types are inferred automatically from the Zod schema (`z.infer<typeof schema>`)
- Industry standard — students will encounter this pattern in real jobs
- Less boilerplate than Formik, better TS support than Yup

### Library Background — What to Tell Students

**React Hook Form** is one of the most downloaded React libraries in the world (~12 million weekly downloads). It solves the problem of coordinating form state — instead of a `useState` per field plus manual tracking of what's dirty, what's been touched, and when to show errors, you call `useForm` once and it handles all of that internally. The key insight for students: RHF manages state *outside* the React render cycle using a ref-based approach, which is why it's extremely performant even on large forms.

> Key reference pages to bookmark: [useForm API](https://react-hook-form.com/docs/useform) | [Controller](https://react-hook-form.com/docs/usecontroller/controller) | [formState](https://react-hook-form.com/docs/useform/formstate)

**Zod** is the current TypeScript-first standard for data validation. Unlike Yup (which was the previous standard and added TypeScript support later), Zod was designed for TypeScript from the ground up — so type inference is exact and automatic. Students should understand that Zod is used far beyond forms: validating API responses, environment variables, config files, and anywhere data crosses a boundary. The mental model is: *describe the shape of valid data once, check anything against it anywhere*.

> Key reference pages to bookmark: [Zod basics](https://zod.dev/?id=basic-usage) | [String validators](https://zod.dev/?id=strings) | [.refine() for custom rules](https://zod.dev/?id=refine)

**@hookform/resolvers** is a thin adapter package. RHF's `resolver` option accepts any function that takes form values and returns `{ values, errors }`. The resolvers package implements this contract for Zod (and other libraries). Students don't need to understand the internals — just that `zodResolver(schema)` is the one line that connects the two libraries.

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

- [ ] Run `npm install react-hook-form zod @hookform/resolvers` in the project before class
- [ ] Have the app running and ready to demo live
- [ ] Open `app/(tab)/courses/_layout.tsx` — you'll reference it when creating `settings/_layout.tsx`
- [ ] Open `app/(tab)/courses/index.tsx` — you'll reference the `Pressable` + `router.push` pattern
- [ ] Have the finished `profile.tsx` ready but **don't show it yet** — build it live

---

## Day 1 (2 hours) — Schema, Controller, Form UI

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

### Step 3 (20 min) — Introduce the Library Stack

**Don't start with code.** Set the context first.

> "Every form you've ever filled in online — login, signup, checkout — has two things: a way to capture what the user typed, and a way to check if it's valid. We could write both of those by hand, and we did in older React code. But today, we use two libraries that split these jobs cleanly."

Draw or show this division:

```
┌─────────────────────────────────────────────────────────┐
│  react-hook-form                                         │
│  ─────────────────────────────────────────────────────  │
│  "Track what the user typed. Know which fields are       │
│   dirty. Know when to show errors. Call the validator." │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  zod                                                     │
│  ─────────────────────────────────────────────────────  │
│  "Define the rules. What shape is valid data?            │
│   firstName must be at least 2 chars. email must be     │
│   a real email. etc."                                    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  @hookform/resolvers/zod                                 │
│  ─────────────────────────────────────────────────────  │
│  "The adapter. Plugs Zod into React Hook Form so they   │
│   speak the same language. One import, one line."        │
└─────────────────────────────────────────────────────────┘
```

### Step 4 (20 min) — Write the Zod Schema

Start `profile.tsx` with just the schema. No JSX yet.

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

**Go through each rule line by line and explain:**
- `.trim()` — strips leading/trailing spaces before checking. Type `"  "` — it's technically 2 chars but empty after trim.
- `.min(2, "message")` — Zod includes the error message right in the rule. No separate `errors` object to manage.
- `.email()` — Zod has a built-in email check. No regex to write or explain.
- `.length(9)` — must be exactly 9. Not min, not max — exactly.
- `.refine()` — for custom rules Zod doesn't cover built-in. The function returns `true` (valid) or `false` (invalid). **Explain the phone logic:** strip non-digits with `replace(/\D/g, "")`, then check if ≥ 10 digits remain. This lets users type `(403) 555-0123` in any format.

**The type inference moment** — point at `z.infer<typeof profileSchema>`:
> "This is why the industry moved to Zod. We write the schema once, and TypeScript automatically knows what shape the form data has. We didn't write a separate `type ProfileForm` by hand — Zod generated it for us."

### Step 5 (25 min) — `useForm` + `Controller`

Now add the component:

```tsx
const {
  control,
  handleSubmit,
  formState: { errors },
} = useForm<ProfileForm>({
  resolver: zodResolver(profileSchema),
  defaultValues: {
    firstName: "", lastName: "", email: "", studentId: "", phone: "",
  },
  mode: "onSubmit",
});
```

**Explain each piece:**

| Piece | What it does |
|-------|-------------|
| `control` | The "registration system" — passed to each `Controller` so RHF knows about each field |
| `handleSubmit` | Wraps your `onSubmit`. Validates first, only calls your function if schema passes |
| `formState.errors` | Object of errors, keyed by field name. Populated after submit attempt |
| `resolver: zodResolver(...)` | Plugs Zod in. One line replaces our entire manual `validate()` function |
| `defaultValues` | Initial field values. Required for controlled inputs |
| `mode: "onSubmit"` | Only validate when user presses submit (not on every keystroke) |

Now show the first `Controller` for First Name:

```tsx
<Controller
  control={control}
  name="firstName"
  render={({ field: { onChange, value } }) => (
    <TextInput
      value={value}
      onChangeText={onChange}
      placeholder="e.g. Jane"
    />
  )}
/>
```

**Why `Controller` instead of `register`?**
> "React Hook Form has two ways to connect inputs. `register` works great for plain HTML `<input>` elements. But React Native's `TextInput` isn't an HTML element — it uses `onChangeText` instead of `onChange`. `Controller` is the React Native-friendly wrapper. You give it the field name, and it gives you back `value` and `onChange` through the render prop. Just pass them to your `TextInput`."

Build the remaining four fields following the exact same pattern. Let students watch for First Name, then have them try Last Name on their own. Compare their code — it should be nearly identical with just the names changed.

### Step 6 (10 min) — The submit button

```tsx
function onSubmit(data: ProfileForm) {
  Alert.alert("Profile Saved", "Your profile has been updated.", [
    { text: "OK", onPress: () => router.back() },
  ]);
}

<Pressable style={styles.button} onPress={handleSubmit(onSubmit)}>
  <Text style={styles.buttonText}>Save Profile</Text>
</Pressable>
```

**Key point:** `handleSubmit(onSubmit)` — not `onSubmit` directly. `handleSubmit` is RHF's wrapper:
1. It runs validation against the Zod schema
2. If invalid, it populates `errors` and re-renders. Your `onSubmit` never runs.
3. If valid, it calls your `onSubmit` with the fully typed form data.

Run the app. Fill every field. Press Save. Alert appears. **Leave error display for Day 2.**

### Day 1 Closing (10 min)

Run the full app. Walk through what works:
- Settings tab loads, Account card is tappable
- Edit Profile screen has five inputs that capture text
- Press Save with valid data → success alert
- Press Save with empty fields → nothing visible happens yet (errors aren't displayed)

**Set up Day 2:**
> "The form validates — but the user can't see why it failed. `formState.errors` has all the information, but we haven't wired it to the UI yet. That's Day 2."

**Homework (optional):** Read the "React Hook Form + Zod" section of `WEEK8_FORMS.md`. Come ready to explain what `Controller` does and why we need it.

---

## Before Class (Day 2)

### Prep checklist

- [ ] Make sure Day 1 code is working on your machine
- [ ] Prepare the student challenge requirements on a slide or handout

### What students should have from Day 1

```
app/(tab)/settings/
├── _layout.tsx       ← Stack navigator
├── index.tsx         ← Settings list (Account card tappable)
└── profile.tsx       ← Form with 5 Controller fields + submit (NO error display yet)

styles/theme.ts       ← Updated with error color + input radius
```

---

## Day 2 (2 hours) — Error Display + Polish + Student Challenge

### Opening (10 min) — Recap Day 1

**Ask these out loud — let students answer:**
1. "What are the three libraries and what does each do?" (RHF = state/flow, Zod = rules, resolvers = glue)
2. "Why do we use `Controller` in React Native instead of `register`?" (TextInput isn't an HTML input, uses `onChangeText`)
3. "What does `handleSubmit` do before calling our `onSubmit`?" (Runs Zod validation first)

**Then demonstrate the problem we're solving today:**

Run the app. Type "x" in every field. Press Save. Nothing visible happens — no errors, no feedback. The validation ran and failed, but the user has no idea.

> "All the validation information exists in `formState.errors`. We just haven't connected it to the screen yet. Today we fix that."

### Step 7 (25 min) — Wiring Up Error Display

**Show `formState.errors` in the console first** (or mention it conceptually):

> "After a failed submit, `errors` is an object like this:
> ```
> {
>   firstName: { message: "First name must be at least 2 characters." },
>   email: { message: "Please enter a valid email address." }
> }
> ```
> Valid fields don't appear. Only failed fields get an entry."

Do the first field together — First Name:

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

{/* Error message below the input */}
{errors.firstName && (
  <Text style={styles.error}>{errors.firstName.message}</Text>
)}
```

**Explain each change:**
- `errors.firstName && styles.inputError` — conditional style in an array. If `errors.firstName` is undefined (no error), nothing extra is applied. If it's an object (error exists), `inputError` overrides just the `borderColor`.
- `errors.firstName.message` — the exact string we put in the Zod schema. No duplication — write the message once in the schema, display it here.

Give students 5 minutes to add error display for the remaining four fields on their own. Walk around and help.

**Common issue to watch for:** Students writing `errors.firstName?.message` with optional chaining. Technically fine, but explain that `errors.firstName` is already `undefined` when there's no error, so the short-circuit `&&` before the `<Text>` already protects us.

### Step 8 (15 min) — Mode Options

Now that error display works, introduce the `mode` option:

```tsx
useForm({ mode: "onSubmit" })    // Default — validate only when Submit pressed
useForm({ mode: "onBlur" })      // Validate when user leaves a field
useForm({ mode: "onChange" })    // Validate on every keystroke
```

**Live demo — switch to `"onBlur"`:**
- Type "J" in First Name, then tap to the next field
- Error appears immediately after leaving the field

**Ask the class:** "Is this better or worse than `onSubmit` mode?"

Let them discuss. There's no single right answer — it depends on UX preference. `onBlur` is common in production apps. For this course, `onSubmit` keeps things simpler.

**Switch back to `"onSubmit"`** before moving on.

### Step 9 (15 min) — Common Mistakes Walkthrough

Don't just list these — **demonstrate them live**:

1. **Missing `defaultValues`** → Remove `defaultValues`. Type in a field, press save. RHF loses track of the initial value. Add it back.

2. **Using `onChange` instead of `onChangeText`** in the `TextInput`:
   ```tsx
   // WRONG — this is HTML's onChange
   <TextInput onChange={onChange} />

   // CORRECT — React Native uses onChangeText
   <TextInput onChangeText={onChange} />
   ```
   Show the broken behavior (typing does nothing), then fix it.

3. **Calling `onSubmit` directly instead of `handleSubmit(onSubmit)`:**
   ```tsx
   // WRONG — skips validation entirely
   onPress={onSubmit}

   // CORRECT — runs Zod first
   onPress={handleSubmit(onSubmit)}
   ```

4. **Forgetting `resolver`** → Remove `zodResolver`. Press save with empty fields. Submits successfully — Zod schema is ignored. Add it back.

### Step 10 (20 min) — Student Challenge

Present the Program selection challenge. Give them the requirements:

- New field: Program (e.g. "Software Development", "Data Analytics", "Network Systems")
- Add it to the Zod schema: `program: z.string().min(1, "Please select a program.")`
- Create a list of program options displayed as `Pressable` items the user taps to select
- Track the selected program with `useState<string>("")` (or `null`) — this field is **not** a `TextInput`, so use `Controller`'s `onChange` to set it manually when a Pressable is tapped
- Highlight the selected program visually
- Show the selected program in the success alert

**Hint to give students for non-TextInput fields with Controller:**
```tsx
<Controller
  control={control}
  name="program"
  render={({ field: { onChange, value } }) => (
    <View>
      {PROGRAMS.map((p) => (
        <Pressable key={p} onPress={() => onChange(p)}>
          <Text>{p}</Text>
        </Pressable>
      ))}
    </View>
  )}
/>
```

This pattern — using `Controller` with a non-TextInput component — is exactly what they'll use in the lab for Category and Urgency.

If students finish early, bonus challenge: use `mode: "onBlur"` and see how the experience changes.

### Day 2 Closing (10 min)

Zoom out and connect to the bigger picture:

> "You now know the pattern that real production apps use for forms. The schema-first approach — define what valid data looks like, then let the library handle the rest — scales to 50-field enterprise forms just as well as our 5-field profile form. Next week we'll persist this data so it survives when you close the app."

**Quick knowledge check — ask these out loud:**
1. "Where do validation rules live now?" (In the Zod schema)
2. "What does `handleSubmit` do?" (Runs validation, only calls onSubmit if valid)
3. "Why `Controller` instead of `register`?" (React Native's TextInput needs onChangeText, not onChange)

---

## Troubleshooting During Class

| Student says... | Likely cause | Fix |
|----------------|-------------|-----|
| "My Settings tab disappeared" | Both `settings.tsx` and `settings/` exist | Delete `settings.tsx` |
| "Typing doesn't do anything" | Using `onChange` instead of `onChangeText` in TextInput | Change to `onChangeText={onChange}` |
| "Errors never show" | `errors` from `formState` not destructured, or missing `resolver` | Check `useForm` setup |
| "Submit always succeeds even with bad data" | Missing `resolver: zodResolver(profileSchema)` | Add the resolver |
| "TypeScript errors on `errors.firstName.message`" | Accessing `.message` without checking if error exists first | Use `errors.firstName?.message` or guard with `&&` |
| "Back button doesn't appear" | Missing `_layout.tsx` in the settings folder | Create it with the Stack navigator |
| "Imports are broken" | Relative paths didn't get updated after moving to settings/ folder | Need one more `../` — three levels up now |

---

## Pacing Notes

### Day 1
- **If running ahead:** Show the Zod docs briefly — let students see `.url()`, `.uuid()`, `.min()` with no message arg. Builds curiosity for what schemas can do.
- **If running behind:** Skip building all five fields live — do First Name and Last Name together, have students complete Email, Student ID, and Phone as a brief pair activity.
- **If students are confused by `Controller`:** Go back to the analogy — "RHF is the manager. `Controller` is how the manager hands a field to RHF to track. You hand it a name and a render function. The render function gets `value` and `onChange` back."

### Day 2
- **If running ahead:** Extend the student challenge — have them add a `z.discriminatedUnion` or a `z.enum(["Software Development", "Data Analytics", "Network Systems"])` for the program field instead of just `z.string()`.
- **If running behind:** Skip the mode demo (Step 8). Students can experiment on their own. Prioritize Step 7 (error display) and the student challenge.
- **If Day 1 code is broken for some students:** Spend the first 10 minutes of Day 2 helping them catch up. Pair them with a student who has working code.

---

## Files students should have at the end of Week 8

```
app/(tab)/settings/
├── _layout.tsx       ← Stack navigator (2 screens)
├── index.tsx         ← Settings list (Account card now tappable)
└── profile.tsx       ← Edit Profile form (RHF + Zod, 5 fields)

styles/theme.ts       ← Updated with error color + input radius
```

The old `app/(tab)/settings.tsx` should be **deleted**.

### Dependencies added this week

```
react-hook-form
zod
@hookform/resolvers
```
