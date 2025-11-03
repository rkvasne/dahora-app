# Simple static web server for local preview (Windows PowerShell)
param(
    [int]$Port = 5500
)

$listener = New-Object System.Net.HttpListener
$prefix = "http://localhost:$Port/"
$listener.Prefixes.Add($prefix)
$listener.Start()
Write-Host "Servidor rodando em $prefix" -ForegroundColor Cyan

function Get-MimeType($ext) {
    switch ($ext.ToLower()) {
        '.html' { 'text/html' }
        '.css'  { 'text/css' }
        '.js'   { 'application/javascript' }
        '.png'  { 'image/png' }
        '.jpg'  { 'image/jpeg' }
        '.jpeg' { 'image/jpeg' }
        '.ico'  { 'image/x-icon' }
        default { 'application/octet-stream' }
    }
}

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $path = $context.Request.Url.AbsolutePath.TrimStart('/')
        if ([string]::IsNullOrWhiteSpace($path)) { $path = 'index.html' }
        $full = Join-Path (Get-Location) $path
        if (Test-Path $full) {
            $bytes = [System.IO.File]::ReadAllBytes($full)
            $ext = [System.IO.Path]::GetExtension($full)
            $context.Response.ContentType = Get-MimeType $ext
            $context.Response.OutputStream.Write($bytes,0,$bytes.Length)
        } else {
            $context.Response.StatusCode = 404
            $msg = [System.Text.Encoding]::UTF8.GetBytes('Not Found')
            $context.Response.OutputStream.Write($msg,0,$msg.Length)
        }
        $context.Response.OutputStream.Close()
    }
}
finally {
    $listener.Stop()
}