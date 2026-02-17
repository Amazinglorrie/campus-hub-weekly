# Lab 7: Navigation

## Objective

Apply the routing concepts from this week's guide by adding new screens and navigation flows to the Campus Hub app, reinforcing your understanding of Stack navigation, nested navigators, dynamic routes, and deep linking.

---

## Starter Code

You should already have the Campus Hub app running with the following structure from the Week 7 guide:

```
app/
├── _layout.tsx                 ← Root Stack Navigator
├── index.tsx                   ← Redirects to /(tab)/home
└── (tab)/
    ├── _layout.tsx             ← Tab Navigator (Home, Courses, Settings)
    ├── home.tsx                ← Home screen (static, no nested navigator)
    ├── courses/
    │   ├── _layout.tsx         ← Stack Navigator (list → detail)
    │   ├── index.tsx           ← Course list screen
    │   └── [id].tsx            ← Course detail screen (dynamic route)
    └── settings/
        ├── _layout.tsx         ← Stack Navigator (index → profile)
        ├── index.tsx           ← Settings screen
        └── profile.tsx         ← Edit Profile screen

components/
└── AppCard.tsx                 ← Reusable card component

styles/
└── theme.ts                   ← Centralized design tokens
```

Make sure your app builds and runs before starting this lab. If any of the above is missing, revisit the routing guide first.

---

## Tasks

### Task 1: Convert the Home Tab to a Nested Stack Navigator (35 marks)

Right now, `home.tsx` is a single file sitting directly inside `(tab)/`. It has no nested navigator, so there is nowhere to push a new screen. The Courses and Settings tabs already use the folder-with-`_layout.tsx` pattern. Your job is to apply that same pattern to the Home tab.

**What to build:**

- An "About Campus Hub" screen that users reach by tapping a card on the Home screen.
- The About screen should display:
  - App name: **Campus Hub**
  - Version: **1.0.0**
  - A short paragraph describing the app (write your own -- one or two sentences is fine)

**Expected file changes:**

| Action | File |
|--------|------|
| **Delete** | `app/(tab)/home.tsx` |
| **Create** | `app/(tab)/home/_layout.tsx` |
| **Create** | `app/(tab)/home/index.tsx` |
| **Create** | `app/(tab)/home/about.tsx` |

**Steps:**

1. Delete the existing `app/(tab)/home.tsx` file. You cannot have both `home.tsx` and a `home/` folder -- Expo Router will not know which one to use.

2. Create the folder `app/(tab)/home/`.

3. Inside that folder, create `_layout.tsx`. This is the nested Stack navigator for the Home tab. It should define two screens: `index` and `about`. Set the title of the index screen to `"Home"` and the about screen to `"About"`.

4. Create `index.tsx` inside the home folder. Move the content from the old `home.tsx` into this file. Then add a third `AppCard` wrapped in a `Pressable` that navigates to the About screen when tapped:
   - Title: `"About Campus Hub"`
   - Subtitle: `"Version, credits, and more"`
   - Right side: a chevron-forward icon (same pattern as the Courses list and Settings screen)
   - The `onPress` should call `router.push("/(tab)/home/about")`

5. Create `about.tsx` inside the home folder. This is a simple screen with:
   - A heading: `"About Campus Hub"`
   - The version number displayed in the same `code` style used on the Course Details screen
   - A short description paragraph

6. Update `app/(tab)/_layout.tsx` -- the tab navigator. The `name` for the Home tab entry must change from `"home"` to `"home"` (it stays the same string because Expo Router resolves `home` to the `home/` folder automatically). No change should actually be needed here, but verify your tab still works.

**Acceptance criteria:**
- The Home tab still appears in the tab bar and loads the Home dashboard as before.
- A new "About Campus Hub" card appears on the Home screen below the existing two cards.
- Tapping the card pushes the About screen with a back button in the header.
- Pressing back returns to the Home dashboard.
- The tab bar remains visible on both the Home dashboard and the About screen.

---

### Task 2: Add Instructor Info to Course Details (40 marks)

The Course Details screen (`[id].tsx`) currently only shows the course ID. In a real app, this screen should show meaningful information. Your job is to expand it with instructor data and add a navigation action.

**What to build:**

- A data structure that maps each course ID to its details (name, subtitle, instructor name, instructor office, and instructor email).
- A redesigned Course Details screen that shows the course name, course code, instructor name, and instructor office.
- A "Contact Instructor" card that, when tapped, pushes a new screen showing the instructor's full contact details.

**Expected file changes:**

| Action | File |
|--------|------|
| **Create** | `app/(tab)/courses/instructor.tsx` |
| **Modify** | `app/(tab)/courses/[id].tsx` |
| **Modify** | `app/(tab)/courses/_layout.tsx` |

**Steps:**

1. In `app/(tab)/courses/[id].tsx`, add a data lookup object above the component (or in the same file). Here is a starter dataset you must use:

```tsx
const COURSE_DATA: Record<string, {
  title: string;
  subtitle: string;
  instructor: string;
  office: string;
  email: string;
}> = {
  cprg216: {
    title: "CPRG-216",
    subtitle: "Advanced Web Systems",
    instructor: "Dr. Sarah Chen",
    office: "Room 312, Building B",
    email: "s.chen@college.ca",
  },
  cprg303: {
    title: "CPRG-303",
    subtitle: "Mobile Development",
    instructor: "Prof. Marcus Johnson",
    office: "Room 108, Building A",
    email: "m.johnson@college.ca",
  },
  cprg306: {
    title: "CPRG-306",
    subtitle: "Backend APIs",
    instructor: "Dr. Emily Park",
    office: "Room 415, Building C",
    email: "e.park@college.ca",
  },
};
```

2. Update the Course Details screen to look up the course using the `id` param. If the `id` does not match any entry, display a "Course not found" message instead of crashing.

3. When a valid course is found, display:
   - The course title (e.g., "CPRG-303") as the heading
   - The subtitle (e.g., "Mobile Development")
   - An `AppCard` showing the instructor name and office
   - A "Contact Instructor" `AppCard` wrapped in a `Pressable` with a chevron-forward icon. When tapped, it should navigate to the instructor screen, passing the course `id` as a query parameter: `router.push({ pathname: "/(tab)/courses/instructor", params: { courseId: id } })`

4. Create `app/(tab)/courses/instructor.tsx`. This screen receives a `courseId` query parameter via `useLocalSearchParams()`. Use it to look up the same `COURSE_DATA` object. Display:
   - Instructor name as the heading
   - Office location
   - Email address
   - A "Send Email" button (use `Pressable` styled like a button). When tapped, show an `Alert` with the message: `"Email drafted to [email address]"`. (We are not sending a real email -- just confirming the action.)

5. Register the new screen in `app/(tab)/courses/_layout.tsx` by adding a `Stack.Screen` entry for `"instructor"` with the title `"Instructor"`.

**Important:** To share `COURSE_DATA` between `[id].tsx` and `instructor.tsx`, you have two options. Either copy the object into both files (simpler but repetitive), or create a shared data file like `data/courses.ts` and import from it. Both approaches are acceptable for this lab. If you choose the shared file approach, document it in your submission.

**Acceptance criteria:**
- Navigating to any course shows the course title, subtitle, instructor name, and office.
- Navigating to an invalid course ID (e.g., typing a random URL) shows a "Course not found" message instead of a crash.
- Tapping "Contact Instructor" pushes the instructor screen with correct details.
- The instructor screen shows name, office, and email.
- Tapping "Send Email" shows an Alert.
- Pressing back from the instructor screen returns to the course detail. Pressing back again returns to the course list.
- The full navigation chain works: Course List -> Course Detail -> Instructor -> back -> back -> Course List.

---

### Task 3: Deep Linking Verification (25 marks)

Deep linking means navigating directly to a specific screen using a URL, without tapping through the app. Expo Router supports this automatically because routes are file-based. Your job is to test this and document your findings.

**What to do:**

1. With the app running in Expo Go or a dev build, open the following URLs one at a time using the method described below. For each URL, note whether it works and what screen appears.

   **How to test:** In your terminal, with the Expo dev server running, use the Expo CLI command:
   ```
   npx uri-scheme open exp://127.0.0.1:8081/--/(tab)/home --android
   ```
   Or, if you are running on the web, simply type the path into the browser address bar (e.g., `http://localhost:8081/(tab)/courses/cprg303`).

   Alternatively, you can use the `Link` component from `expo-router` to create a quick test. Add a temporary link somewhere in the app:
   ```tsx
   import { Link } from "expo-router";
   // ...
   <Link href="/(tab)/courses/cprg303">Go to CPRG-303</Link>
   ```

2. **URLs to test** (test all six):

| # | URL Path | Expected Screen |
|---|----------|-----------------|
| 1 | `/(tab)/home` | Home dashboard |
| 2 | `/(tab)/home/about` | About Campus Hub |
| 3 | `/(tab)/courses` | Course list |
| 4 | `/(tab)/courses/cprg303` | CPRG-303 detail |
| 5 | `/(tab)/courses/invalidxyz` | "Course not found" message |
| 6 | `/(tab)/settings` | Settings screen |

3. **Deliverable:** Create a file called `DEEP_LINK_RESULTS.md` in the root of your project. For each of the 6 URLs, document:
   - The URL you tested
   - Whether it loaded the correct screen (Yes / No)
   - A one-sentence note on what you observed (e.g., "Loaded the About screen with back button to Home")
   - If a URL did not work, explain what happened and what you think the issue is

   Use this template:

```markdown
# Deep Link Test Results

**Student Name:** [Your Name]
**Date:** [Date]

| # | URL Path | Correct Screen? | Notes |
|---|----------|-----------------|-------|
| 1 | `/(tab)/home` | | |
| 2 | `/(tab)/home/about` | | |
| 3 | `/(tab)/courses` | | |
| 4 | `/(tab)/courses/cprg303` | | |
| 5 | `/(tab)/courses/invalidxyz` | | |
| 6 | `/(tab)/settings` | | |
```

4. **Reflection question** (answer in the same file, below the table):

   > In your own words, explain why Expo Router can handle deep links automatically without any extra configuration. What is it about file-based routing that makes this possible? (3-4 sentences minimum.)

**Acceptance criteria:**
- `DEEP_LINK_RESULTS.md` exists in the project root.
- All 6 URLs are tested and documented in the table.
- Each row has a Yes/No answer and a descriptive note.
- The reflection question is answered thoughtfully with at least 3 sentences.

---

## Submission Requirements

Submit the following:

1. **Your complete project folder** (zipped), excluding `node_modules/`. Make sure the project runs with `npx expo start` without errors.

2. **`DEEP_LINK_RESULTS.md`** should be in the project root (it will be included in the zip).

3. **Screenshots** (4 total, included in the zip or pasted into a separate document):
   - Screenshot 1: Home screen showing the new "About Campus Hub" card
   - Screenshot 2: The About screen
   - Screenshot 3: A Course Detail screen showing instructor info and the "Contact Instructor" card
   - Screenshot 4: The Instructor screen showing contact details and the "Send Email" button

**File naming:** `Lab7_[YourLastName]_[YourFirstName].zip`

---

## Rubric

| Criteria | Marks | Details |
|----------|-------|---------|
| **Task 1: Home nested Stack setup** | 15 | `home/` folder created correctly with `_layout.tsx`, `index.tsx`, and `about.tsx`. Old `home.tsx` removed. Stack navigator configured with proper screen names. |
| **Task 1: About screen and navigation** | 12 | "About Campus Hub" card on Home screen navigates to About screen. About screen shows app name, version, and description. Back navigation works. |
| **Task 1: Home tab still works** | 8 | Home tab icon and label still work in the tab bar. Existing cards (Upcoming Deadline, Attendance) still display. Tab bar visible on both Home and About screens. |
| **Task 2: Course detail redesign** | 12 | `[id].tsx` updated with `COURSE_DATA` lookup. Displays course title, subtitle, instructor name, and office. Handles invalid course IDs without crashing. |
| **Task 2: Instructor screen** | 15 | `instructor.tsx` created and registered in `_layout.tsx`. Receives `courseId` param and looks up correct data. Shows instructor name, office, and email. "Send Email" button triggers an Alert. |
| **Task 2: Navigation chain** | 13 | Full chain works: list -> detail -> instructor -> back -> back -> list. No navigation dead ends. Correct data displays on each screen. |
| **Task 3: Deep link testing** | 15 | `DEEP_LINK_RESULTS.md` present. All 6 URLs tested. Each row has a clear Yes/No and a descriptive note. |
| **Task 3: Reflection question** | 10 | Thoughtful explanation of why file-based routing enables automatic deep linking. At least 3 sentences. Demonstrates understanding, not just restating the guide. |
| **Total** | **100** | |

---

## Tips

- **The pattern is the same every time.** Converting `home.tsx` into `home/_layout.tsx` + `home/index.tsx` is the exact same pattern you already see in `courses/` and `settings/`. Study those folders before you start.
- **Test as you go.** Do not write all the code and then run it for the first time. Add one file, make sure it works, then move on.
- **Read the error messages.** If Expo Router throws an error about duplicate routes or missing layouts, it is telling you exactly what is wrong. Read it carefully.
- **Use the existing code as a reference.** The Settings tab already demonstrates pushing from a list to a detail screen with `router.push()`. The Courses tab demonstrates dynamic routes with `useLocalSearchParams()`. You do not need to invent new patterns -- combine what already exists.
- **Ask if you are stuck**, but try for at least 15 minutes first. Most issues come from a file being in the wrong folder or a `_layout.tsx` not registering a screen.
