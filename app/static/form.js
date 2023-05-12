function posting() {
    let url = $('#url').val();
    let comment = $('#comment').val();
    let star = $('#star').val();

    const data = {
        'url': url,
        'comment': comment,
        'rating': parseInt(star)
    }

    fetch('/movies/', {
      method: 'POST', // 또는 'PUT'
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
      console.log('성공:', data);
    })
}

// function open_box() {
//     $('#post-box').show()
// }
// function close_box() {
//     $('#post-box').hide()
// }