# up_image
Takes in a list of domains and then takes a screenshot of each one's website.

### Use:
Create a file with a list of domains on each line.  Theoretically IPs should work, however CIDr and IP range notation will not. *Do not include URL syntax*.  This means no "http" or slashes "/"

python3 main.py <list_of_domains_file.txt>

Input a name for this run.  Images will be placed into this directory sorted by what the return code was (2xx, 4xx, 5xx)

This requires Selenium.  The code uses Firefox, so you'll need to get and install the Gecko driver.
https://www.selenium.dev/documentation/webdriver/getting_started/install_library/

For Ubuntu users, Firefox is installed with Snap on recent versions, which causes issues with Selenium.  To fix this, uninstall Firefox with Snap and then install it using either a Deb downloaded from Firefox's website or follow the following link to install via apt:
https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04

This has been tested on Ubuntu 22.04.3 LTS
