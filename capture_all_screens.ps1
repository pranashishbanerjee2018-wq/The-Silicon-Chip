$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$baseDir = "C:\Users\prana\.gemini\antigravity\scratch\inside_the_silicon"
$outDir = "$baseDir\docs\screenshots"

$scenes = @(
    @{ Name = "01_hero_gateway.png"; Url = "file:///$baseDir/index.html" },
    @{ Name = "02_cleanroom_two_characters.png"; Url = "file:///$baseDir/index.html#act=1" },
    @{ Name = "03_silicon_lattice.png"; Url = "file:///$baseDir/index.html#act=2" },
    @{ Name = "04_pn_junction.png"; Url = "file:///$baseDir/index.html#act=3" },
    @{ Name = "05_mosfet_transistor.png"; Url = "file:///$baseDir/index.html#act=4" },
    @{ Name = "06_matlab_workbench.png"; Url = "file:///$baseDir/index.html#act=5" },
    @{ Name = "07_ic_scale_zoom.png"; Url = "file:///$baseDir/index.html#act=6" },
    @{ Name = "08_viva_exam_modal.png"; Url = "file:///$baseDir/index.html#modal=tech" }
)

foreach ($s in $scenes) {
    $outPath = "$outDir\" + $s.Name
    Write-Host "Capturing $($s.Name)..."
    Start-Process -FilePath $chrome -ArgumentList "--headless=new", "--virtual-time-budget=2000", "--screenshot=$outPath", "--window-size=1440,900", $s.Url -Wait
    if (Test-Path $outPath) {
        $len = (Get-Item $outPath).Length
        Write-Host "  [OK] $($s.Name) ($len bytes)"
    } else {
        Write-Host "  [FAIL] $($s.Name)"
    }
}
Write-Host "All captures finished."
