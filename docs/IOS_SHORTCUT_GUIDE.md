# iOS Shortcut for Fitness Tracker

This guide shows how to create an iOS/Mac Shortcut that updates your fitness tracker via GitHub Actions.

## Prerequisites

1. **GitHub Personal Access Token**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Give it a name: "Fitness Tracker iOS"
   - Select scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
   - Generate and **copy the token** (you won't see it again!)

2. **iOS Shortcuts App**
   - Pre-installed on iPhone/iPad
   - Available on Mac (macOS 12+)

## Shortcut Setup Instructions

### Step 1: Create a New Shortcut

1. Open the **Shortcuts** app
2. Tap **+** (plus) button to create a new shortcut
3. Name it "Log Fitness"

### Step 2: Add Actions

Add these actions in order (tap "Add Action" and search for each):

#### 1. Ask for Date
```
Action: Ask for Input
- Prompt: "What date?"
- Input Type: Date
- Default Value: Current Date
```

#### 2. Format Date
```
Action: Format Date
- Date: (select output from "Ask for Input")
- Format: Custom
- Custom Format: yyyy-MM-dd
```

#### 3. Ask About Exercise
```
Action: Ask for Input
- Prompt: "Did you exercise today?"
- Input Type: Text
- Default Value: (leave empty)
```

#### 4. Convert Exercise to Boolean
```
Action: If
- If: (output from "Ask for Input" about exercise)
- Condition: contains
- Value: yes

Then:
  Action: Text
  - Text: true
  
Otherwise:
  Action: Text
  - Text: false
```

#### 5. Set Variable for Exercise
```
Action: Set Variable
- Variable Name: workoutValue
- Value: (output from If statement)
```

#### 6. Ask About Diet
```
Action: Ask for Input
- Prompt: "Did you eat healthy today?"
- Input Type: Text
- Default Value: (leave empty)
```

#### 7. Convert Diet to Boolean
```
Action: If
- If: (output from "Ask for Input" about diet)
- Condition: contains
- Value: yes

Then:
  Action: Text
  - Text: true
  
Otherwise:
  Action: Text
  - Text: false
```

#### 8. Set Variable for Diet
```
Action: Set Variable
- Variable Name: dietValue
- Value: (output from If statement)
```

#### 9. Create JSON Body
```
Action: Text
- Text:
{
  "ref": "main",
  "inputs": {
    "date": "[Formatted Date]",
    "workout": "[workoutValue]",
    "diet": "[dietValue]"
  }
}

(Replace [Formatted Date], [workoutValue], [dietValue] with the actual variables)
```

#### 10. Make API Request
```
Action: Get Contents of URL
- URL: https://api.github.com/repos/mreider/mreider.com/actions/workflows/update-fitness.yml/dispatches
- Method: POST
- Headers:
  - Accept: application/vnd.github+json
  - Authorization: Bearer YOUR_GITHUB_TOKEN_HERE
  - X-GitHub-Api-Version: 2022-11-28
- Request Body: JSON (from previous Text action)
```

#### 11. Show Result
```
Action: Show Notification
- Title: Fitness Updated!
- Body: Check GitHub Actions for progress
```

### Step 3: Configure the API Request

In the "Get Contents of URL" action:
1. Tap "Show More"
2. Set **Method** to `POST`
3. Add **Headers**:
   - Key: `Accept`, Value: `application/vnd.github+json`
   - Key: `Authorization`, Value: `Bearer YOUR_TOKEN_HERE` (replace with your token)
   - Key: `X-GitHub-Api-Version`, Value: `2022-11-28`
4. Set **Request Body** to the JSON text from step 9

### Step 4: Test It

1. Run the shortcut
2. Pick today's date
3. Answer "yes" or "no" for exercise
4. Answer "yes" or "no" for diet
5. Check GitHub Actions: https://github.com/mreider/mreider.com/actions

## Alternative: Simpler Version with Menu

For a quicker version, replace steps 3-8 with:

```
Action: Choose from Menu
- Prompt: "Today's fitness:"

Menu Items:
  - "Exercise + Diet" → Set both to true
  - "Exercise only" → workout=true, diet=false
  - "Diet only" → workout=false, diet=true
  - "Rest day" → Set both to false
```

## Tips

- **Add to Home Screen**: Long-press the shortcut → "Add to Home Screen"
- **Siri**: Say "Hey Siri, log fitness" to run it
- **Widget**: Add Shortcuts widget to your home screen
- **Automation**: Set it to run automatically at a specific time each day

## Security Note

⚠️ Your GitHub token will be stored in the shortcut. Keep your device secure!

## Troubleshooting

**Error: "Invalid request"**
- Check that your token has `repo` and `workflow` permissions
- Verify the repository name is correct

**Error: "Workflow not found"**
- Make sure `update-fitness.yml` exists in `.github/workflows/`
- Check the branch is `main` (not `master`)

**No response**
- Check your internet connection
- Verify the token hasn't expired (tokens can expire)
