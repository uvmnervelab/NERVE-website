---
title: Papers
layout: single
class: wide
permalink: /papers/
---


{% for category in site.data.papers.categories %}
  <h2>{{category.heading}}</h2>
  <ol>
  {% for paper in category.pubs %}
    <table>
      <td style="width:20%">
      {% if paper.links %}
        {% for link in paper.links limit:1 %}
        <a href="{{link.url}}">
          <img src=
              "{{ paper.image_path }}"
              width="200" height="200"
          >
        </a>
        {% endfor %} 
      {% else %}
          <img src=
              "{{ paper.image_path }}"
              width="200" height="200"
          >
      {% endif %}
      </td>
      <td>
        <li><strong>{{paper.title}}</strong>.
        <br>
        {% for author in paper.authors %}
          {% if forloop.last %}
            {{author}}.
        {% else %}
            {{author}},
        {% endif %}
        {% endfor %}
        <br>
        <em>{{paper.venue}}</em>, 
        {% if paper.volumeissue %}
          {{paper.volumeissue}},
        {% endif %}
        ({{paper.year}}).
        {% if paper.links %}
        <br>
          {% for link in paper.links %}
            [<a href="{{link.url}}">{{link.text}}</a>] 
          {% endfor %}
        {% endif %}
        </li>
      </td>
    </table>
    {% endfor %}
{% endfor %}
  </ol>

