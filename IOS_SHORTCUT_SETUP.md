# Fitness Tracker Shortcut - Quick Setup

## 🚀 Quick Import (Coming Soon)

Apple Shortcuts can be shared via iCloud links. For now, follow the manual setup below.

## 📱 Manual Setup (10 minutes)

### Simplified Step-by-Step

1. **Open Shortcuts app** on iPhone/iPad/Mac

2. **Create New Shortcut** (+ button)

3. **Add these actions** (search and add each):

   ```
   1. "Ask for Input" 
      → Type: Date and Time
      → Question: "What date?"
   
   2. "Format Date"
      → Format: Custom → yyyy-MM-dd
      → Date from step 1
   
   3. "Choose from Menu"
      → Prompt: "What did you do today?"
      → Options:
        • "💪 Exercise + 🥗 Healthy Food"
        • "💪 Exercise Only"  
        • "🥗 Healthy Food Only"
        • "😴 Rest Day"
   
   4. Inside "💪 Exercise + 🥗 Healthy Food":
      - Add "Text" action: true
      - Add "Set Variable": workout
      - Add "Text" action: true
      - Add "Set Variable": diet
   
   5. Inside "💪 Exercise Only":
      - Add "Text" action: true
      - Add "Set Variable": workout
      - Add "Text" action: false
      - Add "Set Variable": diet
   
   6. Inside "🥗 Healthy Food Only":
      - Add "Text" action: false
      - Add "Set Variable": workout
      - Add "Text" action: true
      - Add "Set Variable": diet
   
   7. Inside "😴 Rest Day":
      - Add "Text" action: false
      - Add "Set Variable": workout
      - Add "Text" action: false
      - Add "Set Variable": diet
   
   8. "Text" (after menu closes):
      {
        "ref": "main",
        "inputs": {
          "date": "FORMATTED_DATE",
          "workout": "WORKOUT_VAR",
          "diet": "DIET_VAR"
        }
      }
      (Tap FORMATTED_DATE → select "Formatted Date" variable)
      (Tap WORKOUT_VAR → select "workout" variable)
      (Tap DIET_VAR → select "diet" variable)
   
   9. "Get Contents of URL"
      → URL: https://api.github.com/repos/mreider/mreider.com/actions/workflows/update-fitness.yml/dispatches
      → Method: POST
      → Headers (tap "Add new field" 3 times):
        • Accept: application/vnd.github+json
        • Authorization: Bearer YOUR_GITHUB_TOKEN
        • X-GitHub-Api-Version: 2022-11-28
      → Request Body: JSON (select text from step 8)
   
   10. "Show Result"
       → Show Notification
       → Title: "✅ Fitness logged!"
       → Body: "Check GitHub Actions"
   ```

4. **Get Your GitHub Token**:
   - Visit: https://github.com/settings/tokens/new
   - Name: "Fitness Tracker"
   - Expiration: 90 days or No expiration
   - Select scopes: ✅ repo, ✅ workflow
   - Generate → Copy the token

5. **Paste Token** into step 9 (replace YOUR_GITHUB_TOKEN)

6. **Name it** "Log Fitness"

7. **Test it!**

## 🎯 Even Simpler: 3-Button Version

If the above is too complex, use this ultra-simple version:

```
1. "Ask for Input" → Date
2. "Format Date" → yyyy-MM-dd  
3. "Ask for Input" → Text: "Exercise? (yes/no)"
4. "Ask for Input" → Text: "Healthy food? (yes/no)"
5. "Text":
   {
     "ref": "main",
     "inputs": {
       "date": "DATE",
       "workout": "EXERCISE_ANSWER",
       "diet": "FOOD_ANSWER"
     }
   }
6. "Get Contents of URL" → POST (same as above)
7. "Show Notification"
```

This version just asks yes/no for each question.

## 🏠 Add to Home Screen

1. Long-press the shortcut
2. Tap "Details"
3. Tap "Add to Home Screen"
4. Choose an icon (🏋️ or 🥗)
5. Done! Now it's on your home screen

## 🎤 Use with Siri

Just say: **"Hey Siri, Log Fitness"**

## ⚡ Daily Automation

Set it to remind you:

1. Open Shortcuts app
2. Go to "Automation" tab
3. Create Personal Automation
4. "Time of Day" → 9:00 PM daily
5. Add action "Run Shortcut" → "Log Fitness"
6. Disable "Ask Before Running" (optional)

Now it'll prompt you every evening!

## 🔒 Security

Your GitHub token is stored in the shortcut on your device only. It's not uploaded anywhere except to GitHub's API when you run it.

**Best practice**: Use a token with minimal permissions (just this repo) and set an expiration date.

## ❓ Troubleshooting

**"The operation couldn't be completed"**
→ Check your internet connection

**"Workflow not found"**  
→ Verify repo name is exactly: `mreider/mreider.com`

**"Bad credentials"**
→ Token expired or incorrect - generate a new one

**Nothing happens**
→ Check GitHub Actions tab - it might be running

## 🔗 Useful Links

- GitHub Actions: https://github.com/mreider/mreider.com/actions
- Token Settings: https://github.com/settings/tokens
- Shortcuts Gallery: https://support.apple.com/guide/shortcuts/
