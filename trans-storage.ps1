# 定义两个参数
param(
    [string]$sourcePath,
    [string]$targetPath
)

# 检查当前进程是否有管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin) {
    Write-Error "Please run this script as an administrator"
    exit
}

# 检查参数是否有效
if (-not (Test-Path $sourcePath)) {
    Write-Error "Invalid src path"
    exit
}
if (-not (Test-Path $targetPath)) {
    Write-Error "Invalid target path"
    exit
}

$sourceName = Split-Path $sourcePath -Leaf
$targetFullPath = Join-Path $targetPath $sourceName

Move-Item $sourcePath $targetFullPath -Force
if (Test-Path $sourcePath -PathType Container) {
    New-Item -ItemType SymbolicLink -Path $sourcePath -Target $targetFullPath
} elseif (Test-Path $sourcePath -PathType Leaf) {
    New-Item -ItemType HardLink -Path $sourcePath -Target $targetFullPath
}
