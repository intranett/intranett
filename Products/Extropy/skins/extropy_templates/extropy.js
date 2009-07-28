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
