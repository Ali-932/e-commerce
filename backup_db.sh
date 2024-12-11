#!/bin/bash

python ./manage.py dbbackup --exclude-tables='auth_group, account_user, account_user_groups, account_user_user_permissions, account_user_user_permissions,auth_group, auth_group_permissions, auth_permission, django_admin_log,django_session, taggit_tag, taggit_taggeditem, silk_request, silk_sqlquery,silk_response, order_order, order_orderitem, order_shippingaddress'