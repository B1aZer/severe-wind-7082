/*
* Author:      Marco Kuiper (http://www.marcofolio.net/)
*/

$(document).ready(function()
{

function isTouchDevice(){
	try{
		document.createEvent("TouchEvent");
		return true;
	}catch(e){
		return false;
	}
}

function touchScroll(id){
	if(isTouchDevice()){ //if touch events exist...
		var el=document.getElementById(id);
		var scrollStartPos=0;

		document.getElementById(id).addEventListener("touchstart", function(event) {
			scrollStartPos=this.scrollTop+event.touches[0].pageY;
			event.preventDefault();
		},false);

		document.getElementById(id).addEventListener("touchmove", function(event) {
			this.scrollTop=scrollStartPos-event.touches[0].pageY;
			event.preventDefault();
		},false);
	}
}


    $('#myCarousel').carousel({
        interval: 5200
    });

	$("#player").jPlayer({
		ready: function () {
			$(this).jPlayer("setMedia", {
                m4a: "http://www.jplayer.org/audio/m4a/TSP-01-Cro_magnon_man.m4a",
				oga: "/static/mp3/Dietro.ogg",
			}).jPlayer("play");
		},
		supplied: "m4a, oga",
		swfPath: "/static/js",
        wmode: "window"
	});
    

    /**
    * Set the size for each page to load
    */
    var pageSize = 20;

    /**
    * Username to load the timeline from
    */
    var username = 'marcofolio';

    /**
    * Variable for the current page
    */
    var currentPage = 1;
    var offSet = 0;

    // Appends the new tweet to the UI
    var appendTweet = function(tweet, id, access_token) {
        $.getJSON('https://api.vk.com/method/getProfiles?uid=' + id + '&fields=photo&access_token='+access_token+'&callback=?',function(data) {
            /*console.debug(data);*/
            $("<div class=\"row\" />")
            .append($("<div class=\"span3\" />")
            .append($("<blockquote />")
            .append($("<p />")
            .html(tweet)
            )
            .append($("<small />")
            .html(data['response'][0].first_name + " " + data['response'][0].last_name)
            )
            )
            )
            .append($("<div class=\"span1\" />")
            .append($("<a />")
            .attr("href", "http://twitter.com/" + username + "/status/" + id)
                .attr("title", "Go to Twitter status")
                .append($("<img />")
                .attr("src", data['response'][0].photo)
                )
            )
            )
            .appendTo($("#tweets"));
        });
    };

    // Loads the next tweets
    var loadTweets = function() {

        $.getJSON('/json/'+offSet,function(data) {
            /*console.debug(data);*/
            $.each(data['result'], function(i, post) {
                if (post.date <= 1334085077) {
                    /*$.getJSON('https://api.vk.com/method/getProfiles?uid=%s&fields=photo' % post.id ,function(data) { */
                        appendTweet(post.text, post.id, data['access_token']);
            /*});*/
                }
            });

            // We're done loading the tweets, so hide the overlay and update the UI
            $("#overlay").fadeOut();
            $("#pageCount").html(currentPage);
            $("#tweetCount").html(currentPage * pageSize);
        });

    };

    // First time, directly load the tweets
    loadTweets();
    touchScroll("tweets");

    // Append a scroll event handler to the container
    $("#tweets").scroll(function() {
        // We check if we're at the bottom of the scrollcontainer
        if ($(this)[0].scrollHeight - $(this).scrollTop() == $(this).outerHeight()) {
            // If we're at the bottom, show the overlay and retrieve the next page
            offSet=offSet+(currentPage * pageSize);
            currentPage++;

            if(currentPage > 3) {
                return false;
            }

            $("#overlay").fadeIn();
            loadTweets();
        }
    });

});
