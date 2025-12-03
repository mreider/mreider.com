# 📱 iOS Shortcut Visual Guide

## What You'll Build

A one-tap shortcut that looks like this:

```
┌─────────────────────────────┐
│  💪 Log Fitness             │
└─────────────────────────────┘
```

When tapped, it shows:

```
┌─────────────────────────────┐
│  What date?                 │
│                             │
│  📅 December 3, 2024        │
│                             │
│  [Today] [Select Date]      │
└─────────────────────────────┘
```

Then:

```
┌─────────────────────────────┐
│  What did you do today?     │
│                             │
│  💪 Exercise + 🥗 Diet      │
│  💪 Exercise Only           │
│  🥗 Healthy Food Only       │
│  😴 Rest Day                │
└─────────────────────────────┘
```

Finally:

```
┌─────────────────────────────┐
│  ✅ Fitness logged!         │
│  Check GitHub Actions       │
└─────────────────────────────┘
```

---

## Shortcut Actions Flow

Here's exactly what each action does:

```
┌──────────────────────────────────────┐
│ 1. Ask for Input                     │
│    Type: Date and Time               │
│    Question: "What date?"            │
│    Default: Current Date             │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 2. Format Date                       │
│    Format: Custom                    │
│    Date Format: yyyy-MM-dd           │
│    Input: Date from step 1           │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 3. Choose from Menu                  │
│    Prompt: "What did you do?"        │
│    ├─ 💪 Exercise + 🥗 Diet          │
│    │   ├─ Text: "true"               │
│    │   ├─ Set Variable: workout      │
│    │   ├─ Text: "true"               │
│    │   └─ Set Variable: diet         │
│    ├─ 💪 Exercise Only               │
│    │   ├─ Text: "true"               │
│    │   ├─ Set Variable: workout      │
│    │   ├─ Text: "false"              │
│    │   └─ Set Variable: diet         │
│    ├─ 🥗 Healthy Food Only           │
│    │   ├─ Text: "false"              │
│    │   ├─ Set Variable: workout      │
│    │   ├─ Text: "true"               │
│    │   └─ Set Variable: diet         │
│    └─ 😴 Rest Day                    │
│        ├─ Text: "false"              │
│        ├─ Set Variable: workout      │
│        ├─ Text: "false"              │
│        └─ Set Variable: diet         │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 4. Text (Build JSON)                 │
│    {                                 │
│      "ref": "main",                  │
│      "inputs": {                     │
│        "date": "[Formatted Date]",   │
│        "workout": "[workout]",       │
│        "diet": "[diet]"              │
│      }                               │
│    }                                 │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 5. Get Contents of URL               │
│    Method: POST                      │
│    URL: https://api.github.com/...   │
│    Headers:                          │
│      - Accept: application/...       │
│      - Authorization: Bearer TOKEN   │
│      - X-GitHub-Api-Version: 2022... │
│    Body: JSON from step 4            │
└──────────────────────────────────────┘
                 ↓
┌──────────────────────────────────────┐
│ 6. Show Notification                 │
│    Title: "✅ Fitness logged!"       │
│    Body: "Check GitHub Actions"      │
└──────────────────────────────────────┘
```

---

## Finding Actions in Shortcuts App

When you tap "Add Action", search for:

| Step | Search Term | Category |
|------|-------------|----------|
| 1 | "ask for input" | Scripting |
| 2 | "format date" | Calendar |
| 3 | "choose from menu" | Scripting |
| 4 | "text" | Scripting |
| 5 | "set variable" | Scripting |
| 6 | "get contents" | Web |
| 7 | "show notification" | Scripting |

---

## Adding Variables in Text

When building the JSON in step 4:

1. Type the JSON template
2. Tap on placeholder text (like `FORMATTED_DATE`)
3. Long-press and select "Variables"
4. Choose the variable you created earlier

The final text should show variables as colored pills:

```
{
  "ref": "main",
  "inputs": {
    "date": "┌────────────────┐",
    "workout": "│ Formatted Date │",
    "diet": "└────────────────┘"
  }
}
```

---

## Common Mistakes to Avoid

❌ **Don't** type "true" and "false" with quotes in the Set Variable actions
✅ **Do** use the Text action to set "true" or "false", then assign to variable

❌ **Don't** forget to add all 3 headers in the API request
✅ **Do** add Accept, Authorization, and X-GitHub-Api-Version headers

❌ **Don't** put your token directly in the JSON body
✅ **Do** put it in the Authorization header: `Bearer YOUR_TOKEN`

❌ **Don't** use `yyyy-mm-dd` (lowercase 'mm' is minutes!)
✅ **Do** use `yyyy-MM-dd` (uppercase 'MM' is months!)

---

## Testing Your Shortcut

Before relying on it, test with a known date:

1. Run the shortcut
2. Choose yesterday's date
3. Select "Rest Day"
4. Wait 30 seconds
5. Go to: https://github.com/mreider/mreider.com/actions
6. You should see "Update Fitness Tracker" running
7. After it completes, check your fitness page

If it works, you're all set! 🎉

---

## Advanced: Using Siri

Once your shortcut is created:

1. Open Settings → Siri & Search
2. Scroll to "Shortcuts"
3. Find "Log Fitness"
4. Record phrase: "Log my fitness" or "Log workout"

Now just say: **"Hey Siri, log my fitness"** 🎤

---

## Advanced: Daily Reminder Automation

Make it automatic:

1. Open Shortcuts app
2. Tap "Automation" tab (bottom)
3. Tap "+" → "Create Personal Automation"
4. Choose "Time of Day"
5. Set time (e.g., 9:00 PM)
6. Set frequency: Daily
7. Next → Add Action → "Run Shortcut"
8. Choose "Log Fitness"
9. Toggle OFF "Ask Before Running" (optional)
10. Done

Now every evening at 9 PM, you'll get prompted! 🔔
