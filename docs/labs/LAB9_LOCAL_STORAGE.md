# Lab 9: Local Storage

## Objective

Build persistence for the Home screen and a new "Favorites" feature, applying everything you learned about AsyncStorage, `useEffect`, loading states, and the storage utility — but with new data shapes and interaction patterns you haven't built before (arrays, toggle-to-save, and filtered lists).

---

## What You Already Have

After completing the Week 9 guide, your app has:

- A **storage utility** (`lib/storage.ts`) with `get`, `set`, `remove` functions and `STORAGE_KEYS`
- A **notifications toggle** that persists across app restarts
- An **Edit Profile form** that saves data to storage and pre-fills on revisit
- Patterns for: `useEffect` on mount, async/await in components, loading states with `ActivityIndicator`, and the `async function inside useEffect` pattern

You will **not** be modifying the settings screens. This lab asks you to build something new.

---

## Scenario

Students want to bookmark their favorite courses so they appear on the Home screen for quick access. Your job is to add a "favorite" toggle to each course in the Courses list and display the favorited courses on the Home screen. Everything must persist — if a student favorites a course and closes the app, the favorites should still be there when they reopen it.

---

## Expected File Changes

When you are done, your project should have these modified files:

```
MODIFIED:  lib/storage.ts                       <-- Add FAVORITES key
MODIFIED:  app/(tab)/courses/index.tsx          <-- Add favorite toggle to each course
MODIFIED:  app/(tab)/home.tsx                    <-- Display favorited courses
```

No new files need to be created. No navigation changes are needed.

---

## Tasks

### Task 1: Add a FAVORITES Storage Key (5 marks)

Update `lib/storage.ts` to support storing an array of favorited course IDs.

1. Add a new key to `STORAGE_KEYS`: `FAVORITES: "favorites"`
2. The value stored under this key will be an array of strings (course IDs), e.g., `["cprg216", "cprg303"]`

That's it for this task — the utility functions (`get`, `set`, `remove`) already work with any data type, including arrays.

---

### Task 2: Add Favorite Toggle to Courses List (40 marks)

Modify `app/(tab)/courses/index.tsx` to let users favorite/unfavorite courses.

#### 2a. Load Favorites on Mount (10 marks)

- Add a `favorites` state variable: `useState<string[]>([])`
- Add an `isLoading` state variable: `useState(true)`
- Use `useEffect` to load saved favorites from storage on mount
- If no favorites exist in storage (first launch), keep the default empty array
- Show an `ActivityIndicator` while loading

#### 2b. Toggle Favorite on Press (15 marks)

Add a favorite icon to each course item in the `FlatList`. When tapped, it toggles the course in/out of the favorites array.

- Add a `Pressable` icon to the right side of each course item (use `Ionicons` with `heart` when favorited and `heart-outline` when not)
- The icon color should be `theme.colors.error` (red) when favorited and `theme.colors.muted` (gray) when not
- When tapped, the handler should:
  1. Check if the course ID is already in `favorites`
  2. If yes: remove it from the array (unfavorite)
  3. If no: add it to the array (favorite)
  4. Update state with the new array
  5. Save the new array to storage

**Important:** When creating the new favorites array, use proper immutable patterns:

```tsx
// Adding to array (immutable)
const updated = [...favorites, courseId];

// Removing from array (immutable)
const updated = favorites.filter((id) => id !== courseId);
```

#### 2c. Visual Feedback (15 marks)

- The heart icon should update **immediately** when tapped (optimistic update — don't wait for storage to finish before updating the UI)
- Each course item should show whether it's favorited without needing to navigate away and back
- The favorites should persist: favorite a course → close app → reopen → heart is still filled

---

### Task 3: Display Favorites on Home Screen (35 marks)

Modify `app/(tab)/home.tsx` to show a "My Favorites" section that displays the user's favorited courses.

#### 3a. Load Favorites on Mount (10 marks)

- Add a `favorites` state variable: `useState<string[]>([])`
- Add an `isLoading` state variable: `useState(true)`
- Use `useEffect` to load saved favorites from storage on mount
- Show an `ActivityIndicator` while loading

#### 3b. Display Favorite Courses (15 marks)

- Add a "My Favorites" section header (`<Text>`) below the existing Home screen content
- Filter the `COURSES` array (you'll need to import it or define it — use the same course data as `courses/index.tsx`) to only include courses whose IDs are in the `favorites` array
- Display each favorited course as an `AppCard` showing the course code and name
- Each favorited course card should be tappable — pressing it navigates to `/(tab)/courses/${id}` (cross-tab navigation)
- If there are no favorites, show a message like "No favorites yet. Go to Courses to add some!"

#### 3c. Keep Favorites in Sync (10 marks)

There's a subtle problem: if the user favorites a course on the Courses tab and then switches to the Home tab, the Home screen won't show the new favorite because `useEffect` with `[]` only runs on mount — not on tab switch.

Fix this by using `useFocusEffect` from `expo-router` instead of `useEffect`. This hook runs every time the screen comes into focus (including tab switches):

```tsx
import { useFocusEffect } from "expo-router";
import { useCallback } from "react";

useFocusEffect(
  useCallback(() => {
    async function loadFavorites() {
      const saved = await storage.get<string[]>(STORAGE_KEYS.FAVORITES);
      if (saved !== null) {
        setFavorites(saved);
      }
      setIsLoading(false);
    }
    loadFavorites();
  }, [])
);
```

**Note:** `useFocusEffect` requires wrapping the callback in `useCallback` — this is a React optimization that prevents the effect from being recreated on every render. The `[]` at the end of `useCallback` serves the same purpose as it does in `useEffect`.

---

### Task 4: Styling + Polish (20 marks)

Make everything look polished and consistent with the rest of the app.

#### Courses List Styling (10 marks)

- Heart icons should be properly sized (22-24px) and aligned to the right of each course item
- The tap target for the heart should be large enough to tap comfortably (at least 40x40 area — use padding on the `Pressable`)
- There should be no layout shift when toggling a favorite (the icon changes appearance but stays in the same position and size)
- Theme values used consistently (`theme.colors`, `theme.spacing`, `theme.radius`)

#### Home Screen Styling (10 marks)

- "My Favorites" section header styled consistently with the existing "Home" header
- Favorite course cards use `AppCard` and look consistent with the rest of the app
- Empty state message is styled with `theme.colors.muted` and centered or clearly visible
- Overall layout uses proper spacing (`theme.spacing.screen`, `theme.spacing.gap`)
- Loading spinner uses `theme.colors.primary`

---

## Submission Requirements

Submit the following files:

1. `lib/storage.ts` — Updated with `FAVORITES` key
2. `app/(tab)/courses/index.tsx` — Courses list with favorite toggle
3. `app/(tab)/home.tsx` — Home screen with favorites section

---

## Rubric

| Task | Criteria | Marks |
|------|----------|-------|
| **Task 1: Storage Key** | | **5** |
| | `FAVORITES` key added to `STORAGE_KEYS` | 5 |
| **Task 2: Favorite Toggle** | | **40** |
| | Favorites load from storage on mount with loading state | 10 |
| | Heart icon toggles between filled/outline with correct colors | 5 |
| | Tapping adds/removes course ID from favorites array | 5 |
| | Updated favorites saved to storage after every toggle | 5 |
| | Immutable array operations used (spread/filter, not push/splice) | 5 |
| | Favorites persist across app restarts | 5 |
| | Icon updates immediately on tap (optimistic update) | 5 |
| **Task 3: Home Favorites** | | **35** |
| | Favorites load from storage on mount with loading state | 10 |
| | Favorited courses displayed as tappable cards | 5 |
| | Cards navigate to correct course detail screen | 5 |
| | Empty state message shown when no favorites exist | 5 |
| | `useFocusEffect` used so favorites update when switching tabs | 10 |
| **Task 4: Styling + Polish** | | **20** |
| | Heart icons properly sized, aligned, with comfortable tap targets | 5 |
| | No layout shift when toggling favorites | 5 |
| | Home favorites section styled consistently with the app | 5 |
| | Theme values used consistently throughout | 5 |
| | | **Total: 100** |

---

## Hints

These should point you in the right direction without giving away the solution.

1. **Array state:** Unlike the boolean (notifications) or object (profile) you persisted in the guide, favorites is an **array**. The storage utility handles this automatically — `storage.set(STORAGE_KEYS.FAVORITES, ["cprg216", "cprg303"])` works because `JSON.stringify` handles arrays. When you read it back with `storage.get<string[]>(...)`, you get the array.

2. **Checking if a course is favorited:** Use `favorites.includes(courseId)` to check if a course ID is in the array. This returns `true` or `false`, which you can use to pick the icon name and color:
   ```tsx
   const isFav = favorites.includes(course.id);
   // icon: isFav ? "heart" : "heart-outline"
   // color: isFav ? theme.colors.error : theme.colors.muted
   ```

3. **Toggling a favorite:** The toggle handler needs to do different things depending on whether the course is already favorited:
   ```tsx
   async function toggleFavorite(courseId: string) {
     const isFav = favorites.includes(courseId);
     const updated = isFav
       ? favorites.filter((id) => id !== courseId)  // remove
       : [...favorites, courseId];                   // add
     setFavorites(updated);
     await storage.set(STORAGE_KEYS.FAVORITES, updated);
   }
   ```

4. **Filtering courses on Home:** If you have the `COURSES` array and a `favorites` array of IDs, you can get the favorited courses with:
   ```tsx
   const favoriteCourses = COURSES.filter((c) => favorites.includes(c.id));
   ```

5. **Cross-tab navigation:** You can navigate to a screen in a different tab using the full path. From the Home tab, `router.push("/(tab)/courses/cprg216")` will switch to the Courses tab and push the detail screen.

6. **The COURSES array:** You'll need access to the same course data in both `courses/index.tsx` and `home.tsx`. You could duplicate the array, or (better) extract it to a shared file like `lib/courses.ts` and import from both. Either approach is acceptable for this lab.

7. **`useFocusEffect` vs `useEffect`:** The key difference is when they run. `useEffect(() => {...}, [])` runs once when the component mounts. `useFocusEffect(useCallback(() => {...}, []))` runs every time the screen comes into focus — including the first mount AND every time you switch back to that tab. This is exactly what we need for the Home screen to pick up new favorites.

8. **Optimistic update:** "Optimistic" means updating the UI immediately without waiting for the async operation to finish. In the toggle handler, `setFavorites(updated)` happens synchronously (instant), then `await storage.set(...)` saves to disk (slightly slower). The user sees the change immediately, and storage catches up in the background.

9. **FlatList with favorite icons:** If your courses list uses `FlatList`, you'll need to update the `renderItem` function to include the heart icon. Wrap the icon in its own `Pressable` so tapping the heart doesn't trigger the course navigation. You may need to adjust the item layout to accommodate the icon (e.g., `flexDirection: "row"` with `justifyContent: "space-between"`).

10. **Loading state on Home:** Even though the Home screen might load almost instantly, always include the loading state. It prevents a flash of "No favorites yet" before the real favorites load from storage. This is the same principle from the guide — prevent the UI from showing incorrect content, even briefly.

---

*This lab builds on the storage patterns from the Week 9 guide. If you get stuck on the storage utility, `useEffect`, or loading states, review `WEEK9_LOCAL_STORAGE.md`. The new concept here is working with arrays in storage and using `useFocusEffect` — everything else is the same pattern applied to new data.*
