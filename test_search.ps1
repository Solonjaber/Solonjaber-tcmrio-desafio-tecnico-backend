# Teste de busca semântica com diferentes queries
$baseUrl = "http://localhost:8000/api/v1"

# Login
$loginBody = @{
    username = "admin"
    password = "admin123"
}
$loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method Post -Body $loginBody -ContentType "application/x-www-form-urlencoded"
$token = $loginResponse.access_token

$headers = @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
}

# Testar diferentes queries
$queries = @(
    "profissional",
    "experiência",
    "TI tecnologia",
    "suporte técnico",
    "datacenters"
)

Write-Host "Testando busca semântica com diferentes queries:" -ForegroundColor Cyan
Write-Host "=" * 60

foreach ($query in $queries) {
    Write-Host "`nQuery: '$query'" -ForegroundColor Yellow

    $searchBody = @{
        query = $query
        top_k = 2
    } | ConvertTo-Json

    try {
        $searchResponse = Invoke-RestMethod -Uri "$baseUrl/search/" -Method Post -Body $searchBody -Headers $headers
        Write-Host "  Resultados: $($searchResponse.total_results)" -ForegroundColor $(if ($searchResponse.total_results -gt 0) {"Green"} else {"Red"})

        if ($searchResponse.total_results -gt 0) {
            $firstResult = $searchResponse.results[0]
            Write-Host "  Doc: $($firstResult.document_name)" -ForegroundColor Gray
            Write-Host "  Similarity: $([math]::Round($firstResult.similarity_score, 4))" -ForegroundColor Gray
            Write-Host "  Trecho: $($firstResult.chunk_text.Substring(0, [Math]::Min(100, $firstResult.chunk_text.Length)))..." -ForegroundColor Gray
        }
    } catch {
        Write-Host "  Erro: $_" -ForegroundColor Red
    }
}

Write-Host "`n" + ("=" * 60)
