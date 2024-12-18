# SMTP2Go Mail Usage Check Plugin for Icinga2

## Features

- **Real-time usage check:** Fetches the current mail usage from the SMTP2Go API
- **Configurable thresholds:** Set custom warning and critical percentage thresholds
- **Performance data output:** Returns Icinga-compatible performance data for both absolute mail usage and percentage utilization

## Requirements

- **Python 3**  
- **requests** Python library (install with `pip install requests`)

## Installation

1. Make sure Python 3 is installed on your monitoring server
2. Install the `requests` library if not already present:  
   ```
   pip3 install requests 
   ```
3. Download or clone this repository and place the script in the plugins folder
   ```
   git clone https://github.com/StratoGh0st99/check_smtp2go_usage.git
   cd check_smtp2go_usage
   cp check_smtp2go_usage.py /usr/lib/nagios/plugins/
   ```
4. Make the script executable.
   ```
   chmod +x /usr/lib/nagios/plugins/check_smtp2go_quota.py
   ```

## Usage

### Test your API credentials
   ```
   ./check_smtp2go_quota.py --api-key YOUR_API_KEY --warn 80 --crit 90
   ```
### Parameters
**-a / --api-key (required):** Your SMTP2Go API key

**-w / --warn (required):** Warning threshold in percent (e.g. 80 for 80%)

**-c / --crit (required):** Critical threshold in percent (e.g. 90 for 90%)

### Example Output
```
OK - 200 of 1000 mails used (20.00%) | mails_used=200;800;900;0;1000 usage_percent=20.00%;80;90;0;100
```

## Integrate in Icinga2
1. Define the CheckCommand in Icinga2
   ```
   object CheckCommand "check_smtp2go_quota" {
     import "plugin-check-command"
     command = [ "/usr/lib/nagios/plugins/check_smtp2go_quota.py" ]
     arguments = {
       "--api-key" = "$smtp2go_api_key$"
       "--warn" = "$smtp2go_warn$"
       "--crit" = "$smtp2go_crit$"
       }
   }
   ```
2. Apply the service to a host
   ```
   apply Service "smtp2go-quota" {
     import "generic-service"
     check_command = "check_smtp2go_quota"
     vars.smtp2go_api_key = "YOUR_API_KEY"
     vars.smtp2go_warn = "80"
     vars.smtp2go_crit = "90"
     assign where host.name == "myhost"
     }
   ```
3. Reload Icinga2
   ```
   systemctl reload icinga2
   ```
