# coding: utf-8
import re
from django.core import mail
from django_webtest import WebTest
from django import test
from django.core.urlresolvers import reverse

#class AuthTest(WebTest):
    ##fixtures = ['users.json']

    #def testLogoutAndLogin(self):
        #page = self.app.get('/', user='test3')
        #page = page.click(href="/accounts/logout/",verbose=True).follow()
        #assert "/accounts/logout/" not in page
        #page = self.app.get('/accounts/login/')
        #login_form = page.form
        ##login_form = page.click(linkid="log-in", index=0,verbose=True).form
        #login_form['username'] = 'test3'
        #login_form['password'] = 'test3'
        ##login_form['csrfmiddlewaretoken'] = login_form['csrfmiddlewaretoken']
        #print login_form.fields
        #result_page = login_form.submit().follow()
        #assert "{% url 'auth_login' %}" not in result_page
        #assert "/accounts/logout/" in result_page

    #def testEmailRegister(self):
        #register_form = self.app.get('/').click(u'Регистрация').form
        #self.assertEqual(len(mail.outbox), 0)
        #register_form['email'] = 'example2@example.com'
        #register_form['password'] = '123'
        #assert u'Регистрация завершена' in register_form.submit().follow()
        #self.assertEqual(len(mail.outbox), 1)

        ## активируем аккаунт и проверяем, что после активации
        ## пользователь сразу видит свои покупки
        #mail_body = unicode(mail.outbox[0].body)
        #activate_link = re.search('(/activate/.*/)', mail_body).group(1)
        #activated_page = self.app.get(activate_link).follow()
        #assert u'<h1>Мои покупки</h1>' in activated_page


__test__ = {"urls": """
>>> c = test.Client()
>>> c.get(reverse('orders')).status_code
200
>>> c.get(reverse('list_type_work')).status_code
200
>>> c.get(reverse('create_type_work1')).status_code
200
"""}