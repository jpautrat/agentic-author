Write-Host "Pushing to GitHub with token authentication..."
Write-Host ""

# Get the token from the user
$token = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($token)
$tokenText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Set the remote URL with the token
$remoteUrl = "https://jpautrat:$tokenText@github.com/jpautrat/agentic-author.git"
git remote set-url origin $remoteUrl

# Push to GitHub
Write-Host "Pushing to GitHub..."
git push -u origin main

# Reset the remote URL for security
git remote set-url origin https://github.com/jpautrat/agentic-author.git

Write-Host ""
Write-Host "Done! Check your repository at https://github.com/jpautrat/agentic-author"
Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
