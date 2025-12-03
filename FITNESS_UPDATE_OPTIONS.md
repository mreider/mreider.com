# Fitness Tracker Update Options

There are multiple ways to update your fitness tracker:

## 📱 iOS / iPad (Recommended for Daily Use)

**Best for**: Quick daily logging on your phone

Use the iOS Shortcuts app to create a button on your home screen.

**Setup Guide**: [IOS_SHORTCUT_SETUP.md](./IOS_SHORTCUT_SETUP.md)

**Features**:
- ✅ Date picker with calendar
- ✅ Easy menu selection (Exercise + Diet, Exercise Only, etc.)
- ✅ Home screen widget
- ✅ Siri support: "Hey Siri, Log Fitness"
- ✅ Can automate to remind you daily

**Time to setup**: ~10 minutes

---

## 💻 Mac Terminal (For Developers)

**Best for**: Command-line users, automation scripts

Use the shell script to trigger updates from your Mac terminal.

**Script**: `.github/scripts/trigger_fitness_update.sh`

**Usage**:
```bash
# Set your GitHub token (one time)
export GITHUB_TOKEN="your_token_here"

# Update fitness for today
./trigger_fitness_update.sh 2024-12-03 true true

# Arguments: [date] [workout:true/false] [diet:true/false]
```

**Features**:
- ✅ Fast command-line updates
- ✅ Can integrate into other scripts
- ✅ Good for batch updates

---

## 🌐 GitHub Actions UI (Manual Trigger)

**Best for**: Occasional updates, testing

Go directly to GitHub and trigger the workflow manually.

**Steps**:
1. Go to: https://github.com/mreider/mreider.com/actions
2. Click "Update Fitness Tracker" workflow
3. Click "Run workflow" button
4. Fill in:
   - Date (YYYY-MM-DD)
   - Workout (true/false)
   - Diet (true/false)
5. Click "Run workflow"

**Features**:
- ✅ No setup required
- ✅ Works anywhere with web browser
- ✅ Most reliable (direct GitHub interface)

---

## 🔑 Getting Your GitHub Token

All methods (except GitHub UI) require a Personal Access Token:

1. Visit: https://github.com/settings/tokens/new
2. Name: "Fitness Tracker"
3. Expiration: Choose 90 days or No expiration
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

**Security tip**: Store it securely! Don't share it or commit it to GitHub.

---

## 📊 Viewing Your Progress

After updating, check your fitness tracker page:
- Live site: https://mreider.com/fitness/
- Local: Open `content/fitness.md` in browser after running Hugo

---

## 🆘 Troubleshooting

**"Workflow not found"**
- Check repository name is correct: `mreider/mreider.com`
- Verify workflow file exists: `.github/workflows/update-fitness.yml`

**"Bad credentials"**
- Token expired - generate a new one
- Token doesn't have `workflow` scope - regenerate with correct scopes

**"Nothing happens"**
- Check GitHub Actions tab: https://github.com/mreider/mreider.com/actions
- Look for running or failed workflows
- Check workflow logs for errors

**"Date not found in tracker"**
- The date must exist in `content/fitness.md`
- Add new weeks manually or create a script to generate them

---

## 🎯 Recommended Setup

**Daily users**: Set up the iOS Shortcut (10 min setup, super convenient after)

**Power users**: Use both - iOS for daily logging, terminal for batch updates

**Occasional users**: Just use the GitHub Actions UI
