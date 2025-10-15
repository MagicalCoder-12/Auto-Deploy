Write-Host "🚀 Running Auto Deploy Agent..." -ForegroundColor Green
Write-Host "===============================" -ForegroundColor Green
python deploy_agent.py
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")