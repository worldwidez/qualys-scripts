powershell_script 'Uninstall Qualys Agent' do
  code <<-EOH
    $qualys_agents = Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Qualys Agent*"}
    foreach ($agent in $qualys_agents) {
      $agent.Uninstall()
    }
  EOH
end
