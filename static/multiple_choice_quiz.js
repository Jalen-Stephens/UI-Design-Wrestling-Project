$(document).ready(function() {
    const questionId = window.location.pathname.split('/').pop();
    const $quizForm = $('#quizForm.multiple_choice'); // Target the multiple_choice form
    const $feedbackMessage = $('#feedbackMessage');
    const $nextButton = $('#next-button');
    // Handle form submission via AJAX
    $quizForm.submit(function (e) {
        e.preventDefault();
        const formData =  $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/quiz/' + questionId,
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.correct) {
                    $feedbackMessage.removeClass('alert-danger').addClass('alert-success').text('Congratulations, you got it correct!').show();
                } else {
                    $feedbackMessage.removeClass('alert-success').addClass('alert-danger').text('Incorrect. The answer is: '+ response.correct_answer).show();
                }
                $nextButton.attr('href', '/quiz/' + (parseInt(questionId) + 1)).removeClass('d-none');
                $quizForm.find('input[type="radio"], button').prop('disabled', true); // Disable radio buttons and submit button
            },
            error: function () {
                alert('An error occurred. Please try again.');
            }
        });
    });
});