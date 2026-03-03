from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# ── Colour palette ──────────────────────────────────────────────────────────────
BLUE       = RGBColor(0x25, 0x63, 0xEB)   # primary
DARK       = RGBColor(0x11, 0x18, 0x27)   # text
MUTED      = RGBColor(0x6B, 0x72, 0x80)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
BG         = RGBColor(0xF8, 0xFA, 0xFC)
ERROR      = RGBColor(0xDC, 0x26, 0x26)
CARD       = RGBColor(0xFF, 0xFF, 0xFF)
BORDER     = RGBColor(0xE5, 0xE7, 0xEB)
GREEN      = RGBColor(0x16, 0xA3, 0x4A)
CODE_BG    = RGBColor(0x1E, 0x29, 0x3B)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]   # completely blank

# ── Helpers ──────────────────────────────────────────────────────────────────────
def bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def box(slide, l, t, w, h, text, font_size=18, bold=False, color=DARK,
        align=PP_ALIGN.LEFT, bg_color=None, wrap=True, italic=False):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    if bg_color:
        txBox.fill.solid()
        txBox.fill.fore_color.rgb = bg_color
    return txBox

def rect(slide, l, t, w, h, fill_color, radius=False):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def accent_bar(slide, color=BLUE):
    rect(slide, 0, 0, 0.07, 7.5, color)

def code_block(slide, l, t, w, h, code_text, font_size=11):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = CODE_BG
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    run = p.add_run()
    run.text = code_text
    run.font.size = Pt(font_size)
    run.font.color.rgb = WHITE
    run.font.name = "Courier New"

def pill(slide, l, t, w, h, text, bg_color=BLUE, text_color=WHITE, font_size=11):
    r = rect(slide, l, t, w, h, bg_color)
    box(slide, l + 0.05, t + 0.02, w - 0.1, h, text,
        font_size=font_size, bold=True, color=text_color, align=PP_ALIGN.CENTER)

def section_header(slide, title, subtitle=""):
    bg(slide, BLUE)
    box(slide, 1, 2.5, 11, 1.2, title,
        font_size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    if subtitle:
        box(slide, 1, 3.8, 11, 0.7, subtitle,
            font_size=20, color=RGBColor(0xBF, 0xDB, 0xFF), align=PP_ALIGN.CENTER)

def slide_title(slide, title, subtitle=""):
    accent_bar(slide)
    box(slide, 0.4, 0.25, 12.5, 0.7, title,
        font_size=28, bold=True, color=DARK)
    if subtitle:
        box(slide, 0.4, 0.95, 12.5, 0.4, subtitle,
            font_size=14, color=MUTED, italic=True)
    rect(slide, 0.4, 0.88, 12.5, 0.04, BLUE)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Title
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, DARK)
rect(s, 0, 0, 13.33, 0.6, BLUE)
rect(s, 0, 6.9, 13.33, 0.6, BLUE)

box(s, 0.8, 1.2, 11, 0.7, "WEEK 8",
    font_size=16, bold=True, color=BLUE, align=PP_ALIGN.LEFT)
box(s, 0.8, 1.9, 11, 1.4, "Forms + Validation",
    font_size=52, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
box(s, 0.8, 3.4, 11, 0.6,
    "React Hook Form  ·  Zod  ·  React Native",
    font_size=20, color=RGBColor(0xBF, 0xDB, 0xFF), align=PP_ALIGN.LEFT)

box(s, 0.8, 5.5, 11, 0.4, "Campus Hub — SAIT  |  Winter 2026",
    font_size=13, color=MUTED, align=PP_ALIGN.LEFT)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "What We're Covering", "Two sessions · 4 hours total")

items = [
    ("01", "Why a form library?",         "The problem with plain useState"),
    ("02", "The library stack",            "React Hook Form + Zod + resolvers"),
    ("03", "Zod schemas",                  "Define rules once, validate anywhere"),
    ("04", "useForm hook",                 "control · handleSubmit · errors"),
    ("05", "Controller",                   "Connecting RHF to React Native inputs"),
    ("06", "Error display",                "Conditional styles + inline messages"),
    ("07", "Navigation update",            "settings/ folder with nested Stack"),
]

for i, (num, title, sub) in enumerate(items):
    row = 1.35 + i * 0.72
    rect(s, 0.4, row, 0.55, 0.52, BLUE)
    box(s, 0.4, row, 0.55, 0.52, num,
        font_size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    box(s, 1.1, row, 7, 0.3, title, font_size=14, bold=True, color=DARK)
    box(s, 1.1, row + 0.28, 7, 0.25, sub, font_size=11, color=MUTED)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Section: The Problem
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "The Problem", "Why not just use useState?")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — useState approach pain points
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "The useState Approach — What Goes Wrong")

code_block(s, 0.4, 1.2, 5.8, 5.5,
"""// A separate useState for EVERY field
const [firstName, setFirstName] = useState("")
const [lastName,  setLastName]  = useState("")
const [email,     setEmail]     = useState("")
const [studentId, setStudentId] = useState("")
const [phone,     setPhone]     = useState("")

// A separate errors object
const [errors, setErrors] = useState({})

// A hand-written validate() function
function validate() {
  const newErrors = {}
  if (firstName.trim().length < 2) {
    newErrors.firstName = "Min 2 chars"
  }
  // ... repeated for every field
  setErrors(newErrors)
  return Object.keys(newErrors).length === 0
}""", font_size=10)

problems = [
    "5 fields = 5 useState hooks",
    "Validation logic lives inside the component",
    "Error type defined separately from the rules",
    "Every new field = more boilerplate",
    "No TypeScript safety on form values",
]
box(s, 6.5, 1.2, 0.4, 0.4, "⚠", font_size=22, color=ERROR)
box(s, 6.9, 1.15, 5.8, 0.5, "Problems with this approach",
    font_size=15, bold=True, color=DARK)

for i, p in enumerate(problems):
    row = 1.8 + i * 0.82
    rect(s, 6.5, row, 5.8, 0.65, RGBColor(0xFF, 0xF1, 0xF1))
    box(s, 6.7, row + 0.1, 5.5, 0.45, f"✗  {p}",
        font_size=12, color=ERROR)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Section: The Library Stack
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "The Library Stack", "Three tools, one job")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Three libraries
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "Three Libraries, Three Responsibilities")

libs = [
    (BLUE,  "react-hook-form",
     "Manages form state",
     "Tracks field values, dirty/touched status,\nwhen to show errors, and submission flow.\nOne hook replaces all your useState calls.",
     "react-hook-form.com"),
    (RGBColor(0x7C,0x3A,0xED), "zod",
     "Defines validation rules",
     "Schema-based validation built for TypeScript.\nWrite rules once — get type inference for free.\nUsed beyond forms: APIs, env vars, config files.",
     "zod.dev"),
    (GREEN, "@hookform/resolvers",
     "Connects the two",
     "Thin adapter that makes RHF and Zod\nspeak the same language.\nOne import, one line of config.",
     "github.com/react-hook-form/resolvers"),
]

for i, (color, name, tagline, desc, url) in enumerate(libs):
    col = 0.35 + i * 4.35
    rect(s, col, 1.2, 4.1, 5.5, CARD)
    rect(s, col, 1.2, 4.1, 0.08, color)
    pill(s, col + 0.2, 1.4, 3.7, 0.42, name, bg_color=color)
    box(s, col + 0.2, 2.0, 3.7, 0.4, tagline,
        font_size=13, bold=True, color=DARK)
    box(s, col + 0.2, 2.5, 3.7, 1.8, desc,
        font_size=11, color=MUTED)
    box(s, col + 0.2, 6.1, 3.7, 0.3, f"🔗 {url}",
        font_size=10, color=color, italic=True)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Section: Zod
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "Zod Schemas", "Define rules once · Infer types automatically")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Zod schema code
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "Writing the Zod Schema")

code_block(s, 0.4, 1.2, 6.2, 4.8,
"""import { z } from "zod"

const profileSchema = z.object({
  firstName: z.string().trim()
               .min(2, "Min 2 characters."),

  lastName:  z.string().trim()
               .min(2, "Min 2 characters."),

  email:     z.string().trim()
               .email("Enter a valid email."),

  studentId: z.string().trim()
               .length(9, "Must be 9 characters."),

  phone:     z.string().refine(
    (val) => val.replace(/\\D/g, "").length >= 10,
    "Must have at least 10 digits."
  ),
})

// TypeScript type — generated automatically
type ProfileForm = z.infer<typeof profileSchema>""", font_size=10)

rules = [
    (".trim()",          "Strips spaces before checking"),
    (".min(2)",          "At least 2 characters"),
    (".email()",         "Built-in email format check\n(no regex needed)"),
    (".length(9)",       "Exactly 9 characters"),
    (".refine(fn)",      "Custom rule — strips non-digits\nthen checks count ≥ 10"),
    ("z.infer<>",        "Generates the TS type\nautomatically from the schema"),
]

box(s, 6.9, 1.2, 6, 0.4, "Rule Reference", font_size=14, bold=True, color=DARK)
for i, (rule, desc) in enumerate(rules):
    row = 1.75 + i * 0.88
    rect(s, 6.9, row, 6, 0.75, RGBColor(0xF0, 0xF4, 0xFF))
    box(s, 7.05, row + 0.05, 2, 0.3, rule,
        font_size=11, bold=True, color=BLUE)
    box(s, 9.1, row + 0.05, 3.6, 0.6, desc,
        font_size=10, color=MUTED)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Section: useForm
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "useForm Hook", "The core of React Hook Form")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — useForm breakdown
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "useForm — What You Get Back")

code_block(s, 0.4, 1.2, 5.8, 3.2,
"""const {
  control,
  handleSubmit,
  formState: { errors },
} = useForm<ProfileForm>({
  resolver: zodResolver(profileSchema),
  defaultValues: {
    firstName: "", lastName: "",
    email: "", studentId: "", phone: "",
  },
  mode: "onSubmit",
})""", font_size=11)

items = [
    ("control",           BLUE,  "Passed to every <Controller>.\nLets RHF track each field's value internally."),
    ("handleSubmit",      BLUE,  "Wraps your onSubmit function.\nRuns Zod first — only calls onSubmit if valid."),
    ("formState.errors",  BLUE,  "Object of error messages keyed by field name.\nOnly populated after a failed submit."),
    ("resolver",          RGBColor(0x7C,0x3A,0xED), "zodResolver(schema) — plugs Zod in.\nReplaces your entire manual validate() function."),
    ("defaultValues",     MUTED, "Starting value for every field.\nRequired so RHF knows the initial state."),
    ("mode: 'onSubmit'",  MUTED, "Validate only when user presses Submit.\nOther options: onBlur, onChange, onTouched, all"),
]

for i, (name, color, desc) in enumerate(items):
    row = 1.2 + i * 1.0
    rect(s, 6.5, row, 6.5, 0.85, RGBColor(0xF8, 0xFA, 0xFC))
    rect(s, 6.5, row, 0.06, 0.85, color)
    box(s, 6.7, row + 0.05, 2.2, 0.3, name,
        font_size=12, bold=True, color=DARK)
    box(s, 6.7, row + 0.38, 6.1, 0.42, desc,
        font_size=10, color=MUTED)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Validation modes
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "Validation Modes", "When does RHF run the Zod schema?")

modes = [
    ("onSubmit",  BLUE,  True,  "Only when the user presses Submit.\nBest for beginners — least intrusive."),
    ("onBlur",    GREEN, False, "When the user leaves a field.\nMost common in production apps."),
    ("onChange",  MUTED, False, "On every single keystroke.\nAggressive — useful for password meters."),
    ("onTouched", MUTED, False, "First time on blur, then onChange after.\nA middle ground between onBlur and onChange."),
    ("all",       MUTED, False, "onBlur + onChange combined.\nMost aggressive option."),
]

for i, (mode, color, recommended, desc) in enumerate(modes):
    row = 1.4 + i * 1.08
    rect(s, 0.4, row, 12.5, 0.92, CARD)
    rect(s, 0.4, row, 0.08, 0.92, color)
    pill(s, 0.65, row + 0.22, 1.6, 0.42, f'"{mode}"', bg_color=color)
    if recommended:
        pill(s, 2.4, row + 0.22, 1.8, 0.42, "★ Recommended", bg_color=RGBColor(0xFE,0xF9,0xC3), text_color=RGBColor(0x92,0x40,0x00), font_size=10)
    box(s, 4.4, row + 0.1, 8.2, 0.7, desc, font_size=12, color=DARK)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Section: Controller
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "Controller", "Connecting RHF to React Native inputs")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Controller explained
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "Why Controller? — Web vs React Native")

rect(s, 0.4, 1.3, 5.8, 1.5, RGBColor(0xFF, 0xF1, 0xF1))
box(s, 0.6, 1.35, 5.5, 0.35, "Web HTML — use register()", font_size=12, bold=True, color=ERROR)
code_block(s, 0.4, 1.7, 5.8, 1.0,
"""// HTML input uses onChange
<input {...register("firstName")} />""", font_size=11)

rect(s, 0.4, 3.0, 5.8, 1.5, RGBColor(0xF0, 0xFF, 0xF4))
box(s, 0.6, 3.05, 5.5, 0.35, "React Native — use Controller()", font_size=12, bold=True, color=GREEN)
code_block(s, 0.4, 3.4, 5.8, 1.0,
"""// TextInput uses onChangeText (different!)
<TextInput onChangeText={onChange} />""", font_size=11)

code_block(s, 0.4, 4.6, 5.8, 2.5,
"""<Controller
  control={control}
  name="firstName"
  render={({ field: { onChange, value } }) => (
    <TextInput
      value={value}
      onChangeText={onChange}
      placeholder="e.g. Jane"
    />
  )}
/>""", font_size=10)

points = [
    "control — registers this field with RHF",
    'name — must match a key in your schema',
    "render — gives you value and onChange",
    "value → what the input displays",
    "onChange → called when user types",
    "RHF stores the value internally\n(no useState needed)",
]
box(s, 6.6, 1.3, 6.4, 0.4, "How Controller works", font_size=14, bold=True, color=DARK)
for i, pt in enumerate(points):
    row = 1.85 + i * 0.87
    rect(s, 6.6, row, 6.4, 0.72, RGBColor(0xF0, 0xF4, 0xFF))
    box(s, 6.8, row + 0.1, 6.1, 0.52, f"→  {pt}", font_size=11, color=DARK)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — Section: Error Display
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "Error Display", "Wiring formState.errors to the UI")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — Error display code
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "Displaying Validation Errors")

code_block(s, 0.4, 1.2, 6.1, 4.5,
"""<Text style={styles.label}>First Name</Text>

<Controller
  control={control}
  name="firstName"
  render={({ field: { onChange, value } }) => (
    <TextInput
      style={[
        styles.input,
        errors.firstName && styles.inputError
      ]}
      value={value}
      onChangeText={onChange}
      placeholder="e.g. Jane"
    />
  )}
/>

{errors.firstName && (
  <Text style={styles.error}>
    {errors.firstName.message}
  </Text>
)}""", font_size=10)

box(s, 6.6, 1.2, 6.4, 0.4, "Two layers of error feedback",
    font_size=14, bold=True, color=DARK)

patterns = [
    ("Red border",
     "style={[styles.input, errors.firstName && styles.inputError]}",
     "Array of styles — inputError only applies\nwhen errors.firstName exists.\nOverrides just the borderColor."),
    ("Error message",
     "{errors.firstName && <Text>...</Text>}",
     "Short-circuit rendering.\nIf errors.firstName is undefined → nothing renders.\nIf it has a value → message appears below input."),
    ("Message source",
     'errors.firstName.message',
     "Comes directly from the Zod schema.\nYou wrote it once — it surfaces here automatically.\nNo duplication."),
]

for i, (title, code, desc) in enumerate(patterns):
    row = 1.8 + i * 1.8
    rect(s, 6.6, row, 6.4, 1.6, RGBColor(0xF8, 0xFA, 0xFC))
    rect(s, 6.6, row, 0.07, 1.6, ERROR)
    box(s, 6.8, row + 0.08, 6, 0.3, title, font_size=12, bold=True, color=DARK)
    code_block(s, 6.8, row + 0.42, 6.1, 0.45, code, font_size=9)
    box(s, 6.8, row + 0.98, 6.1, 0.55, desc, font_size=10, color=MUTED)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — Section: Navigation Update
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
section_header(s, "Navigation Update", "Settings gets its own Stack — same pattern as Courses")

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — Folder structure
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "The Same Pattern You Already Know")

code_block(s, 0.4, 1.3, 5.6, 2.5,
"""courses/              settings/
├── _layout.tsx  →    ├── _layout.tsx
├── index.tsx    →    ├── index.tsx
└── [id].tsx          └── profile.tsx

// Stack navigator — identical structure
export default function SettingsLayout() {
  return (
    <Stack>
      <Stack.Screen name="index"
        options={{ title: "Settings" }} />
      <Stack.Screen name="profile"
        options={{ title: "Edit Profile" }} />
    </Stack>
  )
}""", font_size=10)

steps = [
    ("1", "Create settings/ folder",   "Move settings.tsx content into settings/index.tsx"),
    ("2", "Add _layout.tsx",           "Stack navigator — same as courses/_layout.tsx"),
    ("3", "Create profile.tsx",        "The Edit Profile form screen"),
    ("4", "Delete settings.tsx",       "Avoids duplicate route conflict with index.tsx"),
    ("5", "Wrap Account card",         "Pressable + router.push('/(tab)/settings/profile')"),
]

box(s, 6.4, 1.3, 6.5, 0.4, "Steps to convert the tab", font_size=14, bold=True, color=DARK)
for i, (num, title, desc) in enumerate(steps):
    row = 1.85 + i * 1.02
    rect(s, 6.4, row, 0.52, 0.82, BLUE)
    box(s, 6.4, row, 0.52, 0.82, num, font_size=18, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    box(s, 7.05, row + 0.05, 5.7, 0.3, title, font_size=13, bold=True, color=DARK)
    box(s, 7.05, row + 0.40, 5.7, 0.35, desc, font_size=11, color=MUTED)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 18 — Common Mistakes
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s)
slide_title(s, "Common Mistakes to Avoid")

mistakes = [
    ("onChange vs onChangeText",
     "<TextInput onChange={onChange} />",
     "<TextInput onChangeText={onChange} />",
     "onChange is the HTML handler. React Native uses onChangeText.\nThe field will appear frozen if you use the wrong one."),
    ("Skipping handleSubmit",
     "onPress={onSubmit}",
     "onPress={handleSubmit(onSubmit)}",
     "Calling onSubmit directly skips validation entirely.\nAlways wrap it with handleSubmit."),
    ("Missing resolver",
     "useForm({ defaultValues: {...} })",
     "useForm({ resolver: zodResolver(schema), ... })",
     "Without the resolver, the Zod schema is completely ignored.\nThe form will accept any data."),
    ("Not deleting settings.tsx",
     "settings.tsx + settings/index.tsx both exist",
     "Delete settings.tsx after creating the folder",
     "Expo Router will throw a duplicate route error.\nAlways delete the single file when converting to a folder."),
]

for i, (title, wrong, right, note) in enumerate(mistakes):
    row = 1.3 + i * 1.5
    rect(s, 0.4, row, 12.5, 1.35, CARD)
    rect(s, 0.4, row, 0.07, 1.35, ERROR)
    box(s, 0.65, row + 0.05, 12, 0.3, title, font_size=13, bold=True, color=DARK)
    box(s, 0.65, row + 0.38, 1, 0.28, "✗", font_size=13, bold=True, color=ERROR)
    box(s, 1.0, row + 0.38, 5.2, 0.28, wrong, font_size=10, color=ERROR)
    box(s, 6.5, row + 0.38, 0.5, 0.28, "✓", font_size=13, bold=True, color=GREEN)
    box(s, 6.9, row + 0.38, 5.8, 0.28, right, font_size=10, color=GREEN)
    box(s, 0.65, row + 0.75, 12, 0.45, note, font_size=10, color=MUTED)

# ════════════════════════════════════════════════════════════════════════════════
# SLIDE 19 — Summary
# ════════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, DARK)
rect(s, 0, 0, 13.33, 0.6, BLUE)

box(s, 0.8, 0.8, 11.5, 0.7, "Week 8 — Key Takeaways",
    font_size=28, bold=True, color=WHITE)

takeaways = [
    ("🗂", "Schema first",        "Write Zod rules once. Types, validation, and error messages all come from the same place."),
    ("🪝", "One hook",            "useForm replaces all your useState calls. control, handleSubmit, and errors are all you need."),
    ("🎮", "Controller",          "The React Native-friendly wrapper. Gives your TextInput value and onChangeText from RHF."),
    ("🛡", "handleSubmit",        "Always wrap your submit function. It runs Zod, blocks invalid submissions, and types your data."),
    ("📁", "Same nav pattern",    "Settings folder mirrors Courses. The nested Stack pattern is now used in two tabs — learn it once, use it everywhere."),
]

for i, (icon, title, desc) in enumerate(takeaways):
    row = 1.6 + i * 1.1
    rect(s, 0.8, row, 11.7, 0.95, RGBColor(0x1E, 0x29, 0x3B))
    box(s, 0.95, row + 0.12, 0.6, 0.65, icon, font_size=22, color=WHITE)
    box(s, 1.65, row + 0.08, 2.2, 0.35, title, font_size=13, bold=True, color=BLUE)
    box(s, 1.65, row + 0.45, 10.5, 0.38, desc, font_size=11, color=RGBColor(0xCB, 0xD5, 0xE1))

box(s, 0.8, 7.05, 11.5, 0.35,
    "Docs: react-hook-form.com  ·  zod.dev  ·  github.com/react-hook-form/resolvers",
    font_size=11, color=MUTED, align=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════════════════════
# Save
# ════════════════════════════════════════════════════════════════════════════════
out = r"D:\Winter 2026\campus-hub-weekly\docs\Week8_Forms_Validation.pptx"
prs.save(out)
print(f"Saved: {out}")
