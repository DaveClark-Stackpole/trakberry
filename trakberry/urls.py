
"""trakberry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""


from django.conf.urls import include, url
from django.contrib import admin


from views2 import main_login, main_login_form, main, main_logout, switch_local, switch_net, main_test_init, main_login_password_lost_form
from views_machinery import machinery
from views_testing import test_display, form_robot_machine_enter, display_robot_machine, machine_list_display, toggletest, test668,create_table_1,test_datalist
from views_tech import tech, job_call, job_close, tech_logout, job_pass, tech_history, tech_history2, tech_recent, tech_recent2, tech_map, t1_call, reset_call_route,tech_email_test,tech_message, modal_test
from views_tech import tech_message_close,tech_message_reply1, tech_report_email, email_hour_check,tech_name_update
from views_tech import tech_epv,tech_epv_back,tech_epv_complete, tech_epv_person_update,tech_epv_assign,tech_PM_assign,tech_epv_week_assign
from views_tech import epv_checks_update
from views_tech import tech_pm, tech_pm_back,tech_pm_complete,tech_PM_master_complete,tech_pm_complete_all,tech_pm_summary, tech_pm_complete_asset
from views_tech import changeover1
#from views_tech import hour_check
from views_transfer import transfer

from mod_simulate import sim
from mod_tracking import edit_part, select_date, select_day, select_datetime, graph_gf6, graph_gf6_report
from mod_test import test_mode
from views_global_mods import test_machine_rate
from views_vacation import vacation_temp, vacation_backup, vacation_purge, vacation_purge_delete, vacation_rebuild,vacation_restore, message_create
from views_vacation import scrap_backup,scrap_restore
from views_admin import retrieve,master2
from views_db import db_select
from views_test import place_test, email_test_1, email_test_2
from views_mod1 import table_copy
from views_vacation import duplicate_1,create_table_1

# *******************************************  Testing Views *******************************************************************************************
from views_email import e_test
from views import fix_time
from views_test import test_list, toggle_1, layer_test, layer_entry, layer_transfer_temp, layer_choice_init, layer_choice, layer_select, layer_audit_check_reset
from views_test import layer_retrieve,sup_mess, test_scrap1
from views_test_email import email1, done_email_1
from views_testing import clear_login
from views_test import create_scrap_table, test_scrap_production, test_update_blue, test_update_yellow, test_update_red
from test_test import table_mod1
from view_test1 import kiosk_name,update_column
from mod_test import wildcard_test
from views_test2 import machine1, prediction1

from views_manpower import manpower_allocation
from views_test1 import balancer_1508

from views_production import update7,update7_prev
# ***********************************************************************************************************************************************************


# *******************************************  Main Views *******************************************************************************************
from views import display, db_write, create_table, test, details_session, details_track, reports, test_time, scheduler, inventory, display2, fade_in, fade2
from views import create_test_table, alter_table_name, done, new, graph, graph2, graph3, graph749, graph748, graph750, graph677, ttip,graph_close, display_time, graph_close_snap
from views import graph677_snap, graph748_snap, graph749_snap, graph750_snap, display_initialize, test44, tech_reset,testB
from views2 import main_password_update, password_edit_form, main_message_form,switch_history
from views3 import excel_test,manpower_update, request_test, scrapdate_fix1
# ***********************************************************************************************************************************************************


# *******************************************  Supervisor Section ********************************************************************************************
from views_supervisor import supervisor_display, supervisor_tech_call,supervisor_elec_call,supervisor_maint_call,sup_message_close
from views_supervisor import vacation_display_jump, supervisor_edit, sup_close, employee_vac_enter, vacation_display
from views_supervisor import vacation_display_increment, vacation_display_decrement, vacation_edit, vacation_delete, sup_message_reply1,sup_message_reply0
from views_supervisor import employee_vac_enter_init, employee_vac_enter_init2, vacation_month_fix, vacation_display_initial, resetcheck,sup_message
from views_supervisor import check_email_problem, supervisor_down_no,supervisor_down_yes,supervisor_schedule
from views_supervisor import trainer,trainer_initialize,press_changeover_enter,press_changeover_start,press_changeover_setup,press_changeover_complete,press_changeover_delete,press_changeover_comment
# ***********************************************************************************************************************************************************


# *******************************************  Employee Section ********************************************************************************************
from views_employee import create_matrix, emp_training_enter, emp_info_enter, emp_info_display, emp_matrix_initialize, create_jobs,emp_info_update_status
from views_employee import job_info_display, job_info_enter,matrix_info_init, matrix_update, fix_shift,matrix_info_display,matrix_info_reload,matrix_backup,rot_fix
from views_employee import job_info_update_status, job_info_delete, matrix_job_test, emp_matrix_delete, emp_matrix_rotation_fix, employee_manual_enter, emp_info_group_update
from views_employee import emp_info_absent, emp_info_enter_manual
from views_scheduler import current_schedule, set_rotation, rotation_info_display, rotation_update, schedule_set, schedule_set2, schedule_init,schedule_finalize
from views_scheduler import schedule_set2b,schedule_set3,schedule_reset_data,schedule_redisplay1, schedule_rotation_start

# ***********************************************************************************************************************************************************

# *******************************************  Maintenance App Section ********************************************************************************************
from views_maintenance import maint_mgmt,maint, maint_call, maint_pass, maint_close, maint_logout, maint_job_history, maint_map, maint_call_call
from views_maintenance import maint_mgmt_login_form, maintenance_edit, maintenance_close, maint_close_item, maint_job_entry, maint_mgmt_auto, maint_TV
from views_maintenance import maint_init_call,maint_down_yes,maint_down_no,maint_job_close

# ***********************************************************************************************************************************************************

# *******************************************  Inventory Section ********************************************************************************************
from views_inventory import push_button, inventory_type_entry, inventory_entry, inventory_fix

# ***********************************************************************************************************************************************************

# *******************************************  Kiosk Section ********************************************************************************************
from views_kiosk import kiosk,kiosk_job,kiosk_job_assign, kiosk_job_leave,kiosk_error_badjobnumber,kiosk_error_badclocknumber,kiosk_error_assigned_clocknumber
from views_kiosk import kiosk_production, kiosk_production_entry,flex_test,manual_production_entry,manual_production_entry2
from views_kiosk import entry_recent, manual_cycletime_table, tenr_fix2, tenr_fix3,kiosk_hourly_entry,kiosk_initial_9HP,kiosk_initial_6L_Output
from views_kiosk import kiosk_initial_GF9,kiosk_initial_6L_IN,kiosk_initial_AB1V, kiosk_sub_menu, kiosk_manual, kiosk_kiosk
from views_kiosk import kiosk_help_form, kiosk_forklift_form, kiosk_scrap, kiosk_scrap_entry, kiosk_scrap_reset #, kiosk_mult_entries
from views_kiosk import production_entry_check,kiosk_job_furnace,production_entry_fix,production_entry_fix_shift, production_entry_check_manual
from views_kiosk import test_1_10R,down_10r,down_10r_entry,down_10r_asset_check,down_10r_entry2,tech_down_10r,down_10r_fix,redirect_down_10r_fix
from views_kiosk import tech_down_10r_displayset, tech_down_10r_mobileset,tech_10r_login,tech_10r_logout,down_10r_fix_assign

# ***********************************************************************************************************************************************************
# *******************************************  Manpower Section ********************************************************************************************
from views_kiosk import manpower_layout, tenr_fix,kiosk_menu,ab1v_manpower,tenr1,trilobe,tenr2, error_hourly_duplicate
from views_kiosk import kiosk_production_write
from views_kiosk import set_test1, kiosk_fix55, kiosk_fix44, kiosk_help_close, kiosk_epv_verification, kiosk_epv_entry, production_entry_cleanup
from views_manpower import manpower_allocation_interval_pick

# ***********************************************************************************************************************************************************

# ***********************************************************************************************************************************************************
# *******************************************  Shipping Section ********************************************************************************************
from views_shipping import forklift, forklift_login_form, forklift_logout, forklift_close, forklift_close_item
# ***********************************************************************************************************************************************************

# *******************************************  Management Section ********************************************************************************************
from views_production import mgmt,mgmt_login_form,mgmt_logout,mgmt_production_hourly,mgmt_production_hourly_edit, mgmt_production, mgmt_display_edit, mgmt_cycletime
from views_production import mgmt_production_counts
from views_production import mgmt_users_logins, mgmt_users_logins_edit, mgmt_users_logins_update, mgmt_users_logins_add, mgmt_users_logins_add_new
from views_production import mgmt_test1,track_10r_data,tracking,track_graph_10r_prev,track_graph_tri_prev, track_graph_prev1,track_graph_prev2,track_graph_track,track_graph_8670
from views_production import chart1_1467,chart2_1467,chart1_3050,chart2_3050,chart1_0455,chart2_0455,chart1_9341,chart2_9341
from views_production import chart1_0455_OP30,chart2_0455_OP30,track_1703
from views_production import chart1_1502, chart2_1502, chart1_1507, chart2_1507, chart1_1539, chart2_1539
from views_production import chart1_9341_OP30, chart2_9341_OP30, tracking_10R80, tracking_10R80_screen, tracking_10R80_resume
from views_production import chart1_9341_OP80, chart2_9341_OP80, chart1_9341_OP110, chart2_9341_OP110
from views_production import chart1_5214_OP30, chart2_5214_OP30, chart1_8670_OP80, chart2_8670_OP80, chart1_5404_OP80, chart2_5404_OP80
from views_production import chart1_5401_OP80, chart2_5401_OP80, chart1_3214_OP30, chart2_3214_OP30,chart1_5710,chart2_5710
from views_production import chart1_1467b,chart2_1467b,chart1_3050b,chart2_3050b,chart1_5710b,chart2_5710b
from views_production import chart1_1467o,chart2_1467o,chart1_1467br,chart2_1467br,chart1_0455_OP50,chart2_0455_OP50,chart1_0455_OP40,chart2_0455_OP40
from views_production import mgmt_priorities,auto_updater,cell_track_9341,track_email,cell_track_9341_mobile,cell_track_9341_history_on,cell_track_9341_history
from views_production import cell_track_9341_history_off,mgmt_track_week,mgmt_goals,cell_track_9341_TV,track_1703_initial,track_1704_initial,cell_track_9341_v2
from views_production import cell_track_1467,cell_track_8670,cell_track_9341_history2,track_9341_history_date,cell_track_9341_NEW,cell_9341_mobile,cell_9341_screen
from views_production import plus_0455,minus_0455,plus_9341,minus_9341,plus_3050,minus_3050,plus_1467,minus_1467, wip_update,runrate_10R80,cell_track_9341_archive

from views_operations import gf6_reaction,gf6_input,gf6_reaction_prev,gf6_input_prev,prod_9341,prod_10R,prod_10R_prev, prod_728,prod_728fault,prod_728fault_prev
from views_operations import test_email_7,prod_10R_initial, prod_ab1v, prod_ab1v_initial, prod_ab1v_prev, prod_ab1v_reaction, prod_ab1v_reaction_prev
from views_operations import track_single, live_10R,live_update1,prod_counts1,prod_counts2,hourly_counts
from views_operations import pareto_test,downtime_month_selection,downtime_category_selection,downtime_category_history



from views4 import ios_test, IsDone, NotDone, target_fix1, medium_production, multidrop, scantest, target_fix1
from views4 import target_fix_5401, target_fix_5404, target_fix_5399, target_fix_5214, target_fix_3214
from views_mod1 import mgmt_display_next,mgmt_display_prev

from mod1 import index_template,track_10r

from views_mod2 import hrly_display, butter
from views_barcode import barcode_check, barcode_input, barcode_initial, barcode_reset, barcode_search, barcode_search_check, barcode_verify, barcode_verify_check
from views_barcode import barcode_check_10R,barcode_input_10R,barcode_initial_10R, barcode_wrong_part, barcode_count, barcode_wrong_part2, barcode_wrong_part_reset

# ***********************************************************************************************************************************************************

# *******************************************  Admin Section ********************************************************************************************
from views_admin import master
from views3 import excel_dump, excel_scrap_dump,training_matrix2,training_matrix_find,training_matrix_update_all
from views3 import bounce_matrix,update_matrix_cancel,matrix_cache_matrix, full_update
from views_admin import tech_pm_add,manpower_calculation
from views_healthsafety import temp_display,temp_test1,temp_test_reset,temp_ack,temp_ack_taken
# ***********************************************************************************************************************************************************

# *******************************************  Scrap Section ********************************************************************************************
from views_scrap import scrap_mgmt, scrap_mgmt_login_form,scrap_display,scrap_display_operation,scrap_display_category,scrap_entries,scrap_display_category_shift
from views_scrap import scrap_entries_next, scrap_entries_prev,scrap_entries_update,scrap_display_date_pick,scrap_display_24hr,operation_department,oper_dept_edit_selection,operation_entries_next, operation_entries_prev,operation_entries_update,kiosk_add_category,kiosk_initiate
from views_scrap import scrap_display_entry_edit,scrap_edit_categories_reset,scrap_edit_categories,scrap_edit_categories_entry
from views_scrap import tpm_display,scrap_edit_categories_delete,scrap_edit_categories_newentry,scrap_edit_categories_save
from views_scrap import gate_alarm_list,gate_alarm_list_add,gate_alarm_list_edit, gate_alarm_list_del, gate_alarm_list_hide, gate_alarm_list_show
from views_scrap import gate_alarm_list_add_initial
# ***********************************************************************************************************************************************************

# *******************************************  Quality Section ********************************************************************************************
from views_quality import pie_chart,sup_pie_chart,quality_epv_asset_entry, initial_epv, previous_epv, next_epv, epv_cleanup
from views_quality import gate_alarm_champion,gate_alarm_champion_initial
# 

# *******************************************  Manpower Section ********************************************************************************************
from views_manpower import manpower_update_v2, training_matrix3, matrix_update_v2, training_performance
from views_manpower import trained_email
# ***********************************************************************************************************************************************************

# *******************************************  HR Section ********************************************************************************************
from views_hr import hr,hr_login_form,hr_down
from views_hr import productline_dl,date_picker_productline,production_OA,date_picker_production_OA,production_OA_24hrs
# ***********************************************************************************************************************************************************


# *******************************************  Machinery ********************************************************************************************
from views_machinery import downtime_category_enter
from views_machinery import downtime_category
# *


urlpatterns = [
	url(r'^admin/', include(admin.site.urls)),
	
	# May 26,2015
	# Path for Test of single direct live tracking and then 
	# link to display.html template
	url(r'^$',main),
#part_entries,kiosked_scrap_entry,part_entries_next,part_entries_prev,part_entries_update,
	
	url(r'^display/', main),
	url(r'^testB/', testB),
	url(r'^main_login/', main_login),
	url(r'^main_logout/', main_logout),
	url(r'^main_login_password_lost_form/', main_login_password_lost_form),
	url(r'^switch_local/', switch_local),
	url(r'^switch_net/', switch_net),
	url(r'^switch_history/', switch_history),
	url(r'^main_login_form/', main_login_form),
	url(r'^display1/', display),
	url(r'^display_initialize/', display_initialize),
	url(r'^display2/', display2),
	url(r'^test6/', test_display),
	url(r'^test668/', test668),
	url(r'^create/', test),
	url(r'^new/', new),
	url(r'^display_time/', display_time),
	url(r'^tmr/', test_machine_rate),
	url(r'^fix_shift/', fix_shift),
	url(r'^sup_message_close/', sup_message_close),
	url(r'^fade/', fade_in),
	url(r'^fade2/', fade2),
	url(r'^ttip/', ttip),
	url(r'^graph_gf6op/get/(?P<index>\d+)/$', graph_gf6),
	url(r'^graph_gf6_report/get/(?P<index>\w{0,50})/$', graph_gf6_report),
	#url(r'^graph_gf6_report/get/(?P<index>\d+)/$', graph_gf6_report),
	url(r'^graph/', graph),
	url(r'^graph2/', graph2),
	url(r'^graph3/', graph3),
	url(r'^db_write/', db_write),  
	url(r'^sim/', sim),	
	url(r'^test/', test),
	url(r'^sup_mess/', sup_mess),	
	url(r'^done/', done),
	url(r'^details_session/', details_session),
	url(r'^details_track/', details_track),
	url(r'^main/', main),
	url(r'^tech_reset/', tech_reset),
	url(r'^tech_email_test/', tech_email_test),
	url(r'^done_email_1/', done_email_1),
	url(r'^tech_message_close/', tech_message_close),
	url(r'^tech_message_reply1/', tech_message_reply1),
	url(r'^tech_epv_person_update/', tech_epv_person_update),
	url(r'^email_hour_check/', email_hour_check),
	url(r'^modal_test/', modal_test),

	url(r'^trainer/', trainer),
    url(r'^trainer_initialize/', trainer_initialize),
    url(r'^press_changeover_enter/', press_changeover_enter),
	url(r'^press_changeover_start/get/(?P<index>\d+)/$', press_changeover_start),
	url(r'^press_changeover_setup/get/(?P<index>\d+)/$', press_changeover_setup),
    url(r'^press_changeover_complete/get/(?P<index>\d+)/$', press_changeover_complete),
    url(r'^press_changeover_delete/get/(?P<index>\d+)/$', press_changeover_delete),
    url(r'^press_changeover_comment/get/(?P<index>\d+)/$', press_changeover_comment),
   

    	

	
	
	# Reports URL Patterns ***********************************
	url(r'^reports/', select_date),
	url(r'^reports_day/', select_day),
	url(r'^reports_snapshot/', select_datetime),
	# ********************************************************
	
	# Reports URL Patterns for Vacations ***********************************
	url(r'^employee_vacation_enter/', employee_vac_enter),
	url(r'^employee_vacation_enter_init2/', employee_vac_enter_init2),
	url(r'^employee_vacation_enter_init/get/(?P<index>\d+)/$', employee_vac_enter_init),
	url(r'^emp_matrix_rotation_fix/', emp_matrix_rotation_fix),
	url(r'^employee_manual_enter/', employee_manual_enter),
	url(r'^emp_info_enter_manual/', emp_info_enter_manual),
	url(r'^emp_info_group_update/', emp_info_group_update),
	url(r'^matrix_backup/', matrix_backup),
	url(r'^vacation_display/', vacation_display),
	url(r'^vacation_display_jump/', vacation_display_jump),
	url(r'^vacation_display_increment/', vacation_display_increment),
	url(r'^vacation_display_decrement/', vacation_display_decrement),
	url(r'^vacation_edit/get/(?P<index>\d+)/$', vacation_edit),
	url(r'^vacation_delete/', vacation_delete),
	url(r'^vacation_display_initial/', vacation_display_initial),
	url(r'^vacation_backup/', vacation_backup),
	url(r'^message_create/', message_create),
	url(r'^vacation_rebuild/', vacation_rebuild),
	url(r'^vacation_restore/', vacation_restore),
	url(r'^vacation_purge/', vacation_purge),
	url(r'^vacation_purge_delete/', vacation_purge_delete),
	url(r'^vacation_month_fix/', vacation_month_fix),
	url(r'^resetcheck/', resetcheck),
	url(r'^duplicate_1/', duplicate_1),
	url(r'^create_table_1/', create_table_1),
	# ********************************************************	
	
	url(r'^machinery/', machinery),
	url(r'^test_time/', test_time),
	url(r'^scheduler/', scheduler),
	url(r'^inventory/', inventory),
	url(r'^testdb/', create_test_table),
	url(r'^edit/', edit_part),
	url(r'^create_table_1/', create_table_1),
	url(r'^test44/', test44),
	url(r'^graph_gf6/get/(?P<index>\w{0,50})/$', graph_gf6),
	url(r'^check_email_problem/', check_email_problem),
	#url(r'^graph_gf6/get/(?P<index>\d+)/$', graph_gf6),
	url(r'^graph749/', graph749),
	url(r'^graph748/', graph748),
	url(r'^graph750/', graph750),
	url(r'^graph677_snap/', graph677_snap),
	url(r'^graph748_snap/', graph748_snap),
	url(r'^graph749_snap/', graph749_snap),
	url(r'^graph750_snap/', graph750_snap),
	url(r'^graph677/', graph677),
	url(r'^graph_close/', graph_close),
	url(r'^graph_close_snap/', graph_close_snap),
	url(r'^test_var/', test_mode),
	url(r'^tech/', tech),
	url(r'^sup/', supervisor_display),
	url(r'^sup_down_tech/', supervisor_tech_call),
	url(r'^sup_close/', sup_close), 
	url(r'^transfer/', transfer),
	url(r'^reset_call_route/', reset_call_route),
	url(r'^sup_down_elec/', supervisor_elec_call),
	url(r'^sup_down_maint/', supervisor_maint_call),
	url(r'^supervisor_down_no/', supervisor_down_no),
	url(r'^supervisor_down_yes/', supervisor_down_yes),
	url(r'^sup_message_reply1/', sup_message_reply1),
	url(r'^sup_message_reply0/', sup_message_reply0),
	url(r'^sup_message/', sup_message),
	url(r'^supervisor_schedule/', supervisor_schedule), 
	#url(r'^sup_down_main/', supervisor_main_call),
	#url(r'^sedit/get/(?P<index>\d+)/$', supervisor_edit),
	url(r'^sedit/', supervisor_edit),
	url(r'^alter/', alter_table_name),
	url(r'^tech_logout/', tech_logout),
	url(r'^tech_down_10r/', tech_down_10r),
	url(r'^jcall/get/(?P<index>\d+)/$', job_call),
	url(r'^jclose/get/(?P<index>\d+)/$', job_close),
	url(r'^changeover1/get/(?P<index>\d+)/$', changeover1),
	url(r'^jpass/get/(?P<index>\d+)/$', job_pass),
	url(r'^tech_epv/get/(?P<index>\w{0,50})/$', tech_epv),
	url(r'^tech_pm/get/(?P<index>\w{0,50})/$', tech_pm),
	url(r'^tech_epv_complete/get/(?P<index>\w{0,50})/$', tech_epv_complete),
	url(r'^tech_pm_complete/get/(?P<index>\w{0,50})/$', tech_pm_complete),
	url(r'^tech_pm_complete_asset/get/(?P<index>\w{0,50})/$', tech_pm_complete_asset),
	url(r'^tech_pm_complete_all/', tech_pm_complete_all),
	url(r'^tech_epv_back/', tech_epv_back),
	url(r'^tech_pm_back/', tech_pm_back),
	url(r'^tech_history/', tech_history),
	url(r'^tech_history2/', tech_history2),
	url(r'^tech_recent/', tech_recent),
	url(r'^tech_recent2/', tech_recent2),
	url(r'^t1_call/', t1_call),
	url(r'^tech_map/', tech_map),
	url(r'^tech_message/', tech_message),	
	url(r'^tech_report_email/', tech_report_email),
	url(r'^tech_name_update/', tech_name_update),
	url(r'^tech_epv_assign/', tech_epv_assign),
	url(r'^tech_PM_assign/', tech_PM_assign),
	url(r'^tech_PM_master_complete/', tech_PM_master_complete),
	url(r'^tech_epv_week_assign/', tech_epv_week_assign),
	url(r'^tech_pm_summary/', tech_pm_summary),
	url(r'^redirect_down_10r_fix/', redirect_down_10r_fix),
	url(r'^tech_down_10r_mobileset/', tech_down_10r_mobileset),
	url(r'^tech_down_10r_displayset/', tech_down_10r_displayset),
	

	url(r'^tech_pm_summary/', tech_pm_summary),
	

	url(r'^epv_checks_update/', epv_checks_update),

	url(r'^main_password_update/', main_password_update),
	url(r'^main_message_form/', main_message_form),
	
	# **************  Maintenance Section ***************************************
	url(r'^maint_mgmt/', maint_mgmt),
	url(r'^maint_mgmt_auto/', maint_mgmt_auto),
	url(r'^maintenance_edit/', maintenance_edit),
	url(r'^maint_init_call/', maint_init_call),
	url(r'^maintenance_close/', maintenance_close),
	url(r'^maint_mgmt_login_form/', maint_mgmt_login_form),
	url(r'^maint_down_yes/', maint_down_yes),
	url(r'^maint_down_no/', maint_down_no),
	url(r'^maint/', maint),
	url(r'^maint_TV/', maint_TV),
	url(r'^maint_map/', maint_map),
	url(r'^mcall/get/(?P<index>\d+)/$', maint_call),
	url(r'^mclose/get/(?P<index>\d+)/$', maint_close),
	url(r'^mpass/get/(?P<index>\d+)/$', maint_pass),
	url(r'^maint_logout/', maint_logout),
	url(r'^maintenance/', maint_logout),
	url(r'^maint_job_history/', maint_job_history),
	url(r'^maint_call_call/', maint_call_call),
	url(r'^maint_close_item/', maint_close_item),
	url(r'^maint_job_entry/', maint_job_entry),
	url(r'^maint_job_close/', maint_job_close),
	url(r'^sup_pie_chart/', sup_pie_chart),
    url(r'^pareto_test/', pareto_test),
	
	
	# **************  Employee Section ***************************************
	url(r'^create_matrix/', create_matrix),
	url(r'^create_jobs/', create_jobs),
	url(r'^emp_training_enter/', emp_training_enter),
	url(r'^emp_info_delete/get/(?P<index>\w{0,50})/$', emp_info_update_status),
	url(r'^emp_info_absent/get/(?P<index>\w{0,50})/$', emp_info_absent),
	url(r'^emp_info_enter/', emp_info_enter),
	url(r'^rot_fix/', rot_fix),
	url(r'^emp_info_display/', emp_info_display),
	url(r'^emp_matrix_delete/', emp_matrix_delete),
	url(r'^emp_matrix_initialize/', emp_matrix_initialize),
	url(r'^emp_matrix_rotation_fix/', emp_matrix_rotation_fix),
	url(r'^job_info_delete/', job_info_delete),
	url(r'^job_info_display/', job_info_display),
	url(r'^job_info_enter/', job_info_enter),
	url(r'^job_info_update_status/get/(?P<index>\w{0,50})/$', job_info_update_status),
	url(r'^matrix_info_init/', matrix_info_init),
	url(r'^matrix_info_display/', matrix_info_display),
	url(r'^matrix_info_reload/', matrix_info_reload),
	url(r'^training_matrix/get/(?P<index>\d+)/$', matrix_update),
	url(r'^bounce_matrix/', bounce_matrix),
	url(r'^update_matrix_cancel/', update_matrix_cancel),
	url(r'^matrix_cache_matrix/', matrix_cache_matrix),
	
	url(r'^matrix_job_test/', matrix_job_test),
	url(r'^current_schedule/', current_schedule),
	url(r'^set_rotation/', set_rotation),
	url(r'^rotation_info_display/', rotation_info_display),
	url(r'^rotation_matrix/get/(?P<index>\d+)/$', rotation_update),

					# *******  Scheduling Section   **********
	url(r'^schedule_set/', schedule_set),
	url(r'^schedule_rotation_start/', schedule_rotation_start),
	url(r'^schedule_finalize/', schedule_finalize),
	url(r'^schedule_set2b/', schedule_set2b),
	url(r'^schedule_redisplay1/', schedule_redisplay1),
	#url(r'^schedule_add_job/get/(?P<index>\w{0,50})/$', schedule_add_job),
	#url(r'^tech/get/complete/(?P<index>\d+)/$', complete),
	url(r'^training_matrix2/', training_matrix3),
	url(r'^training_matrix_find/get/(?P<index>\w{0,50})/$', training_matrix_find),
	url(r'^training_matrix_update_all/', training_matrix_update_all),
	url(r'^full_update/', full_update),
	# ************************************************************************
	
	# **************  Testing Section ***************************************
	url(r'^wildcard_test/', wildcard_test),  
	url(r'^main_test_init/', main_test_init),   
	url(r'^email_test_1/', email_test_1),
	url(r'^email_test_2/', email_test_2),
	url(r'^email1/', email1),
	url(r'^target_fix1/', target_fix1),
	url(r'^target_fix_5401/', target_fix_5401),
	url(r'^target_fix_5404/', target_fix_5404),
	url(r'^target_fix_5399/', target_fix_5399),
	url(r'^target_fix_5214/', target_fix_5214),
	url(r'^target_fix_3214/', target_fix_3214),
	url(r'^multidrop/', multidrop),
	url(r'^scantest/', scantest),
	url(r'^ios_test/', ios_test),
	url(r'^medium_production/', medium_production),
	url(r'^IsDone/', IsDone),
	url(r'^NotDone/', NotDone),
	url(r'^form_robot_machine_enter/', form_robot_machine_enter),
	url(r'^display_robot_machine/', display_robot_machine),
	url(r'^machine_list_display/', machine_list_display),
	url(r'^e_test/', e_test),
	url(r'^db_select/', db_select),
	url(r'^place_test/', place_test),
	url(r'^schedule_init/', schedule_init),
	url(r'^schedule_set2/', schedule_set2),
	url(r'^schedule_set3/', schedule_set3),
	url(r'^schedule_reset_data/', schedule_reset_data),
	url(r'^table_copy/', table_copy),
	# Test for correcting timestamp issues on tracking data
	url(r'^fix_time/', fix_time),
	url(r'^test_list/', test_list),
	url(r'^test_datalist/', test_datalist),
	url(r'^toggle_1/', toggle_1),
	url(r'^layer_test/', layer_test),
	url(r'^layer_entry/', layer_entry),
	url(r'^layer_transfer_temp/', layer_transfer_temp),
	url(r'^layer_choice/', layer_choice),
	url(r'^layer_select/', layer_select),
	url(r'^layer_audit_check_reset/', layer_audit_check_reset),
	url(r'^layer_retrieve/get/(?P<index>\d+)/$', layer_retrieve),
	url(r'^clear_login/', clear_login),
	url(r'^create_scrap_table/', create_scrap_table),
	url(r'^test_scrap_production/', test_scrap_production),
	url(r'^test_scrap1/', test_scrap1),
	url(r'^excel_test/', excel_test),
	url(r'^manpower_update/', manpower_update),
	url(r'^table_mod1/', table_mod1),
	url(r'^kiosk_name/', kiosk_name),
	url(r'^update_column/', update_column),
	url(r'^request_test/', request_test),
#	url(r'^hour_check/', hour_check),
	url(r'^test_update_blue/', test_update_blue),
	url(r'^test_update_red/', test_update_red),
	url(r'^test_update_yellow/', test_update_yellow),
	url(r'^machine1/', machine1),
	url(r'^prediction1/', prediction1),

	url(r'^manpower_allocation/', manpower_allocation),

	url(r'^balancer_1508/', balancer_1508),

	# ************************************************************************
	
	# **************  Kiosk Section ***************************************
	url(r'^kiosk/', kiosk),
	url(r'^down_10r/', down_10r),
	url(r'^down_10r_entry/get/(?P<index>\d+)/$', down_10r_entry),
	url(r'^down_10r_asset_check/', down_10r_asset_check),
	url(r'^down_10r_entry2/', down_10r_entry2),
	url(r'^down_10r_fix/get/(?P<index>\d+)/$', down_10r_fix),

	url(r'^set_test1/', set_test1),
	url(r'^flex_test/', flex_test),
	url(r'^kiosk_job/', kiosk_job),
	url(r'^kiosk_production/', kiosk_production),
	url(r'^kiosk_job_assign/', kiosk_job_assign),
	url(r'^kiosk_error_badjobnumber/', kiosk_error_badjobnumber),
	url(r'^kiosk_error_badclocknumber/', kiosk_error_badclocknumber),
	url(r'^kiosk_error_assigned_clocknumber/', kiosk_error_assigned_clocknumber),
	url(r'^kiosk_job_leave/', kiosk_job_leave),
	url(r'^kiosk_production_entry/', kiosk_production_entry),
	url(r'^kiosk_hourly_entry/', kiosk_hourly_entry),
	url(r'^error_hourly_duplicate/', error_hourly_duplicate),
	url(r'^kiosk_menu/', kiosk_menu),
	url(r'^kiosk_sub_menu/', kiosk_sub_menu),
	url(r'^tenr1/', tenr1),
	url(r'^kiosk_fix55/', kiosk_fix55),
	url(r'^kiosk_fix44/', kiosk_fix44),
	url(r'^kiosk_manual/', kiosk_manual),
	url(r'^kiosk_kiosk/', kiosk_kiosk),
	url(r'^kiosk_scrap/', kiosk_scrap), # The Kiosk Scrap Module
	url(r'^kiosk_scrap_entry/', kiosk_scrap_entry),
	url(r'^kiosk_scrap_reset/', kiosk_scrap_reset), 
	url(r'^kiosk_epv_verification/', kiosk_epv_verification), 
	url(r'^kiosk_epv_entry/', kiosk_epv_entry), 
	url(r'^kiosk_production_write/', kiosk_production_write), 
	url(r'^scrap_backup/', scrap_backup),
	url(r'^scrap_restore/', scrap_restore),
	# url(r'^kiosk_mult_entries/', kiosk_mult_entries), 

	url(r'^kiosk_help_form/', kiosk_help_form),
	url(r'^kiosk_forklift_form/', kiosk_forklift_form),
	url(r'^kiosk_job_furnace/', kiosk_job_furnace),
	url(r'^production_entry_check/', production_entry_check),
	url(r'^production_entry_fix/', production_entry_fix),
	url(r'^production_entry_check_manual/', production_entry_check_manual),
	url(r'^production_entry_fix_shift/get/(?P<index>[\w|\W]+)', production_entry_fix_shift),

	url(r'^tenr2/', tenr2),
	url(r'^trilobe/', trilobe),
	url(r'^kiosk_initial_9HP/', kiosk_initial_9HP),
	url(r'^kiosk_initial_6L_Output/', kiosk_initial_6L_Output),
	url(r'^kiosk_initial_6L_IN/', kiosk_initial_6L_IN),
	url(r'^kiosk_initial_GF9/', kiosk_initial_GF9),
	url(r'^kiosk_initial_AB1V/', kiosk_initial_AB1V),
	url(r'^kiosk_help_close/', kiosk_help_close),
	url(r'^production_entry_cleanup/', production_entry_cleanup),
	url(r'^trilobe/', trilobe),
	url(r'^manual_production_entry/', manual_production_entry),
	url(r'^manual_production_entry2/', manual_production_entry2),
	url(r'^entry_recent/', entry_recent),
	url(r'^tenr_fix/', tenr_fix),
	url(r'^tenr_fix2/', tenr_fix2),
	url(r'^tenr_fix3/', tenr_fix3),
	url(r'^manual_cycletime_table/', manual_cycletime_table),
	url(r'^ab1v_manpower/', ab1v_manpower),

	url(r'^tech_10r_login/', tech_10r_login),
	url(r'^tech_10r_logout/', tech_10r_logout),
	url(r'^down_10r_fix_assign/', down_10r_fix_assign),






	# ************************************************************************
		# **************  Manpower Section ***************************************
	url(r'^manpower_layout/', manpower_layout),

	# ************************************************************************

		# **************  Shipping Section ***************************************
	url(r'^forklift/', forklift),
	url(r'^forklift_login_form/', forklift_login_form),
	url(r'^forklift_logout/', forklift_logout),
	url(r'^forklift_close/get/(?P<index>\d+)/$', forklift_close),
	url(r'^forklift_close_item/', forklift_close_item),
	# ************************************************************************

		# **************  Management Section ***************************************
	url(r'^mgmt/', mgmt),
	url(r'^mgmt_production_counts/', mgmt_production_counts),
	url(r'^mgmt_users_logins/', mgmt_users_logins),
	url(r'^mgmt_users_logins_update/', mgmt_users_logins_update),
	url(r'^mgmt_users_logins_edit/', mgmt_users_logins_edit),
	url(r'^mgmt_users_logins_add/', mgmt_users_logins_add),
	url(r'^mgmt_users_logins_add_new/', mgmt_users_logins_add_new),
	url(r'^mgmt_login_form/', mgmt_login_form),
	url(r'^mgmt_logout/', mgmt_logout),
	url(r'^mgmt_production_hourly/', mgmt_production_hourly),
	url(r'^mgmt_production/', mgmt_production),
	url(r'^mgmt_cycletime/', mgmt_cycletime),
	url(r'^mgmt_production_hourly_edit/get/(?P<index>\d+)/$', mgmt_production_hourly_edit),
	url(r'^mgmt_display_edit/get/(?P<index>\d+)/$', mgmt_display_edit),
	url(r'^mgmt_display_next/', mgmt_display_next),
	url(r'^mgmt_display_prev/', mgmt_display_prev),
	url(r'^mgmt_test1/', mgmt_test1),
	url(r'^mgmt_track_week/',mgmt_track_week),
	url(r'^mgmt_goals/',mgmt_goals),
	url(r'^plus_0455/',plus_0455),
	url(r'^minus_0455/',minus_0455),
	url(r'^plus_9341/',plus_9341),
	url(r'^minus_9341/',minus_9341),
	url(r'^plus_3050/',plus_3050),
	url(r'^minus_3050/',minus_3050),
	url(r'^plus_1467/',plus_1467),
	url(r'^minus_1467/',minus_1467),
	url(r'^track_10r/', track_10r),
	url(r'^track_10r_data/', track_10r_data),
	url(r'^tracking/', tracking),
	url(r'^tracking_10R80/', tracking_10R80),
	url(r'^tracking_10R80_resume/', tracking_10R80_resume),
	url(r'^tracking_10R80_screen/', tracking_10R80_screen),
	url(r'^track_graph_10r_prev/get/(?P<index>\d+)/$', track_graph_10r_prev),
	url(r'^track_graph_tri_prev/get/(?P<index>\d+)/$', track_graph_tri_prev),
	url(r'^track_graph_prev1/get/(?P<index>\d+)/$', track_graph_prev1),
	url(r'^track_graph_prev2/get/(?P<index>\d+)/$', track_graph_prev2),
	url(r'^track_graph_track/get/(?P<index>\d+)/$', track_graph_track),
	
	url(r'^track_graph_8670/get/(?P<index>\d+)/$', track_graph_8670),

	# url(r'^track_graph_8670/get/(?P<index>[\w|\W]+)', track_graph_8670),



	url(r'^track_1703/', track_1703),
	url(r'^track_1703_initial/get/(?P<index>\d+)/$', track_1703_initial),
	url(r'^track_1704_initial/get/(?P<index>\d+)/$', track_1704_initial),

	url(r'^chart1_1467/', chart1_1467),
	url(r'^chart2_1467/', chart2_1467),
	url(r'^chart1_3050/', chart1_3050),
	url(r'^chart2_3050/', chart2_3050),
	url(r'^chart1_5710/', chart1_5710),
	url(r'^chart2_5710/', chart2_5710),
	url(r'^chart1_1467b/', chart1_1467b),
	url(r'^chart2_1467b/', chart2_1467b),
	url(r'^chart1_1467o/', chart1_1467o),
	url(r'^chart2_1467o/', chart2_1467o),
	url(r'^chart1_1467br/', chart1_1467br),
	url(r'^chart2_1467br/', chart2_1467br),
	url(r'^chart1_3050b/', chart1_3050b),
	url(r'^chart2_3050b/', chart2_3050b),
	url(r'^chart1_5710b/', chart1_5710b),
	url(r'^chart2_5710b/', chart2_5710b),
	url(r'^chart1_0455/', chart1_0455),
	url(r'^chart2_0455/', chart2_0455),
	url(r'^chart1_0455_OP30/', chart1_0455_OP30),
	url(r'^chart2_0455_OP30/', chart2_0455_OP30),
	url(r'^chart1_0455_OP40/', chart1_0455_OP40),
	url(r'^chart2_0455_OP40/', chart2_0455_OP40),
	url(r'^chart1_0455_OP50/', chart1_0455_OP50),
	url(r'^chart2_0455_OP50/', chart2_0455_OP50),
	url(r'^chart1_9341/', chart1_9341),
	url(r'^chart2_9341/', chart2_9341),
	url(r'^chart1_9341_OP30/', chart1_9341_OP30),
	url(r'^chart2_9341_OP30/', chart2_9341_OP30),
	url(r'^chart1_1502/', chart1_1502),
	url(r'^chart2_1502/', chart2_1502),
	url(r'^chart1_1507/', chart1_1507),
	url(r'^chart2_1507/', chart2_1507),
	url(r'^chart1_1539/', chart1_1539),
	url(r'^chart2_1539/', chart2_1539),
	url(r'^chart1_9341_OP80/', chart1_9341_OP80),
	url(r'^chart2_9341_OP80/', chart2_9341_OP80),
	url(r'^chart1_9341_OP110/', chart1_9341_OP110),
	url(r'^chart2_9341_OP110/', chart2_9341_OP110),
	url(r'^chart1_5214_OP30/', chart1_5214_OP30),
	url(r'^chart2_5214_OP30/', chart2_5214_OP30),
	url(r'^chart1_8670_OP80/', chart1_8670_OP80),
	url(r'^chart2_8670_OP80/', chart2_8670_OP80),
	url(r'^chart1_5404_OP80/', chart1_5404_OP80),
	url(r'^chart2_5404_OP80/', chart2_5404_OP80),
	url(r'^chart1_5401_OP80/', chart1_5401_OP80),
	url(r'^chart2_5401_OP80/', chart2_5401_OP80),
	url(r'^chart1_3214_OP30/', chart1_3214_OP30),
	url(r'^chart2_3214_OP30/', chart2_3214_OP30),
	url(r'^mgmt_priorities/', mgmt_priorities),   
	url(r'^cell_track_9341/', cell_track_9341),
	url(r'^cell_track_1467/', cell_track_1467),
	url(r'^cell_track_8670/', cell_track_8670),
	url(r'^cell_track_9341_TV/', cell_track_9341_TV),
	url(r'^cell_track_9341_NEW/', cell_track_9341_NEW),
	url(r'^cell_track_9341_mobile/', cell_track_9341_mobile),
	url(r'^cell_track_9341_history_on/', cell_track_9341_history_on),
	url(r'^cell_track_9341_history_off/', cell_track_9341_history_off),
	url(r'^cell_track_9341_history/', cell_track_9341_history),
	url(r'^cell_track_9341_archive/', cell_track_9341_archive),
	url(r'^cell_track_9341_history2/', cell_track_9341_history2),
	url(r'^cell_9341_mobile/', cell_9341_mobile),
	url(r'^cell_9341_screen/', cell_9341_screen),
	url(r'^cell_track_9341_v2/', cell_track_9341_v2),
	url(r'^track_9341_history_date/', track_9341_history_date),
	url(r'^wip_update/', wip_update),



	# ************************************************************************


	# **************  Opertions Section ***************************************
	url(r'^gf6_reaction/', gf6_reaction),
	url(r'^gf6_input/', gf6_input),
	url(r'^gf6_reaction_prev/', gf6_reaction_prev),
	url(r'^gf6_input_prev/', gf6_input_prev),
	url(r'^prod_9341/', prod_9341),
	url(r'^prod_10R/', prod_10R),
	url(r'^prod_counts1/', prod_counts1),
	url(r'^prod_counts2/', prod_counts2),
	url(r'^hourly_counts/get/(?P<index>[\w|\W]+)', hourly_counts),
	url(r'^prod_ab1v/', prod_ab1v),
	url(r'^prod_ab1v_reaction/', prod_ab1v_reaction),
	url(r'^prod_ab1v_reaction_prev/', prod_ab1v_reaction_prev),
	url(r'^prod_ab1v_prev/', prod_ab1v_prev),
	url(r'^prod_ab1v_initial/', prod_ab1v_initial),
	url(r'^prod_10R_initial/', prod_10R_initial),
	url(r'^prod_10R_prev/', prod_10R_prev),
	url(r'^prod_728/', prod_728),
	url(r'^prod_728fault/', prod_728fault),
	url(r'^prod_728fault_prev/', prod_728fault_prev),
	url(r'^test_email_7/', test_email_7),

	url(r'^track_single/', track_single),

	url(r'^live_10R/', live_10R),
	url(r'^live_update1/', live_update1),


	url(r'^runrate_10R80/', runrate_10R80),
    
	url(r'^downtime_month_selection/', downtime_month_selection),
    url(r'^downtime_category_selection/get/(?P<index>[\w|\W]+)', downtime_category_selection),
    url(r'^downtime_category_history/get/(?P<index>[\w|\W]+)', downtime_category_history),




	# ************************************************************************


	# **************  Admin Section ***************************************
	url(r'^master/', master),
	url(r'^master2/', master2),
	url(r'^excel_dump/', excel_dump),
	url(r'^excel_scrap_dump/', excel_scrap_dump),
	url(r'^auto_updater/', auto_updater),
	url(r'^password_edit_form/', password_edit_form),
	url(r'^tech_pm_add/', tech_pm_add),

	url(r'^temp_display/', temp_display),

	url(r'^manpower_calculation/', manpower_calculation),


	# ************************************************************************


		# **************  Mod1 Section ***************************************
	url(r'^index_template/get/(?P<index>\d+)/$', index_template),
	# ************************************************************************

	# Retrieve Data from ADMIN views for testing
	url(r'^retrieve/', retrieve),
	url(r'^create_table/', create_table),
	
	
	url(r'^push_button/', push_button),
	url(r'^inventory_type_entry/', inventory_type_entry),
	url(r'^inventory_entry/', inventory_entry),
	url(r'^inventory_fix/', inventory_fix),

	# **************  Mod2 Section ***************************************
	url(r'^hrly_display/', hrly_display),
	url(r'^butter/', butter),

	# *************  Barcode *********************************************
	url(r'^barcode_input/', barcode_input),
	url(r'^barcode_check/', barcode_check),
	url(r'^barcode_initial/', barcode_initial),
	url(r'^barcode_reset/', barcode_reset),
	url(r'^barcode_search/', barcode_search),
	url(r'^barcode_search_check/', barcode_search_check),
	url(r'^barcode_verify/', barcode_verify),
	url(r'^barcode_verify_check/', barcode_verify_check),
	url(r'^barcode_input_10R/', barcode_input_10R),
	url(r'^barcode_check_10R/', barcode_check_10R),
	url(r'^barcode_initial_10R/', barcode_initial_10R),
	url(r'^barcode_wrong_part/', barcode_wrong_part),
	url(r'^barcode_wrong_part2/', barcode_wrong_part2),
	url(r'^barcode_wrong_part_reset/', barcode_wrong_part_reset),
	url(r'^barcode_count/', barcode_count),

	# *************  Quality Section *********************************************
	url(r'^scrap_mgmt/', scrap_mgmt),
	url(r'^scrap_mgmt_login_form/', scrap_mgmt_login_form),
	url(r'^scrap_display/', scrap_display),
	url(r'^scrap_display_24hr/', scrap_display_24hr),
	url(r'^scrap_display_date_pick/', scrap_display_date_pick),
	url(r'^scrap_entries_next/', scrap_entries_next),
	url(r'^scrap_entries_prev/', scrap_entries_prev),
	url(r'^scrapdate_fix1/', scrapdate_fix1),
	url(r'^tpm_display/', tpm_display),
	url(r'^scrap_edit_categories_reset/', scrap_edit_categories_reset),
	url(r'^scrap_edit_categories/', scrap_edit_categories),
	url(r'^scrap_edit_categories_entry/', scrap_edit_categories_entry),
	url(r'^scrap_edit_categories_newentry/', scrap_edit_categories_newentry),
	url(r'^scrap_edit_categories_delete/get/(?P<index>\d+)/$', scrap_edit_categories_delete),
	url(r'^scrap_edit_categories_save/', scrap_edit_categories_save),
	url(r'^pie_chart/', pie_chart),
	url(r'^initial_epv/', initial_epv),
	url(r'^next_epv/', next_epv),
	url(r'^previous_epv/', previous_epv),
	url(r'^epv_cleanup/', epv_cleanup),
	url(r'^quality_epv_asset_entry/', quality_epv_asset_entry),

	url(r'^gate_alarm_list/', gate_alarm_list),
	url(r'^gate_alarm_list_add/', gate_alarm_list_add),
	url(r'^gate_alarm_list_edit/', gate_alarm_list_edit),
	url(r'^gate_alarm_list_del/', gate_alarm_list_del),
	url(r'^gate_alarm_list_hide/', gate_alarm_list_hide),
	url(r'^gate_alarm_list_show/', gate_alarm_list_show),
	url(r'^gate_alarm_list_add_initial/', gate_alarm_list_add_initial),
	url(r'^gate_alarm_champion_initial/get/(?P<index>\w{0,50})/$', gate_alarm_champion_initial),
	url(r'^gate_alarm_champion/', gate_alarm_champion),
	# **************************************************************************

	# *************  Manpower Section *********************************************
	url(r'^manpower_update_v2/', manpower_update_v2),
	url(r'^matrix_update_v2/', matrix_update_v2),
	url(r'^training_matrix3/', training_matrix3),
	url(r'^training_performance/', training_performance),
	url(r'^trained_email/', trained_email),
	url(r'^track_email/', track_email),
	url(r'^manpower_allocation_interval_pick/', manpower_allocation_interval_pick),
	# **************************************************************************

	# **************  HR Section ***************************************
	url(r'^hr/', hr),
	url(r'^hr_login_form/', hr_login_form),
    url(r'^hr_down/', hr_down),

	url(r'^update7/', update7),
	url(r'^update7_prev/', update7_prev),


	url(r'^temp_test_reset/', temp_test_reset),
	url(r'^temp_test1/', temp_test1),
	url(r'^temp_ack/get/(?P<index>\w{0,50})/$', temp_ack),
	url(r'^temp_ack_taken/', temp_ack_taken),
    url(r'^productline_dl/', productline_dl),
    url(r'^date_picker_productline/', date_picker_productline),
    url(r'^production_OA/', production_OA),
    url(r'^date_picker_production_OA/', date_picker_production_OA),
    url(r'^production_OA_24hrs/', production_OA_24hrs),
	

	# **************************************************************************
# *******************************************  Machinery ********************************************************************************************
	url(r'^downtime_category_enter/', downtime_category_enter),
    url(r'^downtime_category/', downtime_category),



	# url(r'^scrap_display_operation/get/(?P<index>\w{0,50})/$', scrap_display_operation),
	
	url(r'^scrap_display_operation/get/(?P<index>[\w\-]+)/$', scrap_display_operation),

	# Need to have \w|W as url pattern to capture spaces and other characters
	# url(r'^scrap_display_category/get/(?P<index>[\w\-]+)/$', scrap_display_category),
	url(r'^scrap_display_category/get/(?P<index>[\w|\W]+)', scrap_display_category),
	url(r'^scrap_display_category_shift/get/(?P<index>[\w|\W]+)', scrap_display_category_shift),
	url(r'^scrap_display_entry_edit/get/(?P<index>[\w|\W]+)', scrap_display_entry_edit),
	url(r'^scrap_entries/', scrap_entries),
	url(r'^scrap_entries_update/(?P<index>\d+)/$', scrap_entries_update),
	#url(r'^scrap_entries/get/(?P<index>[\w\-]+)/$', scrap_entries),
	#url(r'^scrap_display_o/', scrap_display_o),
	url(r'^operation_entries_prev/', operation_entries_prev),
	url(r'^operation_entries_next/', operation_entries_next),
	url(r'^operation_department/', operation_department),
	# url(r'^part_entries/', part_entries),
	url(r'^operation_entries_update/(?P<index>\d+)/$', operation_entries_update),
	# url(r'^kiosk_add_category/get/(?P<index>[\w|\W]+)',  kiosk_add_category),
	# url(r'^kiosk_add_category/(?P<index>\d+)/$', kiosk_add_category),
	url(r'^kiosk_add_category/', kiosk_add_category),
	url(r'^kiosk_initiate/', kiosk_initiate),
	# url(r'^part_entries_update/(?P<index>\d+)/$', part_entries_update),
	# url(r'^part_entries_prev/', part_entries_prev),
	# url(r'^part_entries_next/', part_entries_next),


]
 

