$Packages = Get-Content -Path .\packages.json | ConvertFrom-Json

$Packages.packages | ForEach-Object {
    $Package = $_
    choco upgrade $Package.Name --version $Package.Version
}
