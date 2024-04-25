---
title: Opportunities
layout: single
class: wide
permalink: /opportunities/
---

<div markdown="0">
<ul>
    {% for opening in site.data.opportunities.openings %}
    <li>
        <h2><a href="{{opening.url}}">{{opening.title}}</a></h2>
            {% if opening.description %}
                <details>
                    <summary>Description</summary>
                    <br>
                        {% include {{opening.description}} %}
                </details>
            {% endif %}
        <br>
            {% if opening.apply %}
                <details>
                    <summary>Apply</summary>
                    <br>
                        {% include {{opening.apply}} %}
                </details>
            {% endif %}
        <br>
        Contact: <a href="mailto:{{opening.email}}">{{opening.contact}}</a>
    </li>
    {% endfor %}
</ul>
</div>