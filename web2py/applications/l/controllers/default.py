# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ########################################################################
# # This is a sample controller
# # - index is the default action of any application
# # - user is required for authentication and authorization
# # - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Welcome to web2py!")
    response.title = "所有课程"
    lessons = db(db.lesson_list).select(orderby=~db.lesson_list.l_date)
    return dict(lessons=lessons)


@auth.requires_membership("teacher")
def add_new():
    response.title = "添加新完成的课程"
    form = SQLFORM(db.lesson_list, fields=["l_name",
                                           "l_author",
                                           "l_date"])
    if form.process().accepted:
        if request.vars.redirect:
            redirect(request.vars.redirect)
        else:
            redirect(URL("index"))

    return dict(form=form)


@auth.requires(auth.has_membership("teacher") or auth.has_membership("editor"))
def edit_lesson():
    response.title = "编辑课程信息"
    if request.vars.l_id:
        l_id = request.vars.l_id
        form = SQLFORM(db.lesson_list, record=db.lesson_list[l_id], deletable=auth.has_membership("teacher"))
        if form.process().accepted:
            if request.vars.redirect:
                redirect(request.vars.redirect)
            else:
                redirect(URL("index"))

        return dict(form=form)
    else:
        redirect(URL("index"))


@auth.requires_login()
def this_week():
    response.title = "本周完成的课程"

    today = datetime.date.today()
    this_week_start = today - datetime.timedelta(days=today.weekday())
    lessons = db(db.lesson_list.l_date >= this_week_start).select(orderby=~db.lesson_list.l_date)

    return dict(lessons=lessons)


@auth.requires_login()
def under_line_lesson():
    response.title = "未上线课程"

    lessons = db(db.lesson_list.l_online_date == None).select(orderby=~db.lesson_list.l_date)
    return dict(lessons=lessons)


@auth.requires_login()
def online_this_week():
    response.title = "本周上线课程"

    today = datetime.date.today()
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)
    lessons = db((db.lesson_list.l_online_date >= this_week_start) &
                 (db.lesson_list.l_online_date <= this_week_end)
    ).select(orderby=~db.lesson_list.l_online_date)
    return dict(lessons=lessons)


@auth.requires_login()
def online_next_week():
    response.title = "下周上线课程"

    today = datetime.date.today()
    this_week_start = today - datetime.timedelta(days=today.weekday())
    this_week_end = this_week_start + datetime.timedelta(days=6)
    next_week_start = this_week_start + datetime.timedelta(days=7)
    next_week_end = this_week_end + datetime.timedelta(days=7)
    lessons = db((db.lesson_list.l_online_date >= next_week_start) &
                 (db.lesson_list.l_online_date <= next_week_end)
    ).select(orderby=~db.lesson_list.l_online_date)
    return dict(lessons=lessons)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    response.title = "用户登陆"
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
