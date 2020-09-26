# Network
A Twitter-like social network website for making posts and following users.

![](/repoImages/Network1.gif)

Within this repository is a Django project called `project4` that contains a single app called `network`. This was one of the final projects of Harvard's [CS50W](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/) course.

### How to run locally
After cloning the repository onto your machine, navigate to the project's directory.

1. Install requirements (keep in mind this was made with `python 3.8.3`)
    - `pip install -r requirements.txt`

2. Create a database
    - `python`
    ```python
     import sqlite3
     conn = None
     conn = sqlite3.connect("myDB.db")
     conn.close()
     quit()
    ```

    - Change the name of the used DB in `settings.py` within the `project4` directory.
    ```py
    DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'myDB.db')}
    }
    ```

3. Migrate and run server
    - `python manage.py migrate`
    - `python manager.py runserver`

### Understanding
- **All Posts**: Here, one can see all posts from all users, with the most recent posts first.
    - Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.
    - Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

- **Profile Page**: Clicking on a username will load that user’s profile page. This page will:
    - Display the number of followers the user has, as well as the number of people that the user follows.
    - Display all of the posts for that user, in reverse chronological order.
    - For any other user who is signed in, a “Follow” or “Unfollow” button is available to let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user cannot follow themselves.

- **Following**: The "Following" link in the navigation bar takes the user to a page where they can see all posts made by users that the current user follows.  
    - This page behaves just as the “All Posts” page does, just with a more limited set of posts.
    - This page is only available to users who are signed in.

- **Features**
    - Pagination
    - AJAX Post Editing
    - AJAX Like System




