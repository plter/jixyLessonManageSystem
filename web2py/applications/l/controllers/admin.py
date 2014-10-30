# -*- coding: utf-8 -*-

@auth.requires_membership("teacher")
def index():
    response.title = "网站管理"
    return dict()

@auth.requires_membership("teacher")
def users():
    response.title = "所有用户"
    usersData = db().select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name,db.auth_user.email)
    return dict(usersData=usersData)

@auth.requires_membership("teacher")
def groups():
    response.title = "所有群组"
    groupsData = db().select(db.auth_group.ALL)
    return dict(groupsData=groupsData)

@auth.requires_membership("teacher")
def member_ships():
    response.title = "用户关系表"
    member_ship_data = db().select(db.auth_membership.ALL)
    return dict(member_ship_data = member_ship_data)

@auth.requires_membership("teacher")
def member_ship_edit():
    response.title = "编辑用户关系"

    if request.vars.msid:
        msid = request.vars.msid
        form = SQLFORM(table=db.auth_membership,record=db.auth_membership[msid])
        if form.process().accepted:
            redirect("member_ships")

    else:
        redirect("member_ships")

    return dict(form=form)