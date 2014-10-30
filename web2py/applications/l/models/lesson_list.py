# coding=utf-8

import datetime

db.define_table("lesson_list",
                Field("l_name", label="课程名称", requires=IS_NOT_EMPTY()),
                Field("l_author", label="录课讲师", requires=IS_NOT_EMPTY()),
                Field("l_date", label="创建日期", type="date", default=datetime.date.today()),
                Field("l_online_date", label="上线日期", type="date")
)
