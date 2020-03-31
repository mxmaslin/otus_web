const axios = require('axios');

//<li><a href="{% url 'courses:course-detail' pk=course.pk %}">{{ course }}</a></li>
//  {% endfor %}
//  </ul>



axios.get('/api/v1/courses')
    .then(function(response){
        let courses = response.data;
        let ul = $('ul.courses-fetched');
        let result = courses.map(
            course => {
            let course_id = JSON.stringify(course.id);
            let course_name = JSON.stringify(course.name).replace(/"/g, "");
            let course_started = JSON.stringify(course.started).replace(/"/g, "");;
         return `<li><a href='/${course_id}/'>${course_name} ${course_started}</a></li>`
        })
        result = result.join('');
        ul.append(result);
        console.log(result);
    })