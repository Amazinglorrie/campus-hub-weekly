# Lab 8: Forms + Validation

## Objective

Build a "Report Issue" form on a new screen inside the Home tab, using **React Hook Form + Zod** — the same library stack from the Week 8 guide. You will apply the schema-first approach to new field types: multiline text, selection groups, and colored indicators.

---

## What You Already Have

After completing the Week 8 guide, your app has:

- A **Settings** tab with a nested Stack (`settings/_layout.tsx` → `index.tsx` → `profile.tsx`)
- An **Edit Profile** form using React Hook Form + Zod with 5 validated fields
- Patterns for: `useForm`, `Controller`, Zod schemas, `zodResolver`, `handleSubmit`, error display, and conditional styling
- A centralized `theme.ts` with colors (`bg`, `card`, `text`, `muted`, `primary`, `border`, `error`) and radius values (`card`, `input`)
- A reusable `AppCard` component

You will **not** be modifying the profile form. This lab asks you to build something new using the same patterns.

---

## Scenario

SAIT wants students to be able to report campus issues (broken equipment, facility problems, safety concerns) directly from the Campus Hub app. Your job is to build the "Report Issue" form. It lives inside the Home tab and is accessible by tapping a card on the Home screen.

---

## Expected File Changes

When you are done, your project should have these new and modified files:

```
DELETED:   app/(tab)/home.tsx

CREATED:   app/(tab)/home/_layout.tsx        <-- Stack navigator for Home tab
CREATED:   app/(tab)/home/index.tsx          <-- Home screen (moved from home.tsx)
CREATED:   app/(tab)/home/report.tsx         <-- Report Issue form (NEW)

MODIFIED:  app/(tab)/_layout.tsx             <-- Update Tabs.Screen name if needed
```

This follows the **exact same pattern** you used when converting `settings.tsx` into the `settings/` folder in the Week 8 guide, and the same pattern used by the `courses/` folder from Week 7. If you are unsure how to do this, review the "Architecture Impact" section of `WEEK8_FORMS.md`.

**After your changes, the architecture should look like this:**

```
app/(tab)/_layout.tsx ................ Tabs
    |
    ├── home/_layout.tsx ............. Stack (Nested)   <-- NEW
    |       |
    |       ├── index.tsx ............ Home screen (moved content)
    |       └── report.tsx ........... Report Issue form (NEW)
    |
    ├── courses/_layout.tsx .......... Stack (Nested)   (Week 7)
    |       ├── index.tsx
    |       └── [id].tsx
    |
    └── settings/_layout.tsx ......... Stack (Nested)   (Week 8 guide)
            ├── index.tsx
            └── profile.tsx
```

---

## Tasks

### Task 1: Navigation Setup (10 marks)

Convert the Home tab from a single file into a folder with a nested Stack, then add a "Report Issue" card that navigates to the new form screen.

1. **Create the `home/` folder** with a `_layout.tsx` Stack navigator. Register two screens: `index` (title: "Home") and `report` (title: "Report Issue").
2. **Move the Home screen content** from `home.tsx` into `home/index.tsx`. Update import paths (you are one folder deeper now). Delete `home.tsx`.
3. **Add a tappable card** to the Home screen that navigates to the report form. Wrap an `AppCard` in a `Pressable` that calls `router.push("/(tab)/home/report")`. Use the title "Report Issue", a subtitle like "Report a campus problem", and a `chevron-forward` icon on the right.
4. Verify that tapping the card pushes to a blank `report.tsx` screen with a working back button.

---

### Task 2: Build the Report Issue Form (35 marks)

Create the form in `app/(tab)/home/report.tsx` using **React Hook Form + Zod**.

Start by defining your Zod schema and the `useForm` hook before building any JSX. This is the same schema-first approach from the profile form.

The form has five fields. Each has specific requirements that differ from the profile form — you cannot copy-paste.

#### Field 1: Title (7 marks)

- Standard `TextInput` (single line) connected via `Controller`
- Placeholder: `"e.g. Projector not working in N210"`
- Schema rule: validated in Task 3

#### Field 2: Category (7 marks)

- **Not a TextInput.** This is a selection group connected via `Controller`.
- Define a constant array **outside the component**:
  ```tsx
  const CATEGORIES = ["Facilities", "IT/Equipment", "Safety", "Other"];
  ```
- Inside the `Controller` render prop, use `onChange` and `value` to build a list of tappable `Pressable` items:
  - Tapping an item calls `onChange(categoryName)` to set the field value
  - Compare `value === category` to know which item is currently selected
  - Visually highlight the selected item (e.g., `theme.colors.primary` background with white text)
- Arrange items in a horizontal row using `flexDirection: "row"` and `flexWrap: "wrap"`

#### Field 3: Description (7 marks)

- **Multiline `TextInput`** — this is a new pattern you have not used before
- Connected via `Controller` the same way as a single-line input
- Use `multiline={true}` and `numberOfLines={4}` as props on the `TextInput`
- Add `textAlignVertical: "top"` to the style (so text starts at the top on Android)
- Set a `minHeight` of around 100 in the style
- Placeholder: `"Describe the issue in detail..."`

#### Field 4: Location (7 marks)

- Standard `TextInput` (single line) connected via `Controller`
- Placeholder: `"e.g. Building N, Room 210"`
- `autoCapitalize="words"`

#### Field 5: Urgency (7 marks)

- **Not a TextInput.** A colored selection group connected via `Controller`.
- Define a constant array **outside the component**:
  ```tsx
  const URGENCY_LEVELS = ["Low", "Medium", "High"];
  ```
- Each urgency level has a **distinct color** even when unselected:
  - Low: green (`#16a34a`)
  - Medium: amber (`#ca8a04`)
  - High: red (`#dc2626` / `theme.colors.error`)
- The selected level should look noticeably different from unselected (e.g., solid fill when selected, colored border when unselected)
- Arrange items in a horizontal row

---

### Task 3: Zod Schema + Validation (25 marks)

Define a Zod schema at the top of `report.tsx` that covers all five fields. Pass it to `useForm` via `zodResolver`. Validate on submit (`mode: "onSubmit"`).

#### Schema Rules (15 marks, 3 per field)

| Field | Rule | Error Message |
|-------|------|---------------|
| Title | Between 5 and 100 characters (after trim) | `"Title must be between 5 and 100 characters."` |
| Category | Non-empty string (a category must be selected) | `"Please select a category."` |
| Description | At least 20 characters (after trim) | `"Description must be at least 20 characters."` |
| Location | Non-empty, not just whitespace | `"Please enter a location."` |
| Urgency | Non-empty string (a level must be selected) | `"Please select an urgency level."` |

**Hint for Title (min AND max):** Use `.min(5).max(100)` chained together, or use `.refine()` for a custom combined check.

**Hint for selection fields (Category, Urgency):** These are stored as strings. Use `z.string().min(1, "...")` — an empty string `""` fails `.min(1)`, so validation catches the case where the user never tapped a selection.

#### Error Display (10 marks)

- Show an inline error `<Text>` with `theme.colors.error` below each invalid field
- Apply a red border on invalid `TextInput` fields using conditional styling in the `Controller` render prop: `style={[styles.input, errors.title && styles.inputError]}`
- For Category and Urgency, show the error message below the group of items (no border to turn red since they're not TextInputs)

---

### Task 4: Success + Reset (15 marks)

1. **Success Alert (8 marks):** When `handleSubmit` calls your `onSubmit` function (validation passed), show an `Alert.alert` with:
   - Title: `"Issue Reported"`
   - Message: A formatted summary of all five fields using template literals and `\n` for line breaks

2. **Reset + Navigate Back (7 marks):** After the user dismisses the alert, the form should:
   - Reset all fields using RHF's `reset()` function (destructure it from `useForm` alongside `control`, `handleSubmit`, etc.)
   - Navigate back with `router.back()`
   - Use the `Alert.alert` callback (third argument) to trigger reset and navigation after "OK" is tapped:
     ```tsx
     Alert.alert("Issue Reported", summary, [
       {
         text: "OK",
         onPress: () => {
           reset();       // Resets all fields to defaultValues
           router.back();
         },
       },
     ]);
     ```

---

### Task 5: Styling + Polish (15 marks)

1. **Theme Consistency (5 marks)**
   - Use `theme.colors.bg` for the screen background
   - Use `theme.colors.card` for input backgrounds
   - Use `theme.colors.border` for default input borders
   - Use `theme.colors.error` for error text and error borders
   - Use `theme.radius.input` for input and button border radius
   - Use `theme.spacing.screen` for screen padding

2. **Selection Group Styling (5 marks)**
   - Category items clearly show which one is selected
   - Urgency items use their level-specific colors and clearly indicate selection state
   - Both groups have rounded corners and consistent spacing between items

3. **Overall Layout (5 marks)**
   - The form must be wrapped in a `ScrollView` so it is scrollable when the keyboard is open
   - Consistent spacing between label-input pairs
   - Labels styled consistently (font weight, size, color matching the profile form)
   - Submit button clearly separated from the last field with top margin

---

## Submission Requirements

Submit the following files:

1. `app/(tab)/home/_layout.tsx`
2. `app/(tab)/home/index.tsx`
3. `app/(tab)/home/report.tsx`
4. `app/(tab)/_layout.tsx` — only if you made changes to the tab layout

**Confirm** that you have deleted `app/(tab)/home.tsx`. Having both `home.tsx` and `home/index.tsx` will cause a routing conflict.

---

## Rubric

| Task | Criteria | Marks |
|------|----------|-------|
| **Task 1: Navigation Setup** | | **10** |
| | Home folder created with correct `_layout.tsx` Stack navigator | 3 |
| | Home screen content moved to `index.tsx` with correct imports; old `home.tsx` deleted | 3 |
| | Tappable "Report Issue" card navigates to the report screen | 2 |
| | Back button works correctly from the report screen | 2 |
| **Task 2: Form Fields** | | **35** |
| | Title: Controller-wrapped TextInput with placeholder | 7 |
| | Category: Controller-wrapped Pressable selection group with visual highlight | 7 |
| | Description: Controller-wrapped multiline TextInput with correct props and visible height | 7 |
| | Location: Controller-wrapped TextInput with placeholder and autoCapitalize | 7 |
| | Urgency: Controller-wrapped colored selection group with distinct colors per level | 7 |
| **Task 3: Zod Schema + Validation** | | **25** |
| | Title validates min 5 / max 100 characters with trim | 3 |
| | Category validates that a selection has been made | 3 |
| | Description validates min 20 characters with trim | 3 |
| | Location validates non-empty with trim | 3 |
| | Urgency validates that a selection has been made | 3 |
| | Inline error messages appear below each invalid field | 4 |
| | Red border on invalid TextInput fields | 3 |
| **Task 4: Success + Reset** | | **15** |
| | Alert displays with correct title and formatted summary of all fields | 8 |
| | All fields reset via `reset()` and app navigates back on alert dismiss | 7 |
| **Task 5: Styling + Polish** | | **15** |
| | Theme values used consistently (colors, radius, spacing) | 5 |
| | Selection groups have clear selected/unselected states with proper styling | 5 |
| | ScrollView wrapper, consistent spacing, clean label/input layout | 5 |
| | | **Total: 100** |

---

## Hints

1. **Converting Home to a folder:** Same conversion as `settings.tsx` → `settings/` in the Week 8 guide. The `_layout.tsx` for Home will look almost identical to `settings/_layout.tsx` — just different screen names.

2. **Schema-first:** Write the full Zod schema and `useForm` setup before any JSX. This matches the profile form approach and helps you think about the shape of data before thinking about UI.

3. **Selection fields with `Controller`:** These don't have a `TextInput` inside — but `Controller` doesn't care. It gives you `onChange` and `value`. Call `onChange(itemValue)` when the user taps a `Pressable`. Check `value === item` to know which is selected. The Zod rule `z.string().min(1)` catches the case where `value` is still `""` (nothing selected yet).

4. **Multiline TextInput:** Key props are `multiline={true}` and `numberOfLines={4}`. Add `textAlignVertical: "top"` in the **style** (not as a prop) so text starts at the top on Android. Set a `minHeight` in the style so the input looks like a text area.

5. **Urgency colors:** Define a helper object outside the component:
   ```tsx
   const URGENCY_COLORS: Record<string, string> = {
     Low: "#16a34a",
     Medium: "#ca8a04",
     High: "#dc2626",
   };
   ```
   Then use `URGENCY_COLORS[level]` inside your map to get the right color per item.

6. **Resetting with RHF:** Destructure `reset` from `useForm`:
   ```tsx
   const { control, handleSubmit, reset, formState: { errors } } = useForm({ ... });
   ```
   Calling `reset()` with no arguments restores all fields to `defaultValues`.

7. **`handleSubmit` is always the `onPress` handler:**
   ```tsx
   <Pressable onPress={handleSubmit(onSubmit)}>
   ```
   Never pass `onSubmit` directly — that skips validation.

8. **Error messages from the schema:** The string you pass to Zod rules (`z.string().min(1, "Please select a category.")`) is what appears in `errors.category.message`. You don't need to write the message anywhere else.

9. **Don't forget `trim()` on text fields** in your schema: `z.string().trim().min(5)`. A field full of spaces should not pass the length check.

10. **Scrolling:** Wrap your entire form in `<ScrollView>` with `contentContainerStyle` for padding — same as the profile form. Without this, the bottom of the form may be cut off when the keyboard is open.

---

*This lab builds on the React Hook Form + Zod patterns from the Week 8 guide. The approach is the same — schema-first, `Controller` for each field, `handleSubmit` wrapping your submit function. Adapt the patterns, don't copy them.*
