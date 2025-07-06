{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account activation
{% endblock %}

http://127.0.0.1:8000/accounts/api/v1/activation/confirm/{{ token }}

{% endblock %}