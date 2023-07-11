function delete_post(post_id) {
    document.querySelector(`#deletePost_${post_id}_div`).style.display = 'block';

    document.querySelector(`#deleteWarning_${post_id}_noButton`).addEventListener('click', () => {
        document.querySelector(`#deletePost_${post_id}_div`).style.display = 'none';
    })

    document.querySelector(`#deleteWarning_${post_id}_yesButton`).addEventListener('click', () => {

        fetch(`/delete_post/${post_id}`, {
            method: 'POST'
        })

        document.querySelector(`#post_${post_id}_div`).remove();

        // return false;
    })

}

function edit_post(post_id) {
    document.querySelector(`#editPost_${post_id}_button`).style.display = 'none';
    document.querySelector(`#post_${post_id}_edited`).style.display = 'none';
    text = document.querySelector(`#post_${post_id}_text`).innerHTML;
    document.querySelector(`#post_${post_id}_text`).innerHTML = `<textarea id="editPost_${post_id}_textarea" maxlength="280">${text.trim()}</textarea> <input id="submitPost_${post_id}_button" type="submit" value="Edit">`;

    document.querySelector(`#submitPost_${post_id}_button`).addEventListener('click', () => {

        const edited_text = document.querySelector(`#editPost_${post_id}_textarea`).value;

        if (edited_text.trim() !== ("")) {

            fetch(`/edit_post/${post_id}`, {
                method: 'POST',
                body: JSON.stringify({text: edited_text})
            })
            document.querySelector(`#post_${post_id}_errorMessage`).innerHTML = '';
            document.querySelector(`#post_${post_id}_errorMessage`).style.display = 'none';
            document.querySelector(`#editPost_${post_id}_button`).style.display = 'block';
            document.querySelector(`#post_${post_id}_text`).innerHTML = document.querySelector(`#editPost_${post_id}_textarea`).value;
            document.querySelector(`#post_${post_id}_edited`).style.display = 'block';
            document.querySelector(`#post_${post_id}_edited`).innerHTML = 'Edited';

        }

        else {
            document.querySelector(`#post_${post_id}_errorMessage`).style.display = 'block';
            document.querySelector(`#post_${post_id}_errorMessage`).innerHTML = 'The post cannot be empty.';
        }

        return false;
        
    });
}

function like(post_id) {
    fetch(`/like/${post_id}`, {
        method: 'POST'
    })
    let likes_count = document.querySelector(`#post_${post_id}_likes`).innerHTML;
    likes_count ++;
    document.querySelector(`#post_${post_id}_likes`).innerHTML = likes_count;
    document.querySelector(`#like_${post_id}_button`).style.display = 'none';
    document.querySelector(`#likeAnimation_${post_id}_button`).style.display = 'block';
    document.querySelector(`#dislike_${post_id}_button`).style.display = 'none';
    return false;
}

function dislike(post_id) {
    fetch(`/dislike/${post_id}`, {
        method: 'POST'
    })
    let likes_count = document.querySelector(`#post_${post_id}_likes`).innerHTML;
    likes_count --;
    document.querySelector(`#post_${post_id}_likes`).innerHTML = likes_count;
    document.querySelector(`#like_${post_id}_button`).style.display = 'block';
    document.querySelector(`#likeAnimation_${post_id}_button`).style.display = 'none';
    document.querySelector(`#dislike_${post_id}_button`).style.display = 'none';
    return false;
}

function follow(profile_name) {
    fetch(`/follow/${profile_name}`, {
        method: 'POST'
    })
    let followers_count = document.querySelector('#profile-followersCount').innerHTML;
    followers_count ++;
    document.querySelector('#profile-followersCount').innerHTML = followers_count;
    document.querySelector('#profile-followButton').style.display = 'none';
    document.querySelector('#profile-unfollowButton').style.display = 'block';
    return false;
}

function unfollow(profile_name) {
    fetch(`/unfollow/${profile_name}`, {
        method: 'POST'
    })
    let followers_count = document.querySelector('#profile-followersCount').innerHTML;
    followers_count --;
    document.querySelector('#profile-followersCount').innerHTML = followers_count;
    document.querySelector('#profile-followButton').style.display = 'block';
    document.querySelector('#profile-unfollowButton').style.display = 'none';
    return false;
}
