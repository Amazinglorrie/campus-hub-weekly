# Lab 8: Forms + Validation

## Objective

Build a "Report Issue" form on a new screen inside the Home tab, applying everything you learned about controlled inputs, validation, error handling, and conditional styling -- but with new field types you haven't built before (multiline text, selection groups, and colored indicators).

---

## What You Already Have

After completing the Week 8 guide, your app has:

- A **Settings** tab with a nested Stack (`settings/_layout.tsx` -> `index.tsx` -> `profile.tsx`)
- An **Edit Profile** form with 5 validated fields (First Name, Last Name, Email, Student ID, Phone)
- Patterns for: controlled inputs, `useState`, validation on submit, inline error messages, conditional styling (`inputError`), and a disabled submit button
- A centralized `theme.ts` with colors (`bg`, `card`, `text`, `muted`, `primary`, `border`, `error`) and radius values (`card`, `input`)
- A reusable `AppCard` component

You will **not** be modifying the profile form. This lab asks you to build something new.

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
3. **Add a tappable card** to the Home screen that navigates to the report form. Wrap an `AppCard` in a `Pressable` that calls `router.push("/(tab)/home/report")`. Use the title "Report Issue", a subtitle like "Report a campus problem", and a `chevron-forward` icon on the right (the same pattern used in the Settings screen).
4. Verify that tapping the card pushes to a blank `report.tsx` screen with a working back button.

---

### Task 2: Build the Report Issue Form (35 marks)

Create the form in `app/(tab)/home/report.tsx` with the following five fields. Each field has specific requirements that differ from the profile form -- you cannot copy-paste.

#### Field 1: Title (7 marks)

- Standard `TextInput` (single line)
- Placeholder: `"e.g. Projector not working in N210"`
- Controlled input with its own `useState`
- Will be validated in Task 3

#### Field 2: Category (7 marks)

- **Not a TextInput.** This is a selection group.
- Define a constant array outside the component:
  ```
  const CATEGORIES = ["Facilities", "IT/Equipment", "Safety", "Other"];
  ```
- Render each category as a `Pressable` item that the user taps to select
- Use `useState<string | null>(null)` to track which category is selected
- The selected category should be visually highlighted (e.g., `theme.colors.primary` background with white text; unselected items use `theme.colors.card` background with `theme.colors.text`)
- Arrange the items in a horizontal row using `flexDirection: "row"` and `flexWrap: "wrap"` with appropriate gap/margin

#### Field 3: Description (7 marks)

- **Multiline `TextInput`** -- this is a new pattern you have not used before
- Use the `multiline` and `numberOfLines` props: `multiline={true}` and `numberOfLines={4}`
- Add `textAlignVertical: "top"` to the style so text starts at the top of the box (Android behavior)
- The input should be visibly taller than a standard single-line input (set a `minHeight` of around 100)
- Placeholder: `"Describe the issue in detail..."`
- Controlled input with its own `useState`

#### Field 4: Location (7 marks)

- Standard `TextInput` (single line)
- Placeholder: `"e.g. Building N, Room 210"`
- `autoCapitalize="words"` (building names should be capitalized)
- Controlled input with its own `useState`

#### Field 5: Urgency (7 marks)

- **Not a TextInput.** This is a colored selection group.
- Define a constant array outside the component:
  ```
  const URGENCY_LEVELS = ["Low", "Medium", "High"];
  ```
- Render each level as a `Pressable` item
- Use `useState<string | null>(null)` to track which level is selected
- Each urgency level should have a **distinct color** even when unselected, so the user can see at a glance what each option means:
  - Low: green tones (e.g., `#16a34a` background or border)
  - Medium: yellow/amber tones (e.g., `#ca8a04` background or border)
  - High: red tones (e.g., `#dc2626` or `theme.colors.error` background or border)
- The selected level should look noticeably different from the unselected levels (e.g., solid filled background when selected, just a colored border when unselected)
- Arrange the items in a horizontal row

---

### Task 3: Validation + Error Handling (25 marks)

Implement validation that runs when the user presses Submit. Follow the same validate-on-submit pattern from the profile form, but with rules specific to this form.

#### Validation Rules (15 marks, 3 per field)

| Field | Rule | Error Message |
|-------|------|---------------|
| Title | Required, minimum 5 characters, maximum 100 characters | `"Title must be between 5 and 100 characters."` |
| Category | Required, must have a selection | `"Please select a category."` |
| Description | Required, minimum 20 characters | `"Description must be at least 20 characters."` |
| Location | Required, cannot be empty or whitespace only | `"Please enter a location."` |
| Urgency | Required, must have a selection | `"Please select an urgency level."` |

- Use `trim()` on text fields before validating (just like the profile form does)
- For Title, check both the minimum and maximum length after trimming

#### Error Display (10 marks)

- Show an inline error message (`<Text>` with `theme.colors.error`) below each invalid field
- Apply a red border (`theme.colors.error`) to invalid TextInput fields using conditional styling: `style={[styles.input, errors.title && styles.inputError]}`
- For the Category and Urgency selection groups, show the error message below the group of items (since there is no TextInput border to turn red)
- The Submit button should be **disabled** (both visually and functionally) until all five fields have a value. For text fields, check `.length > 0`. For selection fields, check that the value is not `null`.

---

### Task 4: Success + Reset (15 marks)

Handle what happens after a successful submission.

1. **Success Alert (8 marks):** When all validation passes, show an `Alert.alert` with:
   - Title: `"Issue Reported"`
   - Message: A summary that includes all five field values, formatted clearly. For example:
     ```
     Title: Projector not working in N210
     Category: IT/Equipment
     Description: The ceiling projector in room N210 has not been turning on since Monday...
     Location: Building N, Room 210
     Urgency: High
     ```
   - Use template literals and `\n` for line breaks (same pattern as the profile form alert)

2. **Reset + Navigate Back (7 marks):** After the user dismisses the alert, the form should:
   - Clear all five fields back to their initial values (empty strings for text fields, `null` for selection fields)
   - Navigate back to the Home screen using `router.back()`
   - Use the `Alert.alert` callback (the third argument) to run the reset and navigation after the user presses "OK":
     ```tsx
     Alert.alert("Issue Reported", summary, [
       {
         text: "OK",
         onPress: () => {
           // Reset all state here
           // router.back()
         },
       },
     ]);
     ```

---

### Task 5: Styling + Polish (15 marks)

Make the form look polished, professional, and consistent with the rest of the app.

1. **Theme Consistency (5 marks)**
   - Use `theme.colors.bg` for the screen background
   - Use `theme.colors.card` for input backgrounds
   - Use `theme.colors.border` for default input borders
   - Use `theme.colors.error` for error text and error borders
   - Use `theme.radius.input` for input and button border radius
   - Use `theme.spacing.screen` for screen padding

2. **Selection Group Styling (5 marks)**
   - Category items should clearly show which one is selected (distinct background/text color change)
   - Urgency items should use their level-specific colors and clearly indicate selection state
   - Both groups should have rounded corners and consistent spacing between items

3. **Overall Layout (5 marks)**
   - The form must be wrapped in a `ScrollView` so it is scrollable when the keyboard is open or on smaller screens
   - Use consistent spacing between label-input pairs (matching the profile form's spacing)
   - Labels should be styled consistently (font weight, size, color matching the profile form)
   - The Submit button should sit at the bottom with some top margin, clearly separated from the last field

---

## Submission Requirements

Submit the following files:

1. `app/(tab)/home/_layout.tsx` -- Stack navigator for the Home tab
2. `app/(tab)/home/index.tsx` -- Updated Home screen with the Report Issue card
3. `app/(tab)/home/report.tsx` -- The complete Report Issue form
4. `app/(tab)/_layout.tsx` -- Only if you made changes to the tab layout

**Confirm** that you have deleted `app/(tab)/home.tsx` (the old single file). Having both `home.tsx` and `home/index.tsx` will cause a routing conflict.

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
| | Title: controlled TextInput with placeholder | 7 |
| | Category: Pressable selection group with visual highlight on selection | 7 |
| | Description: multiline TextInput with correct props and visible height | 7 |
| | Location: controlled TextInput with placeholder and autoCapitalize | 7 |
| | Urgency: colored Pressable selection group with distinct colors per level | 7 |
| **Task 3: Validation + Errors** | | **25** |
| | Title validates min 5 / max 100 characters with trim | 3 |
| | Category validates that a selection has been made | 3 |
| | Description validates min 20 characters with trim | 3 |
| | Location validates non-empty with trim | 3 |
| | Urgency validates that a selection has been made | 3 |
| | Inline error messages appear below each invalid field | 4 |
| | Red border on invalid TextInput fields | 3 |
| | Submit button disabled until all fields have values | 3 |
| **Task 4: Success + Reset** | | **15** |
| | Alert displays with correct title and formatted summary of all fields | 8 |
| | All fields reset to initial values and app navigates back on alert dismiss | 7 |
| **Task 5: Styling + Polish** | | **15** |
| | Theme values used consistently (colors, radius, spacing) | 5 |
| | Selection groups have clear selected/unselected states with proper styling | 5 |
| | ScrollView wrapper, consistent spacing, clean label/input layout | 5 |
| | | **Total: 100** |

---

## Hints

These should point you in the right direction without giving away the solution.

1. **Converting Home to a folder:** You have done this exact conversion before. Look at how `settings.tsx` became `settings/_layout.tsx` + `settings/index.tsx` in the Week 8 guide. The `_layout.tsx` for Home will look almost identical to the one in `settings/` -- just with different screen names.

2. **Selection group state:** For Category and Urgency, you need to track *which item is selected*, not text. Use `useState<string | null>(null)` where `null` means "nothing selected." When the user taps an item, set the state to that item's value (e.g., `setCategory("Facilities")`). To check if an item is the selected one, compare: `category === "Facilities"`.

3. **Rendering the selection items:** Use `.map()` on your constant array to render each item as a `Pressable`. Inside the map, use a conditional style to change the appearance based on whether that item is the currently selected value. Something like:
   ```tsx
   style={[styles.optionItem, selectedValue === item && styles.optionItemSelected]}
   ```

4. **Multiline TextInput:** The key props are `multiline={true}` and `numberOfLines={4}`. Add `textAlignVertical: "top"` in the **style** (not as a prop) so text starts at the top on Android. Set a `minHeight` in the style so the input looks like a text area, not a single-line input.

5. **Urgency colors:** Define a helper object or use inline conditionals to map each urgency level to its color. For example:
   ```tsx
   const URGENCY_COLORS: Record<string, string> = {
     Low: "#16a34a",
     Medium: "#ca8a04",
     High: "#dc2626",
   };
   ```
   Then use `URGENCY_COLORS[level]` to get the right color for each item.

6. **The isFormFilled check:** You have five fields but two different types. Text fields check `.length > 0` (or `.trim().length > 0`), and selection fields check `!== null`. Chain them all with `&&`:
   ```tsx
   const isFormFilled =
     title.length > 0 &&
     category !== null &&
     description.length > 0 &&
     location.length > 0 &&
     urgency !== null;
   ```

7. **Alert callback for reset:** `Alert.alert` accepts a third argument -- an array of button objects. Each button can have an `onPress` callback. Use this to reset your state variables and call `router.back()` *after* the user taps "OK."

8. **Error type:** Define a `FormErrors` type with optional string properties for each field, just like the profile form does. For example: `title?: string; category?: string;` and so on.

9. **Do not forget `trim()`** on text fields in your validation function. A field full of spaces should not pass validation.

10. **Scrolling:** Wrap your entire form JSX in a `<ScrollView>` with `contentContainerStyle` for padding, exactly like the profile form does. Without this, the bottom of the form may be cut off on smaller screens or when the keyboard is open.

---

*This lab builds on the forms and validation patterns from the Week 8 guide. If you get stuck, review `WEEK8_FORMS.md` for the patterns -- but remember that this form has different field types, so you will need to adapt, not copy.*
