Aktorzy afery:
              <ul class="group">{% for actor in case.actors %}
               <li><a href="{% url aktor.views.actor object_id=actor.0 %}">{{ actor.1 }}</a></li>{% endfor %}
              </ul>
              {% if case.num_actors %}<p class="pokaz" onclick="case_actors({{ case.id }})">pokaż wszystkich ({{ case.num_actors }})</p>{% endif %}
