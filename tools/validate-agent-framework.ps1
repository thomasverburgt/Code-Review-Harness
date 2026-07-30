[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$registryPath = Join-Path $repositoryRoot 'agents\agent-identities.json'
$registry = Get-Content -Raw -Encoding utf8 -LiteralPath $registryPath | ConvertFrom-Json
$errors = [System.Collections.Generic.List[string]]::new()

function Add-ValidationError {
    param([string]$Message)
    $errors.Add($Message)
}

if ($registry.registry_version -notmatch '^\d+\.\d+\.\d+$') {
    Add-ValidationError "Invalid registry version: $($registry.registry_version)"
}

$uuidOwners = @{}
$designationOwners = @{}
$allNames = @{}
$namespaceByLayer = @{
    specialist = 'SPEC'
    product = 'PROD'
    capability = 'CAP'
    enterprise = 'ENT'
    work = 'WORK'
    orchestration = 'ORCH'
}

foreach ($agent in $registry.agents) {
    $designation = [string]$agent.designation
    $uuid = [string]$agent.agent_uuid

    if ($designation -notmatch '^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$') {
        Add-ValidationError "Invalid designation: $designation"
    }
    $expectedNamespace = $namespaceByLayer[[string]$agent.layer]
    if ($designation -notlike "$expectedNamespace-*") {
        Add-ValidationError "Layer/namespace mismatch for ${designation}: $($agent.layer)"
    }
    if ([string]$agent.contract_version -notmatch '^\d+\.\d+\.\d+$') {
        Add-ValidationError "Invalid contract version for ${designation}: $($agent.contract_version)"
    }
    $parsedGuid = [guid]::Empty
    if (-not [guid]::TryParse($uuid, [ref]$parsedGuid)) {
        Add-ValidationError "Invalid UUID for ${designation}: $uuid"
    }
    if ($uuidOwners.ContainsKey($uuid)) {
        Add-ValidationError "Duplicate UUID $uuid for $designation and $($uuidOwners[$uuid])"
    } else {
        $uuidOwners[$uuid] = $designation
    }
    if ($designationOwners.ContainsKey($designation)) {
        Add-ValidationError "Duplicate designation: $designation"
    } else {
        $designationOwners[$designation] = $uuid
    }
    if ($allNames.ContainsKey($designation)) {
        Add-ValidationError "Designation or alias collision: $designation"
    } else {
        $allNames[$designation] = $uuid
    }

    foreach ($alias in @($agent.legacy_designations)) {
        if ([string]::IsNullOrWhiteSpace([string]$alias)) {
            continue
        }
        if ($allNames.ContainsKey([string]$alias)) {
            Add-ValidationError "Designation or alias collision: $alias"
        } else {
            $allNames[[string]$alias] = $uuid
        }
    }

    $specificationPath = Join-Path (Join-Path $repositoryRoot 'agents') ([string]$agent.specification)
    if (-not (Test-Path -LiteralPath $specificationPath -PathType Leaf)) {
        Add-ValidationError "Missing specification for ${designation}: $($agent.specification)"
    }
}

$requiredEnterpriseAgents = @(
    'ENT-EVIDENCE', 'ENT-ARCH', 'ENT-SYSRISK', 'ENT-GOV', 'ENT-STRAT',
    'ENT-PORTFOLIO', 'ENT-ARCHSTRAT', 'ENT-MATURITY', 'ENT-TECHDEBT',
    'ENT-MODERNIZE', 'ENT-LEARN', 'ENT-SYNTH'
)
foreach ($designation in $requiredEnterpriseAgents) {
    if (-not $designationOwners.ContainsKey($designation)) {
        Add-ValidationError "Missing enterprise agent: $designation"
    }
}

$catalogText = Get-Content -Raw -Encoding utf8 -LiteralPath (Join-Path $repositoryRoot 'agents\agent-registry.md')
foreach ($designation in $designationOwners.Keys) {
    if (-not $catalogText.Contains("``$designation``")) {
        Add-ValidationError "Agent is missing from the human-readable catalog: $designation"
    }
}

Get-ChildItem -Path $repositoryRoot -Recurse -Filter '*.json' | ForEach-Object {
    try {
        Get-Content -Raw -Encoding utf8 -LiteralPath $_.FullName | ConvertFrom-Json | Out-Null
    } catch {
        Add-ValidationError "Invalid JSON: $($_.FullName): $($_.Exception.Message)"
    }
}

if (Get-Command Test-Json -ErrorAction SilentlyContinue) {
    $schemaPath = Join-Path $repositoryRoot 'appendices\schemas\agent-identity-registry.schema.json'
    $schemaText = Get-Content -Raw -Encoding utf8 -LiteralPath $schemaPath
    $registryText = Get-Content -Raw -Encoding utf8 -LiteralPath $registryPath
    if (-not ($registryText | Test-Json -Schema $schemaText -ErrorAction SilentlyContinue)) {
        Add-ValidationError 'Identity registry failed its JSON Schema.'
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

$layerSummary = $registry.agents | Group-Object layer | Sort-Object Name |
    ForEach-Object { "$($_.Name)=$($_.Count)" }
Write-Output "Agent framework validation passed: agents=$($registry.agents.Count); $($layerSummary -join '; ')"
