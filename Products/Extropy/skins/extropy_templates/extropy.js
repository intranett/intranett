function showhiddenfield(node){
    // Reveal hidden form-fields. For the extropy type edit forms
    for (var i=0 ;i < node.childNodes.length ; i++){
        n = node.childNodes[i]
        klass = n.className
        if (klass){
            if (klass.indexOf('invisibleformnode') > -1){
                n.style.display = 'inline';
            }
            if (klass.indexOf('formvaluenode') > -1){
                n.style.display = 'none';
            }
        }
    }
}

function toggleEditArea(node){
    node.childNodes[1].style.display = 'none';
    node.childNodes[3].style.display = 'block';
}

var batchAddRows = Object();
batchAddRows = {
    defaults: {},

    // Attach event handlers and store select defaults
    initRows: function() {
        fields = cssQuery('div.batchAddRow > input[type=text]');
        for (i=0; field=fields[i++];) {
            field.onchange = batchAddRows.rowChange;
        }
        // get selects in first row, their current indexes are the defaults
        rows = cssQuery('div.batchAddRow');
        selects = cssQuery('select', rows[0]);
        for (i=0; select=selects[i++];) {
            batchAddRows.defaults[select.name] = select.selectedIndex;
        }
    },

    // Event handler: row contents changed
    rowChange: function() {
        // Empty row's get deleted
        if (!this.value) batchAddRows.deleteRows();

        // Add a row if all but the last one have contents
        fields = cssQuery('div.batchAddRow > input[type=text]');
        for (i=0; i < fields.length - 1; i++) {
            if (!fields[i].value) return;
        };
        batchAddRows.addRow();
    },

    // Number of rows
    length: function() {
        return cssQuery('div.batchAddRow').length;
    },

    // Delete empty rows
    deleteRows: function(row) {
        var fields = cssQuery('div.batchAddRow > input[type=text]');
        var length = fields.length;
        for (i = 0; i < length; i++) {
            if (length < 3) return;
            if (!fields[i].value) {
                batchAddRows.deleteRow(fields[i].parentNode);
                length--;
            }
        }
    },

    // Delete the indicated row
    deleteRow: function(row) {
        row.parentNode.removeChild(row);
    },

    // Add a row at the end
    addRow: function() {
        // Copy the first row at the end
        var rows = cssQuery('div.batchAddRow');
        var new_row = rows[0].cloneNode(true);
        for (i=0; elem=new_row.childNodes[i++];) {
            if (elem.tagName == 'INPUT') {
                elem.value = '';
                elem.onchange = batchAddRows.rowChange;
            };
            if (elem.tagName == 'SELECT') {
                elem.selectedIndex = batchAddRows.defaults[elem.name];
            }
        }

        var next = rows[rows.length - 1].nextSibling;
        if (next) { rows[0].parentNode.insertBefore(new_row, next); }
        else      { rows[0].appendChild(new_row); }
    }
};
registerPloneFunction(batchAddRows.initRows);

// Weekly planning UI
var Plannable = Class.create();
Plannable.prototype = {
    initialize: function(data) {
        Object.extend(this, data);
        this.tr = $('plannable-' + this.uid);
        this.bar = $('bar-' + this.uid);
        this.tr.observe('mousedown',
                        this.initDrag.bindAsEventListener(this));
    },

    initDrag: function(event) {
        if (this._dragEvent) return;
        if(Event.isLeftClick(event)) {
            // Left mouse down, so we may start a drag. Start listening for
            // mouse up (no drag) and mouse move (a real drag started)
            this._dragEvent = this.dragFromTable.bindAsEventListener(this);
            this._mouseUpEvent = this.cleanupDragListeners.bindAsEventListener(this);
            Event.observe(document, 'mousemove', this._dragEvent);
            this.tr.observe('mouseup', this._mouseUpEvent);
            Event.stop(event);
        }
    },

    cleanupDragListeners: function() {
        Event.stopObserving(document, 'mousemove', this._dragEvent);
        this.tr.stopObserving('mouseup', this._mouseUpEvent);
        delete this._dragEvent;
        delete this._mouseUpEvent;
    },

    dragFromTable: function(event) {
        this.cleanupDragListeners();

        // Clone the progressbar, position it, and start dragging it
        var draggable = this.bar.cloneNode(true);
        $('planning').parentNode.insertBefore(draggable, $('planning'));
        Position.absolutize(draggable);
        var pointer = [Event.pointerX(event), Event.pointerY(event)];
        var dim = this._barSize(draggable);
        var pos = Position.cumulativeOffset(draggable);
        var delta = [parseInt(Element.getStyle(draggable, 'left') || '0'),
                     parseInt(Element.getStyle(draggable,'top') || '0')];
        pos[0] -= delta[0];
        pos[1] -= delta[1];
        draggable.style.left = (pointer[0] - pos[0] - (dim.width / 2)) + 'px';
        draggable.style.top = (pointer[1] - pos[1] - (dim.height / 2)) + 'px';
        draggable.style.width = dim.width + 'px';
        draggable.style.height = dim.height + 'px';

        var drag = new Draggable(draggable, {
            endeffect: function(element) {
                Draggables.activeDraggable.destroy();
                element.remove();
            }
        })
        drag.initDrag.bind(drag)(event);
        drag.updateDrag.bind(drag)(event, pointer);
    },

    _barSize: function(bar) {
        // The wrapping a tag has dim (0, 0), so calc contained spans size
        var height = 0;
        var width = 0;
        var spans = $A(bar.getElementsByTagName('span'));
        spans.each(function(span) {
            var dim = span.getDimensions();
            height = Math.max(height, dim.height);
            width += dim.width + 1; // additional margin required
        });
        return {width: width + 1, height: height};
    },

    tabSelect: function(tabid) {
        if (this.tab == tabid) { this.tr.show(); }
        else                   { this.tr.hide(); }
        return true;
    },

    dropped: function(target) {
        var bar = this.bar.cloneNode(true);
        Position.relativize(bar);
        bar.style.top = 'auto';
        bar.style.left = 'auto';
        bar.id = 'cloned-bar-' + this.uid;
        target.appendChild(bar);
        if (this.tr) {
            this.tr.remove();
            PlanningUI.updatePlannables();
        }
    }
}

var Planned = Class.create();
Object.extend(Planned.prototype, Plannable.prototype);
Object.extend(Planned.prototype, {
    initialize: function(data) {
        Object.extend(this, data);
        // Ensure that we get a new clone if just created
        this.bar = $('cloned-bar-' + this.uid) || $('bar-' + this.uid);
        new Draggable(this.bar, {
            endeffect: function(element) {
                Draggables.activeDraggable.destroy();
                element.remove();
            },
            onStart: function(draggable) {
                // Safari will interpret mouseup -> drag -> mousedown as a click
                var bar = draggable.element;
                bar.observe(
                    'click',
                    (function(e) { Event.stop(e) }).bindAsEventListener(bar));
            }
        });

        var base = this.project + '/' + this.deliverable + ': ' + this.title;
        if (this.state == 'completed') {
            this.bar.title = 'Completed: ' + base;
        } else {
            this.bar.title = base + ' (' + this.remaining + ' hours remaining)'
        }
        this.bar.addClassName('state-' + this.state);
        this.bar.addClassName('planned-task');
        this.bar.href = this.bar.href.replace(/\/timereport2$/, '');

        // Now that we got hold of the correct bar, re-id it
        if (this.bar.id.substr(0, 6) == 'cloned')
            this.bar.id = 'bar-' + this.uid;
    },

    save: function() {
        PlanningUI.outstanding_requests += 1;
        $('planned_spinner').show();
        new Ajax.Request(base_url + '/weeklyplan_assign_task', {
            parameters: {
                uid: this.uid,
                responsible: this.responsible,
                date: this.date},
            onSuccess: this.saveDone.bind(this),
            onComplete: function() {
                PlanningUI.outstanding_requests -= 1;
                if (!PlanningUI.outstanding_requests) $('planned_spinner').hide();
            }
        });
    },

    saveDone: function() {
        // Have we been deleted from the plan? Reload available to see it
        if (!this.responsible) PlanningUI.loadAvailableTasks();
    },

    tabSelect: function() { return false; }
});

var PlanningUI = {
    outstanding_requests: 0,
    currentTab: 'overdue',
    tasks: $H(),

    setTask: function(task) {
        this.tasks[task.uid] = task;

        // Update remaining work totals
        $('planning').getElementsByClassName('plan-total')
            .invoke('down').invoke('update', 0);
        this.tasks.values().each(function(task) {
            var totalField = $('plan-total-' + task.responsible);
            if (!totalField) return;
            totalField.update(parseFloat(totalField.innerHTML) + task.remaining);
        });
    },

    initUI: function() {
        var planning = $('planning');
        if (!planning) return;

        // Make filter form perform through AJAX
        var onFilter = (function(event) {
            this.loadAvailableTasks();
            Event.stop(event);
        }).bindAsEventListener(PlanningUI);
        $('filter_form').observe('submit', onFilter);
        $('filter_form').observe('change', onFilter);
        // Remove Plone's submit-confirmation event, an anon method neatly
        // either clears the handler or prevents it to be set.
        $('filter_submit').onclick = function () {}

        var onTabClick = PlanningUI.switchTab.bindAsEventListener(PlanningUI);
        $A($('plannableCategories').getElementsByTagName('a')).invoke(
            'observe', 'click', onTabClick);

        var onToggle = PlanningUI.toggleUser.bindAsEventListener(PlanningUI);
        $('planning').getElementsByClassName('focustoggle').invoke(
            'observe', 'click', onToggle);
        var cookie = readCookie('extropyPlanningFocus');
        if (cookie) PlanningUI.doToggleUser(cookie);

        var onDropEvent = PlanningUI.receiveDraggable.bind(PlanningUI);
        var plan_days = $('planning').getElementsByClassName('plan-day');
        plan_days.each(function(plan_day) {
            Droppables.add(plan_day, {
                hoverclass: 'plan-day-hover',
                onDrop: onDropEvent});
        });

        Droppables.add('visual-portal-wrapper', {
            accept: 'planned-task',
            onDrop: PlanningUI.discardPlanned.bind(PlanningUI)
        });

        WorkflowActions.subscribe(function(action) {
             action.element.up().previous().className = 'state-' + action.state;
             if (!['active', 'assigned', 'unassigned'].include(action.state)) {
                 delete PlanningUI.tasks[action.uid];
                 action.element.up().up().remove();
                 PlanningUI.updatePlannables();
             }
        })

        // Load tasks, but only if not already loaded by the focus toggle
        if (!$F('getResponsiblePerson')) PlanningUI.loadAvailableTasks();
    },

    switchTab: function(event) {
        var tab = Event.findElement(event, 'li');
        var id = tab.id.split('-')[2];
        this.setTab(id);
        Event.stop(event);
    },

    setTab: function(tabid) {
        this.currentTab = tabid
        var tab = $('plannable-cat-' + tabid);
        var tabs = $A(tab.parentNode.getElementsByTagName('li'));
        tabs.invoke('removeClassName', 'selected');
        tab.addClassName('selected');

        this.tasks.values().invoke('tabSelect', tabid);
    },

    loadAvailableTasks: function() {
        var availtasks = this.tasks.inject([], function(acc, item) {
            if (item.value.tab) acc.push(item.key);
            return acc;
        });
        this.tasks.remove.apply(this.tasks, availtasks);

        var parameters = $H(document.location.search.toQueryParams());
        parameters.merge(Form.serialize('filter_form', true));
        $('available_spinner').show();
        new Ajax.Updater(
            'available_tasks', base_url + '/weeklyplan_tasks_available', {
                method: 'get',
                parameters: parameters,
                evalScripts: true,
                onComplete: function() { $('available_spinner').hide(); }
            })
    },

    updatePlannables: function() {
        var counts = $H({overdue: 0, unassigned: 0, future: 0});
        this.tasks.values().each((function(task) {
            if (!task.tabSelect(this.currentTab)) return;
            counts[task.tab] = counts[task.tab] + 1;
        }).bind(this));
        counts.each(function(item) {
            $(item.key + '-count').update(item.value);
        });

        var status = counts.partition(function(item) { return item.value; });
        status[0].each(function(item) { $('plannable-cat-' + item.key).show() });
        status[1].each(function(item) { $('plannable-cat-' + item.key).hide() });

        if (status[0].length) {
            $('plannables').show();
            $('no-plannables').hide();
            if (!status[0].find(function(item) {
                                return item.key == PlanningUI.currentTab })) {
                PlanningUI.setTab(status[0][0].key);
            }
        } else {
            $('plannables').hide();
            $('no-plannables').show();
        }
    },

    receiveDraggable: function(draggable, droppable, event) {
        var uid = draggable.id.split('-')[1];
        var oldtask = this.tasks[uid];
        delete this.tasks[uid];
        oldtask.dropped(droppable);

        var newtask = new Planned({
            uid: oldtask.uid,
            project: oldtask.project,
            deliverable: oldtask.deliverable,
            title: oldtask.title,
            remaining: oldtask.remaining,
            state: oldtask.state,
            responsible: droppable.parentNode.id.substring(5),
            date: droppable.readAttribute('date')
        });

        this.setTask(newtask);
        newtask.save();
    },

    discardPlanned: function(draggable) {
        var uid = draggable.id.split('-')[1];
        var oldtask = this.tasks[uid];
        delete this.tasks[uid];
        oldtask.responsible = '';
        oldtask.date = '';
        oldtask.save();
    },

    toggleUser: function(event) {
        var toggle = Event.findElement(event, 'span');
        var user = toggle.id.substring(7)
        this.doToggleUser(user);
    },

    doToggleUser: function(user) {
        var toggle = $('toggle-' + user);
        var row = toggle.up().up();
        var responsible = $('getResponsiblePerson')

        toggle.toggleClassName('focused');
        if (toggle.hasClassName('focused')) {
            row.siblings().invoke('hide');
            createCookie('extropyPlanningFocus', user, 365);

            // If filter is set to 'All', set to focused user
            if (!$F(responsible)) {
                var index = responsible.descendants()
                    .pluck('value').indexOf(user);
                responsible.selectedIndex = index;
                this.loadAvailableTasks();
            }
        } else {
            row.siblings().invoke('show');
            createCookie('extropyPlanningFocus', '');

            // If filter is set to user, set to 'All'
            if ($F(responsible) == user) {
                responsible.selectedIndex = 0;
                this.loadAvailableTasks();
            }
        }
    }
}
registerPloneFunction(PlanningUI.initUI);

// Today buttons next to date picker
function _todayString() {
    now = new Date();
    day = now.getDate().toString();
    month = (now.getMonth() + 1).toString();
    year = now.getFullYear().toString();

    if (day.length == 1) day = '0' + day;
    if (month.length == 1) month = '0' + month;
    return year + '/' + month + '/' + day;
};

ExtropyTodayButton = Class.create();
ExtropyTodayButton.prototype = {
    today: _todayString(),

    initialize: function(element) {
        this.button = element;
        this.picker = this.button.previous('select');

        this.todayIndex = this.picker.descendants().pluck('value').indexOf(this.today);
        if (this.todayIndex == -1) return;

        this.button.show();
        this.button.observe('click', this.setToday.bindAsEventListener(this));
    },

    setToday: function(event) {
        if (Event.isLeftClick(event)) this.picker.selectedIndex = this.todayIndex;
    }
};
registerPloneFunction(function() {
    var buttons = document.getElementsByClassName('today_button');
    buttons.map(function(el) { return new ExtropyTodayButton(el); });
});

// Now buttons next to time textbox
ExtropyNowButton = Class.create();
ExtropyNowButton.prototype = {
    now: function() {
        var now = new Date();
        var hours = now.getHours().toString();
        var minutes = now.getMinutes().toString();
        if (hours.length == 1) hours = '0' + hours;
        if (minutes.length == 1) minutes = '0' + minutes;
        return hours + ':' + minutes;
    },

    initialize: function(element) {
        this.button = element;
        this.input = this.button.previous('input');
        this.button.show();
        this.button.observe('click', this.setNow.bindAsEventListener(this));
    },

    setNow: function(event) {
        if (Event.isLeftClick(event)) this.input.value = this.now();
    }
};
registerPloneFunction(function() {
    var buttons = document.getElementsByClassName('now_button');
    buttons.map(function(el) { return new ExtropyNowButton(el); });
});

// Workflow actions (action menus with AJAX functionality)
WorkflowAction = Class.create();
WorkflowAction.prototype = {
    initialize: function(uid) {
        this.uid = uid;
        this.element = $('workflowActions-' + uid);
        this.select = this.element.down()

        this.url = this.element.getAttribute('target') + '/@@workflowactions';

        this.onChange = this.doAction.bindAsEventListener(this);
        this.select.observe('change', this.onChange)

        this.state = this.select.down().value
    },

    _markLoading: function() {
        this.select.stopObserving('change', this.onChange);
        this.select.disable();
        this.element.addClassName('loading');
    },

    reload: function() {
        this._markLoading();
        new Ajax.Updater(
            this.element.up(), this.url, {
                evalScripts: true,
                onComplete: this.onComplete.bind(this)
            });
    },

    doAction: function(event) {
        Event.stop(event);
        this._markLoading();
        var action = this.select.getValue();
        new Ajax.Updater(
            {success: this.element.up()}, this.url, {
                parameters: {action: action},
                evalScripts: true,
                onComplete: this.onComplete.bind(this),
                onFailure: this.onError.bind(this)
            });

        return false;
    },

    onComplete: function() {
        var uid = this.uid;
        setTimeout(function() {WorkflowActions.notify(uid)}, 10);
    },

    onError: function() {
        this.reload();
        alert('Transition failed; perhaps the item in question was changed ' +
              "since you loaded this page. It's workflow state has been reloaded.")
    }
}

var WorkflowActions = {
    uids: $H(),
    subscribers: $A(),

    initUI: function() {
        // Re-register workflowactions
        //this.uids.keys().each(this.registerMenu.bind(this));
    },

    registerMenu: function(uid) {
        this.uids[uid] = new WorkflowAction(uid);
    },

    subscribe: function(listener) {
        if (this.subscribers.include(listener)) return;
        this.subscribers.push(listener);
    },

    unsubscribe: function(listener) {
        this.subscribers = this.subscribers.without(listener);
    },

    notify: function(uid) {
        // grab newly loaded WorkflowAction
        var action = WorkflowActions.uids[uid];
        WorkflowActions.subscribers.each(function(subscriber) { subscriber(action) });
    }
}
registerPloneFunction(WorkflowActions.initUI.bind(WorkflowActions));
