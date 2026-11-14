if ((Get-Command "fix").CommandType -eq "Function") {
	fix @args;
	[Console]::ResetColor()
	exit
}

"First time use of thefix detected. "

if ((Get-Content $PROFILE -Raw -ErrorAction Ignore) -like "*thefix*") {
} else {
	"  - Adding thefix intialization to user `$PROFILE"
	$script = "`n`$env:PYTHONIOENCODING='utf-8' `niex `"`$(thefix --alias)`"";
	Write-Output $script | Add-Content $PROFILE
}

"  - Adding fix() function to current session..."
$env:PYTHONIOENCODING='utf-8'
iex "$($(thefix --alias).Replace("function fix", "function global:fix"))"

"  - Invoking fix()`n"
fix @args;
[Console]::ResetColor()
