// Generated by CoffeeScript 1.3.3
(function() {

  console.log("start_b");

  $(function() {
    var hide_tabs, stats_mdp_change;
    hide_tabs = function(start) {
      var x, _i, _results;
      _results = [];
      for (x = _i = start; start <= 10 ? _i <= 10 : _i >= 10; x = start <= 10 ? ++_i : --_i) {
        $("#stats_tabs" + x).hide();
        _results.push(console.log("hidden:", x));
      }
      return _results;
    };
    console.log("start_a");
    hide_tabs(1);
    console.log("hidden?");
    stats_mdp_change = function() {
      var selected;
      console.log("In stats_mdp_change");
      selected = $(this).val();
      console.log("Change was:", selected);
      hide_tabs(0);
      return $("#stats_tabs" + selected).show();
    };
    $(".stats_mdp").change(stats_mdp_change);
    return console.log("tape");
  });

}).call(this);
