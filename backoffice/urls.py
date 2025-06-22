
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from backoffice.views.chart import create_scatter_chart, create_line_chart, scatter_chart, line_chart, task_progress

from backoffice.views.column import ColumnList, ColumnCreate, ColumnDetail, ColumnUpdate, ColumnDelete 
from backoffice.views.chat import ChatList, ChatCreate, ChatUpdate, message_response, ChatDetail, ChatDelete,message_thread
from backoffice.views.help import HelpList, HelpDetail, HelpCreate, HelpUpdate, HelpDelete
from backoffice.views.meeting import MeetingList, MeetingDetail, MeetingCreate, MeetingUpdate, MeetingDelete
from backoffice.views.meetingresult import MeetingResultList, MeetingResultDetail, MeetingResultCreate, MeetingResultUpdate, MeetingResultDelete
from backoffice.views.project import ProjectList, ProjectDetail, ProjectCreate, ProjectUpdate, ProjectDelete
from backoffice.views.supercolumn import SupercolumnList, SupercolumnCreate, SupercolumnDetail, SupercolumnUpdate, SupercolumnDelete 
from backoffice.views.task import TaskList, TaskCreate, TaskDetail, TaskUpdate, TaskDelete \
    , TaskProgressView, task_stats, task_status_scatter, task_status_line, task_statistics_data, task_statistics\
    ,actualizar_tablero, progreso
from backoffice.views.team import TeamList, TeamDetail, TeamCreate, TeamUpdate, TeamDelete,meetings_chart
from backoffice.views.membership import MembershipList, MembershipDetail, MembershipCreate, MembershipUpdate, MembershipDelete

from backoffice.views.dashboard import KanbanBoardView, dashboard_dos

from backoffice.views.home import dashboard



    
 

urlpatterns = [
   
    path('', dashboard, name='dashboard'),

    

    #ALL COLUMNS URLS
    path('all_columns/', ColumnList.as_view(), name='all_columns'  ),
    path('new_column/', ColumnCreate.as_view(), name="column_create"),
    path('detail_column/<int:pk>/', ColumnDetail.as_view(), name="column_detail"),
    path('update_column/<int:pk>/', ColumnUpdate.as_view(), name="column_update"),
    path('delete_column/<int:pk>/', ColumnDelete.as_view(), name="column_delete"),


      #ALL CHATS URLS
    path('all_chats/', ChatList.as_view(), name='all_chats'  ),
    path('new_chat/', ChatCreate.as_view(), name='new_chat'),
    path('update_chat/<int:pk>/', ChatUpdate.as_view(), name='update_chat'),
    path('response_message/<int:message_id>', message_response,name='response_message'),
    path('message_thread/<int:message_id>',message_thread,name='message_thread'),
    path('see_message/<int:pk>/', ChatDetail.as_view(), name='see_message'),
    path('delete_chat/<int:pk>/', ChatDelete.as_view(), name='delete_chat'),


    #ALL HELPS URLS
    path('help/', HelpList.as_view(), name='help'),
    path('detail_help/<int:pk>/', HelpDetail.as_view(), name='help_detail'),
    path('create_help/', HelpCreate.as_view(), name='help_create'),
    path('update_help/', HelpUpdate.as_view(), name='help_update'),
    path('delete_help/', HelpDelete.as_view(), name='help_delete'),  


    #ALL MEETING URLS
    path('all_meetings/', MeetingList.as_view(), name='all_meetings'),
    path('detail_meeting/<int:pk>/', MeetingDetail.as_view(), name='meeting_detail'),
    path('new_meeting/', MeetingCreate.as_view(), name='meeting_create'),
    path('update_meeting/<int:pk>/', MeetingUpdate.as_view(), name='meeting_update'),
    path('delete_meeting/<int:pk>/', MeetingDelete.as_view(), name='meeting_delete'),  


    #ALL MEETING RESULT URLS
    path('all_meetingresults/', MeetingResultList.as_view(), name='all_meetingresults'),
    path('detail_meetingresult/<int:pk>/', MeetingResultDetail.as_view(), name='meetingresult_detail'),
    path('new_meetingresult/', MeetingResultCreate.as_view(), name='meetingresult_create'),
    path('update_meetingresult/<int:pk>/', MeetingResultUpdate.as_view(), name='meetingresult_update'),
    path('delete_meetingresult/<int:pk>/', MeetingResultDelete.as_view(), name='meetingresult_delete'),  


    #ALL PROJECTS  URLS
    path('all_projects/', ProjectList.as_view(), name='all_projects'),
    path('detail_project/<int:pk>/', ProjectDetail.as_view(), name='project_detail'),
    path('new_project/',ProjectCreate.as_view(), name='project_create'),
    path('update_project/<int:pk>/', ProjectUpdate.as_view(), name='project_update'),
    path('delete_project/<int:pk>/', ProjectDelete.as_view(), name='project_delete'), 
  
    

     #ALL STATS URLS
    path("kanban_board/", KanbanBoardView.as_view(), name="kanban_board"),
    path('statistics/', task_statistics, name='task_statistics'),
    path('status/scatter/', task_status_scatter, name='task_status_scatter'),
    path('status/line/', task_status_line, name='task_status_line'),
    path('scatter_chart/', scatter_chart, name='scatter_chart'),
    path('line_chart/', line_chart, name='line_chart'),
    path('task_stats/', task_stats, name='task_stats'),
    path('task_statistics_data/', task_statistics_data, name='task_statistics_data'),



    #ALL SUPERCOLUMNS URLS
    path('all_supercolumns/', SupercolumnList.as_view(), name='all_supercolumns'  ),
    path('new_supercolumn/', SupercolumnCreate.as_view(), name="supercolumn_create"),
    path('detail_supercolumn/<int:pk>/', SupercolumnDetail.as_view(), name="supercolumn_detail"),
    path('update_supercolumn/<int:pk>/', SupercolumnUpdate.as_view(), name="supercolumn_update"),
    path('delete_supercolumn/<int:pk>/', SupercolumnDelete.as_view(), name="supercolumn_delete"),



     #ALL TASKS URLS
    path('all_tasks/', TaskList.as_view(), name='all_tasks'  ),
    path('new_task/', TaskCreate.as_view(), name="task_create"),
    path('detail_task/<int:pk>/', TaskDetail.as_view(), name="task_detail"),
    path('actualizar_tablero/', actualizar_tablero, name='actualizar_tablero'),
    path('update_task/<int:pk>/', TaskUpdate.as_view(), name="task_update"),
    path('delete_task/<int:pk>/', TaskDelete.as_view(), name="task_delete"),
    #path('task_move/<int:pk>/', task_move, name='task_move'),
    path('task/<int:pk>/progress/', progreso, name='task_progress'),



    #ALL TEAMS URLS
    
    path('all_teams/', TeamList.as_view(), name='all_teams'  ),
    #path('add_user_to_group/<int:pk>/', AddUserToGroupView.as_view(), name='add_user'  ),

    path('new_team/', TeamCreate.as_view(), name="team_create"),
    path('detail_team/<int:pk>/', TeamDetail.as_view(), name="team_detail"),
    path('update_team/<int:pk>/', TeamUpdate.as_view(), name="team_update"),
    path('delete_team/<int:pk>/', TeamDelete.as_view(), name="team_delete"),
    #path('groups/<int:pk>/remove_users/', RemoveUserFromGroupView.as_view(), name='remove_users_from_group'),    

    #ALL MEMBERSHIPS URLS
    path('all_members/', MembershipList.as_view(), name='all_members'  ),
    path('new_member/', MembershipCreate.as_view(), name="member_create"),
    path('detail_member/<int:pk>/', MembershipDetail.as_view(), name="member_detail"),
    path('update_member/<int:pk>/', MembershipUpdate.as_view(), name="member_update"),
    path('delete_member/<int:pk>/', MembershipDelete.as_view(), name="member_delete"),
   



]