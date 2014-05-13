# coding: UTF-8
import os
import web

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, '../templates')
render = web.template.render(templates_root, cache=False)

db = web.database(dbn='mysql', db='cover', user='root', pw='lewis')

config = web.storage(
    email='lone.un@gmail.com',
    site_name = 'lll',
    site_desc = 'lll',
    static = '/static',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

