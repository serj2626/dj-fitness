
// Add Review for post
const addComment = (user, id) => {
    document.getElementById('parentID').value = id
    document.getElementById('commentID').innerText = `${user}, `
}

const like = document.getElementById('likeID')
const dislike = document.getElementById('dislikeID')
const arr = [like, dislike]

arr.forEach(element => {
    element.addEventListener('mouseover', () => {
        element.style['background-color'] =  'gray'
        element.style['opacity'] = 0.5
    })
});

arr.forEach(element => {
    element.addEventListener('mouseout', () => {
        element.style['background-color'] =  'white'
        element.style['opacity'] = 1
    })
});


// End Review for post
