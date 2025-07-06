{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account activation
{% endblock %}

{{ token }}

{% endblock %}