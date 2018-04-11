    var inputs = document.getElementsByClassName('status');
    for(var i = 0; i < inputs.length; i++)
    {
        inputs[i].onblur = function()
        {
            var empty = false;

            for(var j = 0; j < inputs.length; j++)
            {
                if(inputs[j].value == '')
                {
                    empty = true;
                    break;
                }                
            }

            if(!empty)
            {
                //console.log('submitting');
                document.getElementById("submitButton").submit();
            }
        }
    }