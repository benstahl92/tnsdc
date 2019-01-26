# tnsdc --- TNS Discovery Checker

A lightweight package for retrieving TNS discoveries and sending alerts.

## Description

Downloads information from TNS on discoveries announced within a specied number of days (default is 2), collects additional data, and then organizes it into a simple file. Entries that are new are then posted to a Slack channel using WebHooks. It is intended to run daily using a cron job.

## Installation

1. Download tnsdc

   ```sh
   git clone https://github.com/benstahl92/tnsdc
   ```

2. Run setup script

   ```sh
   # from with tnsdc root directory
   python setup.py install
   ```

## Usage

tnsdc is intended to be used through the script ```tns_check```. The only mandatory argument is the name of the file serving as the database (it will be built if it does not exist). By throwing the ```-b``` flag an optional argument giving the number of previous days to download can be specified.

* Note: ```tns_check``` expects a file named `slack.webhook` to exist. This file should contain only the url given after setting up the Slack App called `Incoming Web Hooks`.
