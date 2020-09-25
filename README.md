# Network
A Twitter-like social network website for making posts and following users.

Within this repository is a Django project called `project4` that contains a single app called `network`. This was one of the final projects of Harvard's [CS50W]() course.

**How to run locally**

**Understanding**
- **All Posts**: Here, one can see all posts from all users, with the most recent posts first.
    - Each post includes the username of the poster, the post content itself, the date and time at which the post was made, and the number of “likes” the post has.
    - Users who are signed in are able to write a new text-based post by filling in text into a text area and then clicking a button to submit the post.

- **Profile Page**: Clicking on a username will load that user’s profile page. This page will:
    - Display the number of followers the user has, as well as the number of people that the user follows.
    - Display all of the posts for that user, in reverse chronological order.
    - For any other user who is signed in, a “Follow” or “Unfollow” button is available to let the current user toggle whether or not they are following this user’s posts. Note that this only applies to any “other” user: a user cannot follow themselves.




