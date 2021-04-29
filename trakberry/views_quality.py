from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from trakberry.forms import maint_closeForm, maint_loginForm, maint_searchForm, tech_loginForm, sup_downForm
from views_db import db_open, db_set
from views_mod1 import find_current_date
from views_mod2 import seperate_string, create_new_table,generate_string
from views_email import e_test
from views_vacation import vacation_temp, vacation_set_current, vacation_set_current2, vacation_set_current9
from views_supervisor import supervisor_tech_call
from views_maintenance import login_password_check
from trakberry.views_testing import machine_list_display
from mod1 import hyphon_fix, multi_name_breakdown
import MySQLdb
from trakberry.views_vacation import vacation_temp, vacation_set_current, vacation_set_current2
import time
import datetime 
from django.core.context_processors import csrf


