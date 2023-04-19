<div id="doc" class="markdown-body container-fluid comment-inner comment-enabled" data-hard-breaks="true">

# [<span class="octicon octicon-link"></span>](#Week-4---Remote-Procedure-Call "Week-4---Remote-Procedure-Call")<span>Week 4 - Remote Procedure Call</span>

> <span>Distributed Systems and Network Programming - Spring 2023</span>

## [<span class="octicon octicon-link"></span>](#Overview "Overview")<span>Overview</span>

<span>Your task for this lab is to use</span> [<span>gRPC</span>](https://grpc.io/docs/what-is-grpc/core-concepts/) <span>to remotely call functions defined on a server.</span>

*   <span>The client calls stub functions to do some CRUD operations against a SQLite database.</span>
*   <span>The server executes the corresponding implementations to modify the database content.</span>
*   <span>Communication happens over the network, with</span> [<span>Protocol Buffers</span>](https://protobuf.dev/overview/) <span>as the data serialization format.</span>

## [<span class="octicon octicon-link"></span>](#Remote-Functions "Remote-Functions")<span>Remote Functions</span>

<span>The server should expose the following functions for RPC, the logic for each function is explained below:</span>

*   `PutUser(user_id: int, user_name: str)`

    *   <span>Update the entry for the user with</span> `user_id` <span>to have the specified</span> `user_name`
    *   <span>If such user does not exist, create one and insert it into the database</span>
    *   <span>Return</span> `True` <span>on success and</span> `False` <span>on failure</span>
*   `DeleteUser(user_id: int)`

    *   <span>Delete the entry for the user with the supplied</span> `user_id`
    *   <span>Return</span> `True` <span>on success and</span> `False` <span>on failure</span>
*   `GetUsers()`

    *   <span>Return a list of user objects (all users in the database).</span>
    *   <span>Each object should have two accessible properties named</span> `user_id` <span>and</span> `user_name`

## [<span class="octicon octicon-link"></span>](#Task "Task")<span>Task</span>

1.  <span>Create a Python virtual environment and install the required external dependencies</span>

        python3 -m venv venv
        source venv/bin/activate
        pip3 install grpcio grpcio-tools

2.  <span>Create</span> `schema.proto` <span>which defines the following:</span>

    *   <span>The database</span> `service` <span>with remote functions that can be called through</span> `rpc`<span>.</span>
    *   <span>Request/response</span> `message` <span>format for the client/server communication.</span>
3.  <span>Compile the schema file to generate the stub and service source files (</span>`schema_pb2_grpc.py` <span>and</span> `schema_pb2.py`<span>) using the following command:</span>

        python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. schema.proto

4.  <span>Write the gRPC server code to do the following:</span>

    *   <span>Create or overwrite a local database file</span> `db.sqlite` <span>in the current directory.</span>
    *   <span>Initialize the database with an empty table</span> `Users(id INTEGER, name STRING)`
    *   <span>Create a</span> `grpc.server` <span>that listens forever for client RPC requests and executes them.</span>
        *   <span>The server should terminate gracefully whenever a</span> `KeyboardInterrupt` <span>is received.</span>
        *   <span>Upon receiving a request from the client, the server should print the name of the function to be executed along with the supplied arguments.</span>
    *   <span>Implement the functions for</span> `PutUser`<span>,</span> `DeleteUser`<span>, and</span> `GetUsers` <span>as explained above.</span>
5.  <span>Run your gRPC server, then run the given client (you are not supposed to modify the client).</span>

6.  <span>Verify that the database was populated by inspecting the file</span> `db.sqlite` <span>using your favorite SQLite viewer tool/extension.</span>

## [<span class="octicon octicon-link"></span>](#Example-Run "Example-Run")<span>Example Run</span>

    $ python3 server.py
    gRPC server is listening on 0.0.0.0:1234
    PutUser(1, 'User1')
    PutUser(2, 'User2')
    PutUser(3, 'User3')
    PutUser(4, 'User4')
    PutUser(2, 'User2_updated')
    DeleteUser(3)
    GetUsers()

    $ python3 client.py
    PutUser(1, 'User1') = True
    PutUser(2, 'User2') = True
    PutUser(3, 'User3') = True
    PutUser(4, 'User4') = True
    PutUser(2, 'User2_updated') = True
    DeleteUser(3) = True
    GetUsers() = {1: 'User1', 2: 'User2_updated', 4: 'User4'}

## [<span class="octicon octicon-link"></span>](#Checklist "Checklist")<span>Checklist</span>

*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>A single submitted file (</span>`NameSurname.zip`<span>) containing only</span> `server.py` <span>and</span> `schema.proto`
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code is formatted and does not use any external dependencies (apart from</span> `grpc`<span>)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The</span> `schema.proto` <span>file correctly compiles without errors or warnings.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The server code executes successfully and prints the expected output.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The created database file</span> `db.sqlite` <span>contains the expected data after applying all queries.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code is the author’s original work. Both parties will be penalized for detected plagiarism</span>

</div>

<div class="ui-toc dropup unselectable hidden-print" style="display:none;">

<div class="pull-right dropdown">[](# "Table of content")

<div class="toc">

- [Week 4 - Remote Procedure Call](#week-4---remote-procedure-call)
  - [Overview](#overview)
  - [Remote Functions](#remote-functions)
  - [Task](#task)
  - [Example Run](#example-run)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

</div>

<div id="ui-toc-affix" class="ui-affix-toc ui-toc-dropdown unselectable hidden-print" data-spy="affix" style="top:17px;display:none;" null="">

<div class="toc">

- [Week 4 - Remote Procedure Call](#week-4---remote-procedure-call)
  - [Overview](#overview)
  - [Remote Functions](#remote-functions)
  - [Task](#task)
  - [Example Run](#example-run)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

<script>var markdown = $(".markdown-body"); //smooth all hash trigger scrolling function smoothHashScroll() { var hashElements = $("a[href^='#']").toArray(); for (var i = 0; i < hashElements.length; i++) { var element = hashElements[i]; var $element = $(element); var hash = element.hash; if (hash) { $element.on('click', function (e) { // store hash var hash = this.hash; if ($(hash).length <= 0) return; // prevent default anchor click behavior e.preventDefault(); // animate $('body, html').stop(true, true).animate({ scrollTop: $(hash).offset().top }, 100, "linear", function () { // when done, add hash to url // (default click behaviour) window.location.hash = hash; }); }); } } } smoothHashScroll(); var toc = $('.ui-toc'); var tocAffix = $('.ui-affix-toc'); var tocDropdown = $('.ui-toc-dropdown'); //toc tocDropdown.click(function (e) { e.stopPropagation(); }); var enoughForAffixToc = true; function generateScrollspy() { $(document.body).scrollspy({ target: '' }); $(document.body).scrollspy('refresh'); if (enoughForAffixToc) { toc.hide(); tocAffix.show(); } else { tocAffix.hide(); toc.show(); } $(document.body).scroll(); } function windowResize() { //toc right var paddingRight = parseFloat(markdown.css('padding-right')); var right = ($(window).width() - (markdown.offset().left + markdown.outerWidth() - paddingRight)); toc.css('right', right + 'px'); //affix toc left var newbool; var rightMargin = (markdown.parent().outerWidth() - markdown.outerWidth()) / 2; //for ipad or wider device if (rightMargin >= 133) { newbool = true; var affixLeftMargin = (tocAffix.outerWidth() - tocAffix.width()) / 2; var left = markdown.offset().left + markdown.outerWidth() - affixLeftMargin; tocAffix.css('left', left + 'px'); } else { newbool = false; } if (newbool != enoughForAffixToc) { enoughForAffixToc = newbool; generateScrollspy(); } } $(window).resize(function () { windowResize(); }); $(document).ready(function () { windowResize(); generateScrollspy(); }); //remove hash function removeHash() { window.location.hash = ''; } var backtotop = $('.back-to-top'); var gotobottom = $('.go-to-bottom'); backtotop.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToTop) scrollToTop(); removeHash(); }); gotobottom.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToBottom) scrollToBottom(); removeHash(); }); var toggle = $('.expand-toggle'); var tocExpand = false; checkExpandToggle(); toggle.click(function (e) { e.preventDefault(); e.stopPropagation(); tocExpand = !tocExpand; checkExpandToggle(); }) function checkExpandToggle () { var toc = $('.ui-toc-dropdown .toc'); var toggle = $('.expand-toggle'); if (!tocExpand) { toc.removeClass('expand'); toggle.text('Expand all'); } else { toc.addClass('expand'); toggle.text('Collapse all'); } } function scrollToTop() { $('body, html').stop(true, true).animate({ scrollTop: 0 }, 100, "linear"); } function scrollToBottom() { $('body, html').stop(true, true).animate({ scrollTop: $(document.body)[0].scrollHeight }, 100, "linear"); }</script>