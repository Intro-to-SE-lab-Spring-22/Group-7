from django.urls import path

from . import views

urlpatterns = [
	# ex: /userpage/
	path('', views.index, name='index'),

	# ex: /userpage/search/
	path('search/', views.search, name='search'),

	# ex: /userpage/newacc/
	path('newacc/', views.new_acc, name='new_acc'),

	# ex: /userpage/signin/
	path('signin/', views.sign_in, name='sign_in'),

	# ex: /userpage/#/
	path('<int:user_id>/', views.page, name='page'),
	
	# ex: /userpage/#/#/
	path('<int:user_id>/<int:page_num>/', views.page_num, name='page_num'),

	# ex: /userpage/#/mesg/
	path('<int:user_id>/mesg/', views.mesg, name='mesg'),

	# ex: /userpage/#/friend/
	path('<int:user_id>/friend/', views.friend, name='friend'),

	# ex: /userpage/#/post/
	path('<int:user_id>/post/', views.post, name='post'),

	# ex: /userpage/#/change_size/
	path('<int:user_id>/change_size/', views.chng_size, name='chng_size'),

	# ex: /userpage/change_pass/
	path('change_pass/', views.chng_pass, name='chng_pass'),

	# ex: /userpage/#/change_image/
	path('<int:user_id>/change_image/', views.chng_img, name='chng_img'),

	# ex: /userpage/#/change_data/
	path('<int:user_id>/change_data/', views.chng_data, name='chng_data'),

	# ex: /userpage/post/#/
	path('post/<int:post_id>/', views.comment_page, name='comment_page'),

	# ex: /userpage/post/#/#
	path('post/<int:post_id>/<int:page_num>/', views.comment_page_num, name='comment_page_num'),
    
	# ex: /userpage/post/#/share
	path('post/<int:post_id>/share/', views.share, name='share'),
    
	# ex: /userpage/post/#/like
	path('post/<int:post_id>/like/', views.like, name='like'),

	# ex: /userpage/post/#/comment/
	path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
    
	# ex: /userpage/post/#/del/
	path('post/<int:post_id>/del/', views.delete, name='delete'),

	# ex: /userpage/post/#/edit    
	path('post/<int:post_id>/edit/', views.edit, name='edit'),
]