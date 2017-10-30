# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "ban"
app_title = "Ban"
app_publisher = "BAN"
app_description = "Extension untuk BAN"
app_icon = "octicon octicon-book"
app_color = "grey"
app_email = "cahyadi.suwindra@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ban/css/ban.css"
# app_include_js = "/assets/ban/js/ban.js"

# include js, css files in header of web template
# web_include_css = "/assets/ban/css/ban.css"
# web_include_js = "/assets/ban/js/ban.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "ban.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ban.install.before_install"
# after_install = "ban.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ban.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
     "Sales Order": {
	 "validate": "ban.api.test"
     },
     "user": {
         "validate": "ban.api.test"
     },	
     "Production Order": {
         "validate": "ban.api.check_batch",
         "on_submit": "ban.api.production_order_on_submit"
     },
	 "Stock Entry": {
	     "before_save": "ban.api.calc_rate"
	 }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ban.tasks.all"
# 	],
# 	"daily": [
# 		"ban.tasks.daily"
# 	],
# 	"hourly": [
# 		"ban.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ban.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ban.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ban.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ban.event.get_events"
# }

