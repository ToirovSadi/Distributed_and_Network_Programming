<div id="doc" class="markdown-body container-fluid comment-enabled comment-inner" data-hard-breaks="true">

# [<span class="octicon octicon-link"></span>](#Week-1---Stop-and-Wait-ARQ "Week-1---Stop-and-Wait-ARQ")<span>Week 1 -</span> [<span>Stop-and-Wait ARQ</span>](https://en.wikipedia.org/wiki/Stop-and-wait_ARQ)

> <span>Distributed Systems and Network Programming - Spring 2023</span>

## [<span class="octicon octicon-link"></span>](#Task "Task")<span>Task</span>

*   <span>Your task for this lab is to write a UDP server using Python</span> [<span>socket</span>](https://docs.python.org/3/library/socket.html) <span>module that communicates with a given client. The client reads a file from the local file system and uploads it to the server.</span>

### [<span class="octicon octicon-link"></span>](#Client-Implementation "Client-Implementation")<span>Client Implementation</span>

*   <span>The client starts by sending the following string message</span> `s|0|filename.ext|filesize` <span>where:</span>
    *   `s` <span>indicates that the message type is</span> `start`
    *   `|` <span>is the field delimiter.</span>
    *   `0` <span>is the initial sequence number.</span>
    *   `filename.ext` <span>is the name of the file to be sent (with extension).</span>
    *   `filesize` <span>is the total size of the file to be sent</span> <u><span>in bytes</span></u><span>.</span>
*   <span>The client expects a reply from the server in the format</span> `a|seqno` <span>where:</span>
    *   `a` <span>indicates that the message type is</span> `acknowledgement`<span>.</span>
    *   `seqno` <span>equals</span> `(x+1)%2` <span>where</span> `x` <span>is the sequence number of the message to be acknowledged.</span>
*   <span>If the expected server acknowledgement was received successfully, the client does the following:</span>
    1.  <span>Divide the file into chunks so that the size of a single data packet (including headers) does not exceed the buffer size of the server.</span>
    2.  <span>Start sending file chunks, one by one. Each message has the format</span> `d|seqno|data` <span>where:</span>
        *   `d` <span>indicates that the message type is</span> `data`
        *   `seqno` <span>is the sequence number of the data message, it alternates between</span> `1` <span>and</span> `0`<span>, starting from</span> `1`<span>.</span>
        *   `data` <span>is the raw bytes of the file.</span>
    3.  <span>The client waits for an acknowledgement message after sending each chunk.</span>
*   <span>If an expected acknowledgement message does not arrive within 1 second, the client retransmits the message.</span>
*   <span>If an acknowledgement message arrives with an unexpected sequence number, the client ignores that duplicate ACK and keeps waiting for the expected ACK.</span>

### [<span class="octicon octicon-link"></span>](#Server-Implementation-your-task "Server-Implementation-your-task")<span>Server Implementation (your task)</span>

1.  <span>Parse one integer argument, the port number to listen on.</span>
2.  <span>Create a UDP socket and start listening for incoming messages on</span> `0.0.0.0:<port>`<span>.</span>
    *   <span>The server should use a fixed receiver buffer size of</span> `20480` <span>bytes (20 Kibibytes).</span>
3.  <span>Upon receiving a message from a client, inspect the message type (first character).</span>
    *   <span>If the message type is</span> `s`<span>, prepare to receive a file from the client with the given name and size.</span>
    *   <span>If the message type is</span> `d`<span>, write the delivered chunk to the file system.</span>
    *   <span>Otherwise, terminate gracefully with an error.</span>
4.  <span>In both cases, reply with an acknowledge message in the format</span> `a|seqno` <span>where</span>
    *   `a` <span>indicates that the message type is</span> `acknowledgement`<span>.</span>
    *   `seqno` <span>equals</span> `(x+1)%2` <span>where</span> `x` <span>is the sequence number of the message to be acknowledged.</span>
5.  <span>Once the file is received completely, the server should print an indicating message, write the content to the file system, and close the file.</span>
6.  <span>If an existing file with the same name is present in the server directory, the server should print an indicating message and overwrite that file with the new one.</span>
7.  <span>Your server will be tested under constant delay and packet loss. The following Linux command can be used to simulate 15% packet loss and 1100 milliseconds constant delay over the</span> `lo` <span>interface. File transfer should still succeed after applying the command. To undo the effect use</span> `del` <span>instead of</span> `add`<span>.</span>

        sudo tc qdisc add dev lo root netem loss 15% delay 1100ms

8.  <span>The server stays running unless a fatal error occurs or a</span> `KeyboardInterrupt` <span>is received.</span>

## [<span class="octicon octicon-link"></span>](#Testing "Testing")<span>Testing</span>

*   <span>The project structure looks like this</span>

        .
        ├── client
        │   ├── client.py
        │   ├── image.png
        │   └── note.txt
        └── NameSurname.py

*   <span>Example run and output</span>

        $ python3 NameSurname.py 8080
        ('0.0.0.0', 8080):    Listening...
        ('127.0.0.1', 48256): s|0|note.txt|446
        ('127.0.0.1', 48256): d|1|chunk1
        ('0.0.0.0', 8080):    Received note.txt.
        ^C('0.0.0.0', 8080):  Shutting down...

        $ cd client
        $ python3 client.py 127.0.0.1:8080 note.txt
        Client: s|0|note.txt|446
        Server: a|1
        Client: d|1|chunk1
        Server: a|0

*   <span>Example session visualization</span>

<pre class="mermaid" data-processed="true"><svg aria-labelledby="chart-title-mermaid-1679825177500 chart-desc-mermaid-1679825177500" role="img" viewBox="-50 -10 472 347" style="max-width: 472px;" height="347" xmlns="http://www.w3.org/2000/svg" width="100%" id="mermaid-1679825177500"><style>#mermaid-1679825177500 {font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#mermaid-1679825177500 .error-icon{fill:#552222;}#mermaid-1679825177500 .error-text{fill:#552222;stroke:#552222;}#mermaid-1679825177500 .edge-thickness-normal{stroke-width:2px;}#mermaid-1679825177500 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1679825177500 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1679825177500 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1679825177500 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1679825177500 .marker{fill:#333333;stroke:#333333;}#mermaid-1679825177500 .marker.cross{stroke:#333333;}#mermaid-1679825177500 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1679825177500 .actor{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#mermaid-1679825177500 text.actor>tspan{fill:black;stroke:none;}#mermaid-1679825177500 .actor-line{stroke:grey;}#mermaid-1679825177500 .messageLine0{stroke-width:1.5;stroke-dasharray:none;stroke:#333;}#mermaid-1679825177500 .messageLine1{stroke-width:1.5;stroke-dasharray:2,2;stroke:#333;}#mermaid-1679825177500 #arrowhead path{fill:#333;stroke:#333;}#mermaid-1679825177500 .sequenceNumber{fill:white;}#mermaid-1679825177500 #sequencenumber{fill:#333;}#mermaid-1679825177500 #crosshead path{fill:#333;stroke:#333;}#mermaid-1679825177500 .messageText{fill:#333;stroke:#333;}#mermaid-1679825177500 .labelBox{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#mermaid-1679825177500 .labelText,#mermaid-1679825177500 .labelText>tspan{fill:black;stroke:none;}#mermaid-1679825177500 .loopText,#mermaid-1679825177500 .loopText>tspan{fill:black;stroke:none;}#mermaid-1679825177500 .loopLine{stroke-width:2px;stroke-dasharray:2,2;stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);}#mermaid-1679825177500 .note{stroke:#aaaa33;fill:#fff5ad;}#mermaid-1679825177500 .noteText,#mermaid-1679825177500 .noteText>tspan{fill:black;stroke:none;}#mermaid-1679825177500 .activation0{fill:#f4f4f4;stroke:#666;}#mermaid-1679825177500 .activation1{fill:#f4f4f4;stroke:#666;}#mermaid-1679825177500 .activation2{fill:#f4f4f4;stroke:#666;}#mermaid-1679825177500 .actorPopupMenu{position:absolute;}#mermaid-1679825177500 .actorPopupMenuPanel{position:absolute;fill:#ECECFF;box-shadow:0px 8px 16px 0px rgba(0,0,0,0.2);filter:drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4));}#mermaid-1679825177500 .actor-man line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;}#mermaid-1679825177500 .actor-man circle,#mermaid-1679825177500 line{stroke:hsl(259.6261682243, 59.7765363128%, 87.9019607843%);fill:#ECECFF;stroke-width:2px;}#mermaid-1679825177500 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><g id="root-0"><text style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: &quot;Open Sans&quot;, sans-serif;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="75"><tspan dy="0" x="75">Client</tspan></text></g></g><g><g id="root-1"><text style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: &quot;Open Sans&quot;, sans-serif;" class="actor" alignment-baseline="central" dominant-baseline="central" y="32.5" x="297"><tspan dy="0" x="297">Server</tspan></text></g></g><text style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="80" x="186">s | 0 | note.txt | 2000</text><text style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="124" x="186">a | 1</text><text style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="168" x="186">d | 1 | chunk1</text><text style="font-family: &quot;trebuchet ms&quot;, verdana, arial, sans-serif; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="212" x="186">a | 0</text><g><text style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: &quot;Open Sans&quot;, sans-serif;" class="actor" alignment-baseline="central" dominant-baseline="central" y="293.5" x="75"><tspan dy="0" x="75">Client</tspan></text></g><g><text style="text-anchor: middle; font-size: 14px; font-weight: 400; font-family: &quot;Open Sans&quot;, sans-serif;" class="actor" alignment-baseline="central" dominant-baseline="central" y="293.5" x="297"><tspan dy="0" x="297">Server</tspan></text></g></svg></pre>

*   <span>Resulting directory structure. The text file should arrive intact.</span>

        .
        ├── client
        │   ├── client.py
        │   ├── image.png
        │   └── note.txt
        ├── NameSurname.py
        └── note.txt

## [<span class="octicon octicon-link"></span>](#Checklist "Checklist")<span>Checklist</span>

<span>Your submitted code should satisfy the following requirements. Failing to satisfy an item will result in partial grade deduction or an assignment failure (depending on the severity).</span>

*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>One submitted source file named according to the format</span> `NameSurname.py`
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code executes successfully under the</span> [<span>latest stable Python interpreter</span>](https://www.python.org/downloads/)<span>.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code only imports dependencies from the</span> [<span>standard library</span>](https://docs.python.org/3/library/index.html) <span>(no external dependencies).</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>A sent text/binary file and the corresponding received one are identical (files do not get corrupted in transit).</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code works under constant delay and packet loss.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code is readable and nicely formatted (e.g., according to</span> [<span>PEP8</span>](https://peps.python.org/pep-0008/)<span>)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code is the author’s original work. Both parties will be penalized for detected plagiarism.</span>

</div>

<div class="ui-toc dropup unselectable hidden-print" style="display:none;">

<div class="pull-right dropdown">[](# "Table of content")

<div class="toc">

- [Week 1 - Stop-and-Wait ARQ](#week-1---stop-and-wait-arq)
  - [Task](#task)
    - [Client Implementation](#client-implementation)
    - [Server Implementation (your task)](#server-implementation-your-task)
  - [Testing](#testing)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

</div>

<div id="ui-toc-affix" class="ui-affix-toc ui-toc-dropdown unselectable hidden-print" data-spy="affix" style="top:17px;display:none;" null="">

<div class="toc">

- [Week 1 - Stop-and-Wait ARQ](#week-1---stop-and-wait-arq)
  - [Task](#task)
    - [Client Implementation](#client-implementation)
    - [Server Implementation (your task)](#server-implementation-your-task)
  - [Testing](#testing)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

<script>var markdown = $(".markdown-body"); //smooth all hash trigger scrolling function smoothHashScroll() { var hashElements = $("a[href^='#']").toArray(); for (var i = 0; i < hashElements.length; i++) { var element = hashElements[i]; var $element = $(element); var hash = element.hash; if (hash) { $element.on('click', function (e) { // store hash var hash = this.hash; if ($(hash).length <= 0) return; // prevent default anchor click behavior e.preventDefault(); // animate $('body, html').stop(true, true).animate({ scrollTop: $(hash).offset().top }, 100, "linear", function () { // when done, add hash to url // (default click behaviour) window.location.hash = hash; }); }); } } } smoothHashScroll(); var toc = $('.ui-toc'); var tocAffix = $('.ui-affix-toc'); var tocDropdown = $('.ui-toc-dropdown'); //toc tocDropdown.click(function (e) { e.stopPropagation(); }); var enoughForAffixToc = true; function generateScrollspy() { $(document.body).scrollspy({ target: '' }); $(document.body).scrollspy('refresh'); if (enoughForAffixToc) { toc.hide(); tocAffix.show(); } else { tocAffix.hide(); toc.show(); } $(document.body).scroll(); } function windowResize() { //toc right var paddingRight = parseFloat(markdown.css('padding-right')); var right = ($(window).width() - (markdown.offset().left + markdown.outerWidth() - paddingRight)); toc.css('right', right + 'px'); //affix toc left var newbool; var rightMargin = (markdown.parent().outerWidth() - markdown.outerWidth()) / 2; //for ipad or wider device if (rightMargin >= 133) { newbool = true; var affixLeftMargin = (tocAffix.outerWidth() - tocAffix.width()) / 2; var left = markdown.offset().left + markdown.outerWidth() - affixLeftMargin; tocAffix.css('left', left + 'px'); } else { newbool = false; } if (newbool != enoughForAffixToc) { enoughForAffixToc = newbool; generateScrollspy(); } } $(window).resize(function () { windowResize(); }); $(document).ready(function () { windowResize(); generateScrollspy(); }); //remove hash function removeHash() { window.location.hash = ''; } var backtotop = $('.back-to-top'); var gotobottom = $('.go-to-bottom'); backtotop.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToTop) scrollToTop(); removeHash(); }); gotobottom.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToBottom) scrollToBottom(); removeHash(); }); var toggle = $('.expand-toggle'); var tocExpand = false; checkExpandToggle(); toggle.click(function (e) { e.preventDefault(); e.stopPropagation(); tocExpand = !tocExpand; checkExpandToggle(); }) function checkExpandToggle () { var toc = $('.ui-toc-dropdown .toc'); var toggle = $('.expand-toggle'); if (!tocExpand) { toc.removeClass('expand'); toggle.text('Expand all'); } else { toc.addClass('expand'); toggle.text('Collapse all'); } } function scrollToTop() { $('body, html').stop(true, true).animate({ scrollTop: 0 }, 100, "linear"); } function scrollToBottom() { $('body, html').stop(true, true).animate({ scrollTop: $(document.body)[0].scrollHeight }, 100, "linear"); }</script>