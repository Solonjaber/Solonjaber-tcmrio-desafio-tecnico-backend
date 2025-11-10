# Script PowerShell para testar a API
$baseUrl = "http://localhost:8000/api/v1"

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "TESTE DE INTEGRAÇÃO API" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# 1. Login
Write-Host "`n[1/3] Testando login..." -ForegroundColor Yellow
$loginBody = @{
    username = "admin"
    password = "admin123"
}
$loginResponse = Invoke-RestMethod -Uri "$baseUrl/auth/login" -Method Post -Body $loginBody -ContentType "application/x-www-form-urlencoded"
$token = $loginResponse.access_token
Write-Host "✅ Login bem-sucedido!" -ForegroundColor Green
Write-Host "Token: $($token.Substring(0,50))..." -ForegroundColor Gray

# 2. Busca Semântica
Write-Host "`n[2/3] Testando busca semântica..." -ForegroundColor Yellow
$searchBody = @{
    query = "Cleverton"
    top_k = 2
} | ConvertTo-Json

$headers = @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
}

$searchResponse = Invoke-RestMethod -Uri "$baseUrl/search/" -Method Post -Body $searchBody -Headers $headers
Write-Host "✅ Busca bem-sucedida!" -ForegroundColor Green
Write-Host "Query: $($searchResponse.query)" -ForegroundColor Gray
Write-Host "Total de resultados: $($searchResponse.total_results)" -ForegroundColor Gray
if ($searchResponse.results.Count -gt 0) {
    Write-Host "Primeiro resultado: $($searchResponse.results[0].document_name)" -ForegroundColor Gray
    Write-Host "Similarity: $($searchResponse.results[0].similarity_score)" -ForegroundColor Gray
}

# 3. Chat
Write-Host "`n[3/3] Testando chat..." -ForegroundColor Yellow
$chatBody = @{
    query = "qual o conteúdo do documento?"
    use_context = $true
    max_context_chunks = 2
} | ConvertTo-Json

$chatResponse = Invoke-RestMethod -Uri "$baseUrl/chat/" -Method Post -Body $chatBody -Headers $headers
Write-Host "✅ Chat bem-sucedido!" -ForegroundColor Green
Write-Host "Query: $($chatResponse.query)" -ForegroundColor Gray

# VERIFICAÇÃO CRÍTICA: Campo renomeado
if ($chatResponse.PSObject.Properties.Name -contains "llm_provider") {
    Write-Host "✅ Campo 'llm_provider' presente: $($chatResponse.llm_provider)" -ForegroundColor Green
} else {
    Write-Host "❌ Campo 'llm_provider' AUSENTE!" -ForegroundColor Red
}

if ($chatResponse.PSObject.Properties.Name -contains "model_used") {
    Write-Host "⚠️  Campo antigo 'model_used' ainda presente!" -ForegroundColor Yellow
}

Write-Host "Contexto usado: $($chatResponse.context_used.Count) chunks" -ForegroundColor Gray
Write-Host "Resposta: $($chatResponse.answer.Substring(0, [Math]::Min(100, $chatResponse.answer.Length)))..." -ForegroundColor Gray

Write-Host "`n====================================" -ForegroundColor Cyan
Write-Host "TESTES CONCLUÍDOS COM SUCESSO!" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
