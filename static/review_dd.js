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
            url: '/review/' + questionId,
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.correct) {
                    $feedbackMessage.removeClass('alert-danger').addClass('alert-success').text('Congratulations, you got it correct!').show();
                } else {
                    $feedbackMessage.removeClass('alert-success').addClass('alert-danger').text('Incorrect. The answer is: ' + JSON.stringify(response.correct_answer)).show();
                }
                $nextButton.attr('href', '/learn/' + (parseInt(questionId) + 1)).removeClass('d-none');
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

    let target = event.target.draggable ? event.target.parentElement : event.target

    for(i = 0; i < target.classList.length; i++)
    {
        if(target.classList[i] == "droperror")
        {
            $(target).removeClass("droperror")
            $(target).text(target.id)
        }
    }

    let data = event.dataTransfer.getData("text")
    target.appendChild(document.getElementById(data))

    updateHiddenInput(target)
}

function updateHiddenInput(target)
{
    let hidden_input = document.getElementById(target.id + "_submit")
    if(hidden_input)
    {
        hidden_input.value = target.children[0].id
        for(i = 1; i < target.children.length; i++)
        {
            hidden_input.value += ","+target.children[i].id
        }
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
            updateHiddenInput(document.getElementById(dropopt[i]))
            submissions[dropopt[i]] = document.getElementById(dropopt[i] + "_submit").value
        }
    }
    return submissions
}