# Educational site

There are two tasks:

* make the GraphQL scheme that allows to get courses, teachers and all students enrolled to each course.
* add Query for three models in the project. Add a mutation for one of the models. Write tests to ensure availability of all Queries.

Prior to exploring the project, install the requirements:

    pip install -r requirements.txt
    
To start evaluating GraphQL stuff, run server
    
    ./manage.py runserver
    
Then open http://127.0.0.1:8000/graphql and enter:

```
query{
  courses{
    id
    name
    teacher{
      id
      username
    }
    students{
      id
      username
    }
  }
}
```
That is the solution for the first part of homework.

The second part:

* to create a course, use

```
mutation {
  createCourse(courseData:{
      name: "Course name",
    	started: "2019-05-01T15:12:04+03:00", 
    	teacher: "Existing teacher"
  })
  {
   course{
      name
    	started
    	teacher{
        username
      }
    } 
  }
}
```

* to update the course, use

```
mutation {
  updateCourse(courseData:{
    id: 1,
    name: "Новое название курса",
    started: "2019-05-01T15:12:04+03:00", 
    teacher: "Преподаватель"
  })
  {
   course{
      name
    	started
    	teacher{
        username
      }
    } 
  }
}
```
    
The application developed for [Web-разработчик на Python](https://otus.ru/lessons/webpython/) training course.