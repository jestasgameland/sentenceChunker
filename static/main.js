

function tagSentence(sentence) {

	$.ajax({
	    type : "GET",
	    url : "/getsentence",
	    data : sentence,
	    async : true,  

	    success : function(response) {
	    	
	    },
	    error: function(error) {
	    	document.body.innerHTML = error;
	    }
	});
}

/*

fetch('/getsentence')
  .then(function (response) {
      return response.json();
  }).then(function (text) {
      console.log('GET response:');
      console.log(text.greeting); 
  });

*/

 tagSentence("This is a test.");