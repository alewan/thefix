@set PYTHONIOENCODING=utf-8
@powershell -noprofile -c "cmd /c \"$(thefix %* $(doskey /history)[-2])\"; [Console]::ResetColor();"
