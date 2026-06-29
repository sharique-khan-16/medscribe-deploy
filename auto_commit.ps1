# Auto Commit Script for medscribe git repository
# Designed to be run hourly by Windows Task Scheduler from 8 AM to 5 PM.

$repoPath = "C:\Users\khans\medscribe"
$logPath = "$repoPath\auto_commit.log"
$activityFile = "$repoPath\activity_log.txt"

# Ensure we are in the repository directory
Set-Location -Path $repoPath -ErrorAction Stop

$now = Get-Date
$timestamp = $now.ToString("yyyy-MM-dd HH:mm:ss")
$hour = $now.Hour

# Log execution start
Add-Content -Path $logPath -Value "[$timestamp] Script triggered."

# Verify active hours (8 AM to 5 PM inclusive)
# 8 AM is hour 8, 5 PM is hour 17.
if ($hour -ge 8 -and $hour -le 17) {
    try {
        # 1. Update activity log file
        Add-Content -Path $activityFile -Value "Hourly activity check-in: $timestamp" -ErrorAction Stop

        # 2. Stage the activity log file
        $addOutput = git add "$activityFile" 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "git add failed: $addOutput"
        }

        # 3. Commit the change
        $commitMessage = "chore: automated hourly commit - $timestamp"
        $commitOutput = git commit -m "$commitMessage" 2>&1
        if ($LASTEXITCODE -ne 0 -and $commitOutput -notlike "*nothing to commit*") {
            throw "git commit failed: $commitOutput"
        }

        # 4. Push to remote
        $pushOutput = git push origin main 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "git push failed: $pushOutput"
        }

        Add-Content -Path $logPath -Value "[$timestamp] SUCCESS: Committed and pushed successfully."
    }
    catch {
        $err = $_
        Add-Content -Path $logPath -Value "[$timestamp] ERROR: $err"
    }
} else {
    Add-Content -Path $logPath -Value "[$timestamp] SKIPPED: Current hour ($hour) is outside active hours (8 AM - 5 PM)."
}
