$File = Get-Item -Path "packages*.json"
switch (($File | Measure-Object).Count){
    0 {
        Write-Output -InputObject "No pacakges-<nnn>.json file found."
    }
    1 {
        $Packages = $File | Get-Content | ConvertFrom-Json
        $Packages.packages | ForEach-Object {
            $Package = $_
            choco upgrade $Package.Name --version $Package.Version
        }
    }
    default {
        Write-Output -InputObject "Too many files found. Make sure only 1 packages-<nnn>.json exist."
        Write-Output -InputObject $File.Name
    }
}
