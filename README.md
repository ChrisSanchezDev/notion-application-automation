# **HomeLab: notion-application-automation**

As apart of my collection of **Homelab** projects, this project's goal is to automate specific tasks for my Application Tracker on Notion. Currently, there are two automated tasks that occur, all of which is happening on my Raspberry Pi 4 at home.

### Scripts:
* **daily_icon_swap.py (Daily at 00:00)**
  * Every day at midnight, the icons on all my applications will update with an educated guess towards the proper logo for the company I'm applying for.
* **weekly_audit.py (Weekly at 00:00 Sunday)**
  * Weekly, all my applications will be checked on whether or not there's been 60+ days since I originally applied to them, and if so, it'll automatically label it's current response as "Past 2+ Months".
