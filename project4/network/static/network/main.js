let currentPage = 1;
document.addEventListener('DOMContentLoaded', function() {
    var path = window.location.pathname;
    var pattern = /^\/users\/(\w+)$/;
    var pattern2 = /\/\w+\/following/;
    if (pattern.test(path)) {
        var user = path.match(pattern)[1];
        fetch_userPage(user,currentPage);
        document.getElementById('user-previous-button').addEventListener('click', () => {
            currentPage--;
            fetch_userPage(user,currentPage);
        });
        document.getElementById('user-next-button').addEventListener('click', () => {
            currentPage++;
            fetch_userPage(user,currentPage);
        });
    }else if(pattern2.test(path)){
        load_following(currentPage);
        document.getElementById('previous-button').addEventListener('click', () => {
            currentPage--;
            fetch_posts(currentPage);
        });
        document.getElementById('next-button').addEventListener('click', () => {
            currentPage++;
            fetch_posts(currentPage);
        });
    }else{
        fetch_posts(currentPage);
        document.getElementById('previous-button').addEventListener('click', () => {
            currentPage--;
            fetch_posts(currentPage);
        });
        document.getElementById('next-button').addEventListener('click', () => {
            currentPage++;
            fetch_posts(currentPage);
        });
    }
  });

function fetch_posts(page){
    divBody = document.getElementById("post-section");
    fetch(`/get_posts/All/?page=${page}`)
        .then(response => response.json())
        .then(posts => {
            var logged_user = posts["logged_user"];
            var total_pages = posts["total_pages"];
            divBody.innerHTML = "";
            posts["data"].forEach(post => {
                /*fetch(`${post['id']}/like_count`)
                .then(response => response.json())
                .then(result => {
                    if (logged_user && result.user_liked) {
                        likeButton = document.createElement('button');
                        likeButton.innerHTML = 'Unlike';
                        likeButton.addEventListener('click', () => {
                            console.log("clicked");
                            fetch(`/${post["id"]}/like`, {
                                method: 'PUT'
                              }).then(() => {
                                console.log(`liked`);
                              })
                        });
                    } else if (logged_user && !result.user_liked) {
                        likeButton = document.createElement('button');
                        likeButton.innerHTML = 'Like';
                        //TODO LIKE/UNLIKE
                        likeButton.addEventListener('click', () => {
                            console.log("clicked");

                            fetch(`/${post["id"]}/like`, {
                                method: 'PUT'
                              }).then(() => {
                                console.log(`liked`);
                              })
                        });
                    }
                    totalLikes.innerHTML = `Total Likes: ${result.total_likes}`;
                    if (likeButton) {
                        postBody.appendChild(likeButton);
                    }
                    postBody.appendChild(totalLikes);
                })
                .catch(error => console.error('Error fetching like count:', error));*/
                made_post = make_post(post,logged_user,1)
                divBody.append(made_post);
                });
                document.getElementById('previous-button').style.display = currentPage === 1 ? 'none' : 'block';
                document.getElementById('next-button').style.display = currentPage === total_pages ? 'none' : 'block'; 
        });
}


function fetch_userPage(username,page){
    divBody = document.getElementById("user-post-section");
    fetch(`/get_posts/${username}/?page=${page}`)
    .then(response => response.json())
    .then(posts => {
        var total_pages = posts["total_pages"];
        var logged_user = posts["logged_user"];
        divBody.innerHTML = "";
        posts["data"].forEach(post => {
            made_post = make_post(post,logged_user,2)
            divBody.append(made_post);
            });
            document.getElementById('user-previous-button').style.display = currentPage === 1 ? 'none' : 'block';
            document.getElementById('user-next-button').style.display = currentPage === total_pages ? 'none' : 'block'; 
    });
}

function Follow(follower,followed){
    fetch(`/follow`, {
        method: 'PUT',
        body: JSON.stringify({
            followed: followed,
            follower: follower
        })
      }).then(() => {
        console.log(`${follower} followed succesfully ${followed}`);
        window.location.href = `/users/${followed}`;
      });
}

function Unfollow(follower,followed){
    console.log("Follower: " + follower);
    console.log("Following: " + followed);
    fetch(`/unfollow`, {
        method: 'PUT',
        body: JSON.stringify({
            followed: followed,
            follower: follower
        })
      }).then(() => {
        console.log(`${follower} unfollowed succesfully ${followed}`);
        window.location.href = `/users/${followed}`;
      });
}

function load_following(page){
    divBody = document.getElementById("post-section");
    fetch(`/following?page=${page}`)
    .then(result => result.json())
    .then(posts => {
        var total_pages = posts["total_pages"];
        divBody.innerHTML = "";
        posts["data"].forEach(post => {
            console.log(post['id']);
            made_post = make_post(post,null,0)
            divBody.append(made_post);
        });
        document.getElementById('previous-button').style.display = currentPage === 1 ? 'none' : 'block';
        document.getElementById('next-button').style.display = currentPage === total_pages ? 'none' : 'block'; 
    });
}

function edit_post(post_id,post_body){
    body = document.getElementById(`post${post_id}`);
    body.innerHTML = "";
    textarea = document.createElement("textarea");
    textarea.innerHTML = post_body;
    textarea.setAttribute('id','edit_txt');
    body.append(textarea);
    const buttons = document.getElementsByClassName("editBtn");
    Array.from(buttons).forEach(button => {
        button.style.display = "none";
    });
    saveBtn = document.createElement("button");
    saveBtn.innerHTML = "Save";
    saveBtn.classList.add("btn");
    saveBtn.classList.add("btn-primary");
    body.append(saveBtn);
    saveBtn.addEventListener('click', () => {
        text = document.getElementById("edit_txt").value;
        saveBtn.style.display = "none";
        fetch(`/edit_post/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                text: text
            })
          }).then(() => {
            console.log(`Saved successfully`);
            fetch(`/get_post/${post_id}`).
            then(response => response.json())
            .then(post => {
                postare = post["post"][0];
                body.innerHTML =
                `<div style = "font-size: 24px;">
                ${postare["body"]}</div>
                <h6>${postare["timestamp"]}</h6>`;
            });
          });
    });

}

function make_post(post_data, logged_user,type){
    //DEFAULT POST/FOR FOLLOWING PAGE
    post = document.createElement('div');
    post.style = "margin: 10px;";
    postBody = document.createElement("div");
    user = document.createElement('a');
    user.href = `/users/${post_data["user"]}`;
    user.innerHTML = `${post_data["user"]}`;
    user.style = "color: black;"
    user.classList.add("h3");
    postBody.innerHTML =
    `<div style = "font-size: 24px;">
    ${post_data["body"]}</div>
    <h6>${post_data["timestamp"]}</h6>`;
    let totalLikes = document.createElement('h6');
    let likeButton = document.createElement('button');
    likeButton.classList.add("btn");
    likeButton.classList.add("btn-primary");
    likeButton.style = "margin-right: 10px;";
    fetch(`${post_data['id']}/like_count`)
            .then(response => response.json())
            .then(result => {
                likeButton.innerHTML = result.user_liked ? "Unlike" : "Like";
                totalLikes.innerHTML = `Total Likes: ${result.total_likes}`;
    });
    likeButton.addEventListener('click', () => {
        fetch(`/${post_data["id"]}/like`, {
            method: 'PUT'
        }).then(() => {
            fetch(`${post_data['id']}/like_count`)
            .then(response => response.json())
            .then(result => {
                likeButton.innerHTML = result.user_liked ? "Unlike" : "Like";
                totalLikes.innerHTML = `Total Likes: ${result.total_likes}`;
            })
        })
    });
    post.append(user);
    post.append(postBody);

    post.append(totalLikes);
    if(logged_user && type != 2){
        post.append(likeButton);
    }
    //1 IS FOR ALL POSTS
    //2 IS FOR USER POSTS
    if (type){
        postBody.setAttribute('id',`post${post_data["id"]}`);
        if(post_data["user"] == logged_user){
            editBtn = document.createElement("button");
            editBtn.innerHTML = "Edit";
            editBtn.classList.add("editBtn");
            editBtn.classList.add("btn");
            editBtn.classList.add("btn-primary");
            editBtn.addEventListener('click', () => {
                post_id = post_data["id"];
                post_body = post_data["body"];
                edit_post(post_id,post_body);
            });
            post.append(editBtn);
        }
    }
    else{
        post.append(document.createElement("hr"));
        return post
    }
    post.append(document.createElement("hr"));
    return post
}