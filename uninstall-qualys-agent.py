# Get all Qualys agents installed on the system
$qualys_agents = Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Qualys*"}

# Uninstall all Qualys agents
foreach ($agent in $qualys_agents) {
    $agent.Uninstall()
}
