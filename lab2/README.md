<div id="doc" class="markdown-body container-fluid comment-inner comment-enabled" data-hard-breaks="true">

# [<span class="octicon octicon-link"></span>](#Week-2---Concurrency-and-Parallelism "Week-2---Concurrency-and-Parallelism")<span>Week 2 - Concurrency and Parallelism</span>

> <span>Distributed Systems and Network Programming - Spring 2023</span>

## [<span class="octicon octicon-link"></span>](#Task "Task")<span>Task</span>

<span>Your tasks for this lab:</span>

*   <span>Write a multi-threaded TCP server that communicates with a given client</span>
*   <span>Optimize the runtime of the client using</span> [<span>threading</span>](https://docs.python.org/3/library/threading.html) <span>and</span> [<span>multiprocessing</span>](https://docs.python.org/3/library/multiprocessing.html)

## [<span class="octicon octicon-link"></span>](#Server-Implementation "Server-Implementation")<span>Server Implementation</span>

*   **<span>The server should do the following:</span>**
    1.  <span>Accept a client connection</span>
    2.  <span>Spawn a new thread to handle the connection</span>
    3.  <span>Generate a random 10x10 image (you can use</span> [<span>pillow</span>](https://python-pillow.org/) <span>module for that)</span>
    4.  <span>Send the image to the connected client, then close that connection</span>
*   **<span>Additional requirements:</span>**
    *   <span>The server should stay listening all the time and should not terminate unless a</span> `KeyboardInterrupt` <span>is received.</span>
    *   <span>The server should be able to handle multiple connections simultaneously.</span>
    *   <span>The server socket is marked for address reuse so that the OS would immediately release the bound address after server termination. You can do so by calling the</span> `setsockopt` <span>on the server socket before binding the address as follows:</span>

            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((SERVER_IP, SERVER_PORT))

## [<span class="octicon octicon-link"></span>](#Client-Implementation "Client-Implementation")<span>Client Implementation</span>

**<span>The client does the following:</span>**

1.  <span>Connect to the TCP server multiple times to download 5000 images, one by one.</span>
2.  <span>Download the images to a directory called</span> `frames` <span>(creating the directory if it does not exist).</span>
3.  <span>Create a GIF by combining the downloaded frames.</span>
4.  <span>Use</span> [<span>time</span>](https://docs.python.org/3/library/time.html) <span>module to calculate the total time taken for frame download and GIF generation.</span>

## [<span class="octicon octicon-link"></span>](#Your-task "Your-task")<span>Your task</span>

1.  <span>Once you understand how the client code works, start by writing the server.</span>
2.  <span>Once the server works fine. It’s time to optimize the runtime of the client.</span>
3.  <span>Use</span> `threading` <span>to spawn multiple threads that download the required frames concurrently.</span>
4.  <span>Use</span> `multiprocessing` <span>to spawn multiple processes (not more that your CPU core count) to process the frames in parallel to create the GIF faster. You may use</span> `multiprocessing.Pool()` <span>to achieve the task.</span>
5.  <span>Check the time taken in each stage and verify that the client runtime was improved.</span>

## [<span class="octicon octicon-link"></span>](#Example-run "Example-run")<span>Example run</span>

    $ python3 NameSurname_server.py
    Listening on 0.0.0.0:1234
    Sent an image to (127.0.0.1, 50125)
    Sent an image to (127.0.0.1, 58754)
    ...

    # Before optimizing client
    $ python3 NameSurname_client.py
    Frames download time: 25.516422748565674
    GIF creation time: 30.278062343597412

    # After optimizing client
    $ python3 NameSurname_client.py
    Frames download time: 18.751099348068237
    GIF creation time: 9.695139408111572

## [<span class="octicon octicon-link"></span>](#Checklist "Checklist")<span>Checklist</span>

<span>Your submitted code should satisfy the following requirements. Failing to satisfy an item will result in partial grade deduction or an assignment failure (depending on the severity).</span>

*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Two submitted files named according to the format</span> `NameSurname_client.py` <span>and</span> `NameSurname_server.py`
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code executes successfully under the</span> [<span>latest stable Python interpreter</span>](https://www.python.org/downloads/)<span>.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code does not use any external dependencies (apart from</span> [<span>pillow</span>](https://python-pillow.org/)<span>)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code is readable and nicely formatted (e.g., according to</span> [<span>PEP8</span>](https://peps.python.org/pep-0008/)<span>)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The client runtime is improved after using</span> `threading` <span>and</span> `multiprocessing`
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code is the author’s original work. Both parties will be penalized for detected plagiarism.</span>

</div>

<div class="ui-toc dropup unselectable hidden-print" style="display:none;">

<div class="pull-right dropdown">[](# "Table of content")

<div class="toc">

- [Week 2 - Concurrency and Parallelism](#week-2---concurrency-and-parallelism)
  - [Task](#task)
  - [Server Implementation](#server-implementation)
  - [Client Implementation](#client-implementation)
  - [Your task](#your-task)
  - [Example run](#example-run)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

</div>

<div id="ui-toc-affix" class="ui-affix-toc ui-toc-dropdown unselectable hidden-print" data-spy="affix" style="top:17px;display:none;" null="">

<div class="toc">

- [Week 2 - Concurrency and Parallelism](#week-2---concurrency-and-parallelism)
  - [Task](#task)
  - [Server Implementation](#server-implementation)
  - [Client Implementation](#client-implementation)
  - [Your task](#your-task)
  - [Example run](#example-run)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

<script>var markdown = $(".markdown-body"); //smooth all hash trigger scrolling function smoothHashScroll() { var hashElements = $("a[href^='#']").toArray(); for (var i = 0; i < hashElements.length; i++) { var element = hashElements[i]; var $element = $(element); var hash = element.hash; if (hash) { $element.on('click', function (e) { // store hash var hash = this.hash; if ($(hash).length <= 0) return; // prevent default anchor click behavior e.preventDefault(); // animate $('body, html').stop(true, true).animate({ scrollTop: $(hash).offset().top }, 100, "linear", function () { // when done, add hash to url // (default click behaviour) window.location.hash = hash; }); }); } } } smoothHashScroll(); var toc = $('.ui-toc'); var tocAffix = $('.ui-affix-toc'); var tocDropdown = $('.ui-toc-dropdown'); //toc tocDropdown.click(function (e) { e.stopPropagation(); }); var enoughForAffixToc = true; function generateScrollspy() { $(document.body).scrollspy({ target: '' }); $(document.body).scrollspy('refresh'); if (enoughForAffixToc) { toc.hide(); tocAffix.show(); } else { tocAffix.hide(); toc.show(); } $(document.body).scroll(); } function windowResize() { //toc right var paddingRight = parseFloat(markdown.css('padding-right')); var right = ($(window).width() - (markdown.offset().left + markdown.outerWidth() - paddingRight)); toc.css('right', right + 'px'); //affix toc left var newbool; var rightMargin = (markdown.parent().outerWidth() - markdown.outerWidth()) / 2; //for ipad or wider device if (rightMargin >= 133) { newbool = true; var affixLeftMargin = (tocAffix.outerWidth() - tocAffix.width()) / 2; var left = markdown.offset().left + markdown.outerWidth() - affixLeftMargin; tocAffix.css('left', left + 'px'); } else { newbool = false; } if (newbool != enoughForAffixToc) { enoughForAffixToc = newbool; generateScrollspy(); } } $(window).resize(function () { windowResize(); }); $(document).ready(function () { windowResize(); generateScrollspy(); }); //remove hash function removeHash() { window.location.hash = ''; } var backtotop = $('.back-to-top'); var gotobottom = $('.go-to-bottom'); backtotop.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToTop) scrollToTop(); removeHash(); }); gotobottom.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToBottom) scrollToBottom(); removeHash(); }); var toggle = $('.expand-toggle'); var tocExpand = false; checkExpandToggle(); toggle.click(function (e) { e.preventDefault(); e.stopPropagation(); tocExpand = !tocExpand; checkExpandToggle(); }) function checkExpandToggle () { var toc = $('.ui-toc-dropdown .toc'); var toggle = $('.expand-toggle'); if (!tocExpand) { toc.removeClass('expand'); toggle.text('Expand all'); } else { toc.addClass('expand'); toggle.text('Collapse all'); } } function scrollToTop() { $('body, html').stop(true, true).animate({ scrollTop: 0 }, 100, "linear"); } function scrollToBottom() { $('body, html').stop(true, true).animate({ scrollTop: $(document.body)[0].scrollHeight }, 100, "linear"); }</script>
