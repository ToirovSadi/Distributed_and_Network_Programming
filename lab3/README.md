<div id="doc" class="markdown-body container-fluid comment-inner comment-enabled" data-hard-breaks="true">

# [<span class="octicon octicon-link"></span>](#Week-3---Message-Brokers "Week-3---Message-Brokers")<span>Week 3 - Message Brokers</span>

> <span>Distributed Systems and Network Programming - Spring 2023</span>

## [<span class="octicon octicon-link"></span>](#Overview "Overview")<span>Overview</span>

<span>Your task for this lab is to use</span> [<span>RabbitMQ</span>](https://rabbitmq.com/) <span>as a message broker for a pollution monitoring system.</span>

*   <span>A sensor</span> **<span>(publisher)</span>** <span>collects CO</span><sub><span>2</span></sub> <span>levels in the environment and sends the obtained values to a server.</span>
*   <span>The server</span> **<span>(subscriber)</span>** <span>processes these values and indicates if CO</span><sub><span>2</span></sub> <span>levels are abnormal.</span>

## [<span class="octicon octicon-link"></span>](#System-Architecture "System-Architecture")<span>System Architecture</span>

### [<span class="octicon octicon-link"></span>](#Architecture-diagram "Architecture-diagram")**<span>Architecture diagram</span>**

![diagram](https://user-images.githubusercontent.com/40727318/229937239-2c27b9f4-e484-4eb9-b174-768ed8102b75.svg)

### [<span class="octicon octicon-link"></span>](#Directory-structure "Directory-structure")**<span>Directory structure</span>**

    .
    ├── docker-compose.yml
    ├── publishers
    │   ├── sensor.py
    │   └── control-tower.py
    └── subscribers
        ├── receiver.py
        └── reporter.py

### [<span class="octicon octicon-link"></span>](#Publishers "Publishers")**<span>Publishers</span>**

*   **<span>Sensor (</span>`sensor.py`<span>)</span>**

    *   <span>Reads user input (an integer) representing the current level of CO</span><sub><span>2</span></sub><span>.</span>
    *   <span>Sends the value along with the current time to the server in JSON format.</span>
        *   <span>Values should be sent to the CO2 queue for processing only by the receiver</span>
    *   <span>Example message:</span> `{"time": "2023-04-03 17:19:29", "value": 500}`
*   **<span>Control tower (</span>`control-tower.py`<span>)</span>**

    *   <span>Takes user input (a string) representing a query to the reporter.</span>
    *   <span>The query can either be</span> `current` <span>or</span> `average`
        *   `current`<span>: asks for the current CO</span><sub><span>2</span></sub> <span>level.</span>
        *   `average`<span>: asks for the average of all collected values since the system started.</span>

### [<span class="octicon octicon-link"></span>](#Subscribers "Subscribers")**<span>Subscribers</span>**

*   **<span>Receiver (</span>`receiver.py`<span>)</span>**
    *   <span>Listens for messages from the sensor.</span>
    *   <span>Extracts the received JSON data and appends it to a file (e.g.,</span> `receiver.log`<span>).</span>
    *   <span>Checks the received (latest) CO</span><sub><span>2</span></sub> <span>value</span>
        *   <span>If the value is larger than</span> `500`<span>, the server prints a</span> `WARNING` <span>message.</span>
        *   <span>Otherwise, print</span> `OK`
*   **<span>Reporter (</span>`reporter.py`<span>)</span>**
    *   <span>Listens for messages (queries) from the control tower.</span>
    *   <span>Prints the answer upon receiving a query for</span> `current` <span>or</span> `average`<span>.</span>
    *   <span>The answer can be calculated based on the data from</span> `receiver.log`

### [<span class="octicon octicon-link"></span>](#Message-Broker-RabbitMQ-Server "Message-Broker-RabbitMQ-Server")<span>Message Broker (RabbitMQ Server)</span>

*   <span>The broker is maintaining one or more message queues.</span>
*   <span>Producers push messages to queues for consumers to receive.</span>
*   <span>An exchange controls which messages should be routed to which queues and how it’s done.</span>
    *   <span>Multiple exchange types exist, use the</span> `topic` <span>exchange type which allows routing messages to different queues based on a wildcard (</span>`*`<span>) routing pattern.</span>
*   <span>A binding connects the exchange to a certain queue, the diagram above shows which queues should be bound to the exchange and the routing patterns to use.</span>

## [<span class="octicon octicon-link"></span>](#Task "Task")<span>Task</span>

1.  <span>Run RabbitMQ in a docker container using</span> [<span>docker-compose</span>](https://docs.docker.com/compose/install/) <span>by executing the following command in the same directory as</span> `docker-compose.yml` <span>file.</span>

        docker-compose up

2.  <span>The Web UI should be available at</span> [<span>http://localhost:15672/</span>](http://localhost:15672/)

    *   <span>You can see default login credentials (</span>`rabbit:1234`<span>) in the compose file.</span>
3.  <span>Install</span> [`pika`](https://pypi.org/project/pika/)<span>, the Python library for interacting with RabbitMQ.</span>

    *   <span>It’s recommended to create a virtual environment instead of installing</span> `pika` <span>globally.</span>
    *   <span>You can do so by running the following commands (you may need to install</span> `python3-venv`<span>)</span>

            python -m venv venv
            source venv/bin/activate
            pip install pika

4.  <span>Implement the system components as described above. Refer to</span> [<span>this tutorial</span>](https://www.rabbitmq.com/tutorials/tutorial-three-python.html) <span>and</span> [<span>pika documentation</span>](https://pika.readthedocs.io/en/stable/index.html) <span>for help.</span>

    *   <span>Connect to RabbitMQ server at</span> `localhost` <span>and create a channel.</span>
    *   <span>Use</span> `amq.topic` <span>exchange, or create your own exchange of type</span> `topic`
    *   <span>Send sensor values with a routing key starting with</span> `co2` <span>(e.g.,</span> `co2.sensor`<span>)</span>
    *   <span>Send control queries with a routing key starting with</span> `rep` <span>(e.g.,</span> `rep.current` <span>and</span> `rep.average`<span>)</span>
    *   <span>Configure the receiver to listen for</span> `co2.*` <span>and the reporter to listen for</span> `rep.*`
    *   <span>Don’t forget to</span> `ack` <span>the received messages so that they do not remain in the queue.</span>
5.  <span>Submit a single ZIP archive named</span> `NameSurname.zip` <span>with</span> `publishers` <span>and</span> `subscribers` <span>directories inside.</span>

## [<span class="octicon octicon-link"></span>](#Example-Run "Example-Run")<span>Example Run</span>

    $ python publishers/sensor.py
    Enter CO2 level: 499
    Enter CO2 level: 500
    Enter CO2 level: 501
    Enter CO2 level: 500

    $ python subscribers/receiver.py
    [*] Waiting for CO2 data. Press CTRL+C to exit
    2023-04-03 17:19:29: OK
    2023-04-03 17:20:02: OK
    2023-04-03 17:21:05: WARNING
    2023-04-03 17:22:08: OK

* * *

    $ python publishers/control-tower.py
    Enter Query: current
    Enter Query: average

    $ python subscribers/reporter.py
    [*] Waiting for queries from the control tower. Press CTRL+C to exit
    2023-04-03 17:19:30: Latest CO2 level is 499
    2023-04-03 17:23:02: Average CO2 level is 500.0

## [<span class="octicon octicon-link"></span>](#Checklist "Checklist")<span>Checklist</span>

*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>A single submitted file</span> `NameSurname.zip` <span>with the following content inside:</span>

        .
        ├── publishers
        │   ├── sensor.py
        │   └── control-tower.py
        └── subscribers
            ├── receiver.py
            └── reporter.py

*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Publisher scripts correctly read and process user input.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Subscriber scripts only receive intended messages.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Receiver correctly processes sensor values and prints timestamped</span> `WARNING` <span>or</span> `OK` <span>messages accordingly.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>Reporter correctly processes control tower queries and prints the required answers.</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The code does not use any external dependencies (apart from</span> [`pika`](https://pypi.org/project/pika/)<span>)</span>
*   <input class="task-list-item-checkbox" type="checkbox" disabled="disabled"> <span>The source code is the author’s original work. Both parties will be penalized for detected plagiarism.</span>

</div>

<div class="ui-toc dropup unselectable hidden-print" style="display:none;">

<div class="pull-right dropdown">[](# "Table of content")

<div class="toc">

- [Week 3 - Message Brokers](#week-3---message-brokers)
  - [Overview](#overview)
  - [System Architecture](#system-architecture)
    - [**Architecture diagram**](#architecture-diagram)
    - [**Directory structure**](#directory-structure)
    - [**Publishers**](#publishers)
    - [**Subscribers**](#subscribers)
    - [Message Broker (RabbitMQ Server)](#message-broker-rabbitmq-server)
  - [Task](#task)
  - [Example Run](#example-run)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

</div>

<div id="ui-toc-affix" class="ui-affix-toc ui-toc-dropdown unselectable hidden-print" data-spy="affix" style="top:17px;display:none;" null="">

<div class="toc">

- [Week 3 - Message Brokers](#week-3---message-brokers)
  - [Overview](#overview)
  - [System Architecture](#system-architecture)
    - [**Architecture diagram**](#architecture-diagram)
    - [**Directory structure**](#directory-structure)
    - [**Publishers**](#publishers)
    - [**Subscribers**](#subscribers)
    - [Message Broker (RabbitMQ Server)](#message-broker-rabbitmq-server)
  - [Task](#task)
  - [Example Run](#example-run)
  - [Checklist](#checklist)

</div>

<div class="toc-menu">[Expand all](#)[Back to top](#)[Go to bottom](#)</div>

</div>

<script>var markdown = $(".markdown-body"); //smooth all hash trigger scrolling function smoothHashScroll() { var hashElements = $("a[href^='#']").toArray(); for (var i = 0; i < hashElements.length; i++) { var element = hashElements[i]; var $element = $(element); var hash = element.hash; if (hash) { $element.on('click', function (e) { // store hash var hash = this.hash; if ($(hash).length <= 0) return; // prevent default anchor click behavior e.preventDefault(); // animate $('body, html').stop(true, true).animate({ scrollTop: $(hash).offset().top }, 100, "linear", function () { // when done, add hash to url // (default click behaviour) window.location.hash = hash; }); }); } } } smoothHashScroll(); var toc = $('.ui-toc'); var tocAffix = $('.ui-affix-toc'); var tocDropdown = $('.ui-toc-dropdown'); //toc tocDropdown.click(function (e) { e.stopPropagation(); }); var enoughForAffixToc = true; function generateScrollspy() { $(document.body).scrollspy({ target: '' }); $(document.body).scrollspy('refresh'); if (enoughForAffixToc) { toc.hide(); tocAffix.show(); } else { tocAffix.hide(); toc.show(); } $(document.body).scroll(); } function windowResize() { //toc right var paddingRight = parseFloat(markdown.css('padding-right')); var right = ($(window).width() - (markdown.offset().left + markdown.outerWidth() - paddingRight)); toc.css('right', right + 'px'); //affix toc left var newbool; var rightMargin = (markdown.parent().outerWidth() - markdown.outerWidth()) / 2; //for ipad or wider device if (rightMargin >= 133) { newbool = true; var affixLeftMargin = (tocAffix.outerWidth() - tocAffix.width()) / 2; var left = markdown.offset().left + markdown.outerWidth() - affixLeftMargin; tocAffix.css('left', left + 'px'); } else { newbool = false; } if (newbool != enoughForAffixToc) { enoughForAffixToc = newbool; generateScrollspy(); } } $(window).resize(function () { windowResize(); }); $(document).ready(function () { windowResize(); generateScrollspy(); }); //remove hash function removeHash() { window.location.hash = ''; } var backtotop = $('.back-to-top'); var gotobottom = $('.go-to-bottom'); backtotop.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToTop) scrollToTop(); removeHash(); }); gotobottom.click(function (e) { e.preventDefault(); e.stopPropagation(); if (scrollToBottom) scrollToBottom(); removeHash(); }); var toggle = $('.expand-toggle'); var tocExpand = false; checkExpandToggle(); toggle.click(function (e) { e.preventDefault(); e.stopPropagation(); tocExpand = !tocExpand; checkExpandToggle(); }) function checkExpandToggle () { var toc = $('.ui-toc-dropdown .toc'); var toggle = $('.expand-toggle'); if (!tocExpand) { toc.removeClass('expand'); toggle.text('Expand all'); } else { toc.addClass('expand'); toggle.text('Collapse all'); } } function scrollToTop() { $('body, html').stop(true, true).animate({ scrollTop: 0 }, 100, "linear"); } function scrollToBottom() { $('body, html').stop(true, true).animate({ scrollTop: $(document.body)[0].scrollHeight }, 100, "linear"); }</script>