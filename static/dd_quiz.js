$(document).ready(function(){
    const questionId = window.location.pathname.split('/').pop();
    const $quizForm = $('#quizForm.drag_drop'); // Target the drag_drop form
    const $feedbackMessage = $('#feedbackMessage');
    const $nextButton = $('#next-button');
    // Handle form submission via AJAX
    $quizForm.submit(function (e) {
        e.preventDefault();
        const formData = validateForm()
        if(!formData)
        {
            return
        }
        $.ajax({
            type: 'POST',
            url: '/quiz/' + questionId,
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.correct) {
                    $feedbackMessage.removeClass('alert-danger').addClass('alert-success').text('Congratulations, you got it correct!').show();
                } else {
                    $feedbackMessage.removeClass('alert-success').addClass('alert-danger').text('Incorrect. The answer is: '+ JSON.stringify(response.correct_answer)).show();
                }
                $nextButton.attr('href', '/quiz/' + (parseInt(questionId) + 1)).removeClass('d-none');
                $quizForm.find('button').prop('disabled', true);
            },
            error: function () {
                alert('An error occurred. Please try again.');
            }
        });
    });
});
function onDragStart(event)
{
    event.dataTransfer.setData("text", event.target.id)
}

function onDragOver(event)
{
    event.preventDefault()
}

function onDrop(event)
{
    event.preventDefault()
    $(event.target).removeClass("droperror")
    $(event.target).text(event.target.id)
    const data = event.dataTransfer.getData("text")
    event.target.appendChild(document.getElementById(data))

    hidden_input = document.getElementById(event.target.id + "_submit")
    hidden_input.value = event.target.children[0].id
    for(i = 1; i < event.target.children.length; i++)
    {
        hidden_input.value += ","+event.target.children[i].id
    }
}

function validateForm()
{
    let dropopt = []
    let it = document.getElementsByName('submission').entries()
    for(let i = 0; i < document.getElementsByName('submission').length; i++)
    {
        dropopt.push(it.next().value[1].id.split('_')[0])
    }
    submissions = {}
    for(let i = 0; i < dropopt.length; i++)
    {
        if(document.getElementById(dropopt[i]).children.length < 1)
        {
            while(i < dropopt.length)
            {
                if(document.getElementById(dropopt[i]).children.length < 1)
                {
                    $(document.getElementById(dropopt[i])).addClass("droperror")
                    $(document.getElementById(dropopt[i])).text(dropopt[i]+"\n*required")
                }
                i++
            }
            return false
        }
        else
        {
            submissions[dropopt[i]] = document.getElementById(dropopt[i] + "_submit").value
        }
    }
    return submissions
}