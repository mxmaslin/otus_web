# Educational site

The task is to optimize interaction with DB.

The discussed optimization techniques are

- @cached_property
- F-expression
- Q-expression
- Aggregate, annotate
- select_related, prefetch_related
- exists()
- Subqueries

So the report is following:

At `courses/course-detail.html` and `api/v1/course/<int: pk>/` there were 9 duplicates. As result of [implementing](https://github.com/mxmaslin/otus_web/commit/10840a491b88cd8c8ef28fa09ad99202e6bc0d81) `@cached_property`
the number of duplicates decreased to 5.

Prior the optimization techniques lecture I was aware regarding all the listed techniques except `@cached_property`, and used
part of them (`select_related`, `prefetch_related`, `exists`) for this project.

I didn't find reasons to use the `F`/`Q-expressions`, `aggregate`, `annotate` and `subqueries`.

That's all.
    
The application developed for [Web-разработчик на Python](https://otus.ru/lessons/webpython/) training course.