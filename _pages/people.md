---
title: People
layout: archive
permalink: /people/
class: wide
---


<!-- <div class="grid__wrapper">
    {% for person in site.data.people.people %}
        <figure>
            <img src=
                {{ person.image_path | relative_url }}
            >
        </figure>
        
    {% endfor %}
</div> -->


<div>
{% for person in site.data.people.people %}
    <figure>
    {% if person.url %}
        <a href=
            {% if person.url contains "://" %}
              "{{ person.url }}"
            {% else %}
              "{{ person.url | relative_url }}"
            {% endif %}
            title="{{ person.name }}"
        >
        <img class="thumb" src=
          {% if person.image_path contains "://" %}
            "{{ person.image_path }}"
          {% else %}
            "{{ person.image_path | relative_url }}"
          {% endif %}
          >
        </a>
    {% else %}
        <img class="thumb" src=
          {% if person.image_path contains "://" %}
            "{{ person.image_path }}"
          {% else %}
            "{{ person.image_path | relative_url }}"
          {% endif %}
          alt="{{ person.name }}">
    {% endif %}
    <figcaption>
        <strong>{{person.name}}</strong><br>
        {{person.title}}<br>
        {{person.subject}}
    </figcaption>
    </figure>
{% endfor %}
</div>

