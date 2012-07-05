// Generated by CoffeeScript 1.3.3
(function() {
  var isNumber;

  console.log("start_b");

  isNumber = function(o) {
    return !isNaN((o - 0) && o !== null);
  };

  $(function() {
    var edit_data_change, hide_tabs, mean, stats_mdp_change;
    hide_tabs = function(start) {
      var x, _i, _results;
      _results = [];
      for (x = _i = start; start <= 10 ? _i <= 10 : _i >= 10; x = start <= 10 ? ++_i : --_i) {
        _results.push($("#stats_tabs" + x).hide());
      }
      return _results;
    };
    hide_tabs(1);
    stats_mdp_change = function() {
      var selected;
      selected = $(this).val();
      hide_tabs(0);
      return $("#stats_tabs" + selected).show();
    };
    $(".stats_mdp").change(stats_mdp_change);
    mean = function(the_values) {
      var current_mean, the_mean, total, value, _i, _len;
      total = 0;
      for (_i = 0, _len = the_values.length; _i < _len; _i++) {
        value = the_values[_i];
        total += value;
      }
      the_mean = total / the_values.length;
      the_mean = the_mean.toFixed(2);
      current_mean = parseFloat($("#mean_value").html).toFixed(2);
      if (the_mean !== current_mean) {
        return $("#mean_value").html(the_mean).effect("highlight");
      }
    };
    edit_data_change = function() {
      var real_value, the_mean, the_values, value, values, _i, _len;
      the_values = [];
      values = $('#primary').find(".edit_strain_value");
      for (_i = 0, _len = values.length; _i < _len; _i++) {
        value = values[_i];
        real_value = $(value).val();
        console.log("parent is:", $(value).closest("tr"));
        if (isNumber(real_value) && real_value !== "") {
          the_values.push(parseFloat(real_value));
        }
      }
      return the_mean = mean(the_values);
    };
    $('#primary').change(edit_data_change);
    return console.log("loaded");
  });

}).call(this);
