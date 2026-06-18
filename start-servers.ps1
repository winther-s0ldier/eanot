$proxyJob = Start-Job -ScriptBlock {
    Set-Location "Z:\eanot\proxy-server"
    uvicorn app:app --host 0.0.0.0 --port 5000 --reload
}

$frontendJob = Start-Job -ScriptBlock {
    Set-Location "Z:\eanot\frontend"
    python -m http.server 8080
}

Write-Output "Proxy PID: $($proxyJob.Id)"
Write-Output "Frontend PID: $($frontendJob.Id)"

# Wait forever so servers stay up
while ($true) {
    Start-Sleep -Seconds 10
}
